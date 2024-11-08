from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

from dotenv import load_dotenv
import os

load_dotenv()

model_name = os.environ.get("OPENAI_MODEL_NAME")

model = ChatOpenAI(model=model_name)

prompt = PromptTemplate.from_template("tell me a joke about {topic}.")

chain = prompt | model | StrOutputParser()
