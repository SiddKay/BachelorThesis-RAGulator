from langchain_openai import ChatOpenAI
from langchain_core.runnables import ConfigurableField
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser


# Define the model with configurable fields
model = ChatOpenAI().configurable_fields(
    temperature=ConfigurableField(
        id="temperature",
        name="Temperature",
        description="Controls randomness in the output",
    )
)

# Define the prompt
prompt = PromptTemplate.from_template("tell me a joke about {topic}.")

# Create the chain using pipe syntax
chain = prompt | model | StrOutputParser()
