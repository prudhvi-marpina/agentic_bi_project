import streamlit as st  # type: ignore
import pandas as pd
from pandasql import sqldf  # type: ignore
import plotly.express as px  # type: ignore
import plotly.graph_objects as go
import traceback
from typing import Optional
import numpy as np
from pandas.api.types import is_numeric_dtype
import json
import os
from datetime import datetime

from app.utils.agent_runner import (
    run_query_agent,
    run_insight_agent,
    run_chart_agent
)

def execute_sql_safely(query: str, dataframe: pd.DataFrame) -> Optional[pd.DataFrame]:
    """Execute SQL query with proper error handling."""
    try:
        pysqldf = lambda q: sqldf(q, {"df": dataframe})
        result = pysqldf(query)
        if result.empty:
            st.warning("Query executed successfully but returned no results.")
            return None
        return result
    except Exception as e:
        st.error(f"SQL Execution Error: {str(e)}")
        st.code(traceback.format_exc(), language="python")
        return None

def profile_dataframe(df: pd.DataFrame) -> None:
    """Generate and display a basic data profile."""
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("📊 Basic Statistics")
        st.write(f"- Total Rows: {len(df):,}")
        st.write(f"- Total Columns: {len(df.columns):,}")
        st.write(f"- Missing Values: {df.isna().sum().sum():,}")
        
    with col2:
        st.write("📈 Numeric Columns")
        numeric_cols = [col for col in df.columns if is_numeric_dtype(df[col])]
        st.write(f"- Count: {len(numeric_cols)}")
        st.write("- Names: " + ", ".join(numeric_cols))

def validate_data(df: pd.DataFrame) -> bool:
    """Validate the uploaded dataset."""
    if len(df.columns) < 2:
        st.error("❌ Dataset must have at least 2 columns")
        return False
        
    if len(df) < 1:
        st.error("❌ Dataset is empty")
        return False
        
    if df.columns.duplicated().any():
        st.error("❌ Dataset contains duplicate column names")
        return False
        
    return True

