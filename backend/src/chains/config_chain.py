from langchain_openai import ChatOpenAI
from langchain_core.runnables import ConfigurableField
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

from dotenv import load_dotenv

load_dotenv()

# false_model = ChatOpenAI().configurable_fields(
#     mode1l=ConfigurableField(
#         id="1",
#         name="1",
#         description="1",
#     )
# )


model = ChatOpenAI()

prompt = PromptTemplate.from_template("tell me a joke about {topic}.")

test_chain = prompt | model | StrOutputParser()
