from langchain_openai import ChatOpenAI
from langchain_core.runnables import ConfigurableField
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

model = ChatOpenAI()

# Make the prompt configurable
prompt = PromptTemplate.from_template(
    "Write about {topic}."
).configurable_fields(
    template=ConfigurableField(
        id="template",
        name="Prompt Template",
        description="Template for generating content",
    )
)

chain = prompt | model | StrOutputParser()