def save_query(query: str, sql: str, insight: str) -> None:
    """Save a query to the saved_queries directory."""
    os.makedirs("saved_queries", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"saved_queries/query_{timestamp}.json"
    
    query_data = {
        "timestamp": timestamp,
        "query": query,
        "sql": sql,
        "insight": insight
    }
    
    with open(filename, "w") as f:
        json.dump(query_data, f, indent=2)
    
def load_saved_queries() -> list:
    """Load all saved queries."""
    if not os.path.exists("saved_queries"):
        return []
        
    queries = []
    for filename in os.listdir("saved_queries"):
        if filename.endswith(".json"):
            with open(f"saved_queries/{filename}", "r") as f:
                queries.append(json.load(f))
    return sorted(queries, key=lambda x: x["timestamp"], reverse=True)

def create_interactive_chart(df: pd.DataFrame, chart_type: str = "auto") -> Optional[go.Figure]:
    """Create an interactive chart based on the data and type."""
    if df.empty:
        return None
        
    if chart_type == "auto":
        # Determine best chart type based on data
        num_cols = df.select_dtypes(include=[np.number]).columns
        if len(num_cols) >= 2:
            chart_type = "scatter"
        elif len(df.columns) == 2:
            chart_type = "bar"
        else:
            chart_type = "line"
    
    try:
        if chart_type == "scatter":
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            fig = px.scatter(df, x=numeric_cols[0], y=numeric_cols[1],
                           title="Interactive Scatter Plot")
        elif chart_type == "bar":
            fig = px.bar(df, title="Interactive Bar Chart")
        elif chart_type == "line":
            fig = px.line(df, title="Interactive Line Chart")
        else:
            return None
            
        # Add common layout improvements
        fig.update_layout(
            template="plotly_white",
            title_x=0.5,
            margin=dict(t=50, l=0, r=0, b=0),
            height=500
        )
        
        return fig
    except Exception as e:
        st.error(f"Failed to create chart: {str(e)}")
        return None

# Set Streamlit page config
st.set_page_config(page_title="Agentic BI", layout="wide")

# Title
st.title("📊 Agentic BI: Conversational Data Explorer")

# File uploader
uploaded_file = st.file_uploader("📁 Upload your CSV file", type=["csv"])

# Data handling
if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        
        if not validate_data(df):
            st.stop()
            
        st.success("✅ File uploaded successfully!")

        # Data preview with enhanced profiling
        st.subheader("📄 Data Profile")
        profile_dataframe(df)
        
        with st.expander("Show Data Preview"):
            st.dataframe(df.head())
            
        with st.expander("Show Detailed Statistics"):
            st.write(df.describe())
            
        # Enhanced column preview with types
        with st.expander("🧾 Column Information"):
            for col in df.columns:
                dtype = df[col].dtype
                unique_count = df[col].nunique()
                missing = df[col].isna().sum()
                st.write(f"**{col}** ({dtype})")
                st.write(f"- Unique values: {unique_count}")
                st.write(f"- Missing values: {missing}")
                if is_numeric_dtype(df[col]):
                    st.write(f"- Range: [{df[col].min()}, {df[col].max()}]")

        # User query section
        st.subheader("🤖 Ask a Question About Your Data")
        
        # Load saved queries
        saved_queries = load_saved_queries()
        if saved_queries:
            st.write("💾 Load a saved query:")
            selected_query = st.selectbox(
                "Select a previous query",
                options=[q["query"] for q in saved_queries],
                index=None
            )
            if selected_query:
                user_query = selected_query
            
        user_query = st.text_input("Type your question here (e.g., 'Compare wine and meat spending'):", value=user_query if 'user_query' in locals() else "")

        if user_query:
            st.info(f"Your question: {user_query}")
            columns = ", ".join(df.columns)

            # Step 1: Generate SQL
            with st.spinner("Generating SQL..."):
                generated_sql = run_query_agent(user_query, columns)

            st.subheader("🧠 Generated SQL")
            st.code(generated_sql, language="sql")

            # Step 2: Execute SQL
            with st.spinner("Running SQL on data..."):
                result_df = execute_sql_safely(generated_sql, df)
                
            if result_df is not None:
                st.subheader("📈 Result")
                st.dataframe(result_df)
                
                # Add download button for results
                csv = result_df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Results",
                    data=csv,
                    file_name="query_results.csv",
                    mime="text/csv"
                )

                # Step 3: Generate Chart
                if not result_df.empty:
                    with st.spinner("Creating chart..."):
                        formatted_result = result_df.to_markdown(index=False)
                        chart_code = run_chart_agent(user_query, formatted_result)

                    # Chart options
                    st.subheader("📊 Visualization")
                    chart_type = st.selectbox(
                        "Select chart type:",
                        options=["auto", "scatter", "bar", "line"],
                        index=0
                    )
                    
                    fig = create_interactive_chart(result_df, chart_type)
                    if fig:
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Export options
                        if st.button("📥 Export Chart as HTML"):
                            html = fig.to_html()
                            st.download_button(
                                label="Download HTML",
                                data=html,
                                file_name="chart.html",
                                mime="text/html"
                            )
                    else:
                        st.warning("Could not create chart with the current data.")

                    # Step 4: Generate Insight after plotting
                    with st.spinner("Generating insight..."):
                        insight = run_insight_agent(user_query, formatted_result)

                    st.subheader("🧠 Insight Summary")
                    st.success(insight)

                    # Step 5: Session memory
                    if "qa_history" not in st.session_state:
                        st.session_state.qa_history = []

                    qa_key = f"{user_query.strip()}|{generated_sql.strip()}"
                    if qa_key not in [f"{q['question']}|{q['sql']}" for q in st.session_state.qa_history]:
                        st.session_state.qa_history.append({
                            "question": user_query,
                            "sql": generated_sql,
                            "insight": insight
                        })

                    # Show past Q&A
                    st.subheader("📚 Previous Questions")
                    for item in st.session_state.qa_history[::-1]:
                        st.markdown(f"**Q:** {item['question']}")
                        st.code(item['sql'], language="sql")
                        st.success(item["insight"])
                        st.markdown("---")

                    # Add save query button after generating insight
                    if "insight" in locals():
                        if st.button("💾 Save this query"):
                            save_query(user_query, generated_sql, insight)
                            st.success("Query saved successfully!")

    except Exception as e:
        st.error(f"❌ Error reading the file: {e}")
else:
    st.warning("⬆️ Please upload a CSV file to get started.")
