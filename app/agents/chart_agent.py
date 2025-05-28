from langchain_community.llms import Ollama # type: ignore
from langchain.prompts import PromptTemplate # type: ignore
from langchain.chains import LLMChain # type: ignore

def load_chart_agent():
    llm = Ollama(model="mistral")

    prompt = PromptTemplate(
        input_variables=["question", "result"],
        template="""
You are a data visualization assistant working in Python using Plotly Express.

You have access to a Pandas DataFrame named `df`, which contains the result of a SQL query.

Here’s the user’s question:
"{question}"

Here is the result DataFrame:
{result}

Your task:
- Write a single valid Plotly Express code snippet that starts with: fig =
- Reference only column names that actually exist in the `df` DataFrame
- Never use placeholder names like 'column_0', 'value', or 'category'
- Do NOT hardcode any values — use column names as variables
- If `df` has only one column, use it on the y-axis
- If `df` has two columns, use the first column as x-axis and the second as y-axis
- If `df` has more than two columns, choose the best pair of columns based on the user's question
- Do not return any extra text, markdown, explanation, or code formatting
- Return only one line of code that is executable with `exec()` in Python

Now generate the appropriate Plotly Express chart code.


"""
    )

    return LLMChain(llm=llm, prompt=prompt)
