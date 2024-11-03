"""Example of configurable runnables.

This example shows how to use two options for configuration of runnables:

1) Configurable Fields: Use this to specify values for a given initialization parameter
2) Configurable Alternatives: Use this to specify complete alternative runnables
"""

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import ConfigurableField
from langchain_core.output_parsers import StrOutputParser

from dotenv import load_dotenv

load_dotenv()

###############################################################################
#                EXAMPLE 1: Configure fields based on RunnableConfig          #
###############################################################################

model = ChatOpenAI(
    model="gpt-4o-mini", temperature=0.5
).configurable_alternatives(
    ConfigurableField(
        id="llm",
        name="LLM",
        description=(
            "Decide whether to use a high or a low temperature parameter for the LLM."
        ),
    ),
    high_temp=ChatOpenAI(temperature=0.9),
    low_temp=ChatOpenAI(temperature=0.1),
    default_key="medium_temp",
)

prompt = PromptTemplate.from_template(
    "tell me a joke about {topic}."
).configurable_fields(  # Example of a configurable field
    template=ConfigurableField(
        id="prompt",
        name="Prompt",
        description="The prompt to use. Must contain {topic}.",
    )
)

my_op_parser = StrOutputParser()

temp_chain = prompt | model | my_op_parser


###############################################################################
#                EXAMPLE 2: Configure prompt based on RunnableConfig          #
###############################################################################

configurable_prompt = PromptTemplate.from_template(
    "tell me a joke about {topic}."
).configurable_alternatives(
    ConfigurableField(
        id="prompt",
        name="Prompt",
        description="The prompt to use. Must contain {topic}.",
    ),
    default_key="joke",
    fact=PromptTemplate.from_template(
        "tell me a fact about {topic} in {language} language."
    ),
)
prompt_chain = configurable_prompt | model | StrOutputParser()
