from langchain_community.llms import Ollama # type: ignore
from langchain.prompts import PromptTemplate # type: ignore
from langchain.chains import LLMChain # type: ignore

def load_insight_agent():
    llm = Ollama(model="mistral")

    prompt = PromptTemplate(
        input_variables=["question", "result"],
        template="""
You are a helpful data analyst assisting users in understanding their data.

The user asked this question:
"{question}"

Here is the output of the data analysis after executing the query:
{result}

A chart based on this result was just shown to the user.

Now, write a clear and simple explanation of what the result means. Focus on:
- Key trends, comparisons, or outliers
- What the user should notice from the chart
- Patterns that could be useful for decision making

Avoid using technical terms, raw SQL, or column names. Write in simple, natural English as if explaining to a non-technical audience.

Keep it short, helpful, and human.

"""
    )

    return LLMChain(llm=llm, prompt=prompt)
