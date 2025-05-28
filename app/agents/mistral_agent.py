from langchain_community.llms import Ollama # type: ignore
from langchain.prompts import PromptTemplate # type: ignore
from langchain.chains import LLMChain # type: ignore

def load_mistral_agent():
    llm = Ollama(model="mistral")

    prompt = PromptTemplate(
    input_variables=["question", "columns"],
    template="""
You are a helpful data analyst working with a Pandas DataFrame named df.

The DataFrame has the following columns:
{columns}

Your task is to convert a user's natural language question into a valid SQL query.

Guidelines:
- Always write the SQL query assuming the table name is `df`
- Use standard SQL syntax compatible with the `pandasql` Python library
- Do not use backticks, quotation marks, or markdown formatting
- Do not include explanations, notes, or anything other than the SQL
- Only return the SQL statement starting with SELECT

Examples:
Q: Show average income  
A: SELECT AVG(Income) FROM df;

Q: Average wine spending by marital status  
A: SELECT Marital_Status, AVG(MntWines) FROM df GROUP BY Marital_Status;

Now write a valid SQL query for this user question:
Q: {question}  
A:
"""
)





    return LLMChain(llm=llm, prompt=prompt)
