from langchain_community.chat_models import ChatCohere
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os
from dotenv import load_dotenv

load_dotenv()
cohere_api_key = os.getenv("COHERE_API_KEY")

llm = ChatCohere(cohere_api_key=cohere_api_key)
parser = StrOutputParser()

prompt_template = PromptTemplate.from_template("""
You are an assistant providing structured info about institutions.
Based on the following details, generate a summary:

Institution Name: {name}
Founder: {founder}
Founded Year: {founded_year}
Branches: {branches}
Employees: {num_employees}
Summary: {summary}

Give a clear summary of the institution using this information.
""")

def ask_with_prompt(info) -> str:
    prompt = prompt_template.format(**info.dict())
    return llm.invoke(prompt)
