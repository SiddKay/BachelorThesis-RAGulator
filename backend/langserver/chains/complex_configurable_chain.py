from langchain_community.vectorstores import FAISS
from langchain_core.runnables import (
    Runnable,
    ConfigurableField,
    RunnablePassthrough,
)
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain.schema import Document
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()


# Sample documents to use for the retriever
sample_docs = [
    Document(page_content="Cats love Tuna"),
    Document(page_content="Cats love Milk"),
    Document(page_content="Cats hate Water"),
    Document(page_content="Cats hate Dogs"),
]


# 0. Query reformulation prompt. TODO: Make this configurable
reformulation_prompt = ChatPromptTemplate.from_template(
    "Rewrite the user query to be more specific and searchable. User query: {question}"
)


# 1. Query Reformulation model
reformulation_model = ChatOpenAI(
    model="gpt-4o-mini"
).configurable_alternatives(
    ConfigurableField(
        id="reformulation_model",
        name="Reformulation Model",
        description="Model to use for query reformulation",
    ),
    gpt_35_turbo=ChatOpenAI(model="gpt-3.5-turbo"),
    default_key="gpt_4o_mini",
)


# 2. Document Retriever
vector_store = FAISS.from_documents(sample_docs, embedding=OpenAIEmbeddings())

retriever = vector_store.as_retriever().configurable_fields(
    search_kwargs=ConfigurableField(
        id="search_kwargs_faiss",
        name="Search Kwargs",
        description="The search kwargs to use",
    ),
)

# 3. Answer generation prompt template. TODO: Make this configurable
answer_prompt = """
Only based on the provided context, answer the question in short:
Context: {context}
Question: {question}
"""

configurable_answer_prompt = PromptTemplate.from_template(
    template=answer_prompt
).configurable_fields(
    template=ConfigurableField(
        id="answer_prompt",
        name="Answer Prompt",
        description="Prompt to use for answer generation",
    ),
)

custom_prompt = ChatPromptTemplate.from_template(template=answer_prompt)

# 4. Answer generation model
generation_model = ChatOpenAI(model="gpt-4o-mini").configurable_fields(
    model_name=ConfigurableField(
        id="generation_model",
        name="Generation Model",
        description="Model to use for final generation",
    ),
    temperature=ConfigurableField(
        id="generation_temperature",
        name="Generation Temperature",
        description="Temperature for generation",
    ),
    max_tokens=ConfigurableField(
        id="generation_max_tokens",
        name="Generation Max Tokens",
        description="Max Tokens for generation",
    ),
)


# 5. Output parser with JSON parse as an alternative.
# Make sure to configure the custom_prompt to generate JSON output
custom_parser = StrOutputParser().configurable_alternatives(
    ConfigurableField(
        id="output_parser",
        name="Output Parser",
        description="Parser to use for the output format",
    ),
    json_parser=JsonOutputParser(),
    default_key="str_parser",
)

# Full RAG chain
rag_chain: Runnable = (
    {
        # 1. Reformulate the user query
        "question": RunnablePassthrough(),
        "reformulated_query": reformulation_prompt | reformulation_model,
    }
    | {
        "context": retriever,
    }
    | (configurable_answer_prompt | generation_model | custom_parser)
)

# Example configuration
configured_chain = rag_chain.with_config(
    {
        "search_kwargs_faiss": {"k": 2},
        "reformulation_model": "gpt_4o_mini",  # Alternative - "gpt_35_turbo"
        "generation_model": "gpt-4o-mini",
        "generation_temperature": 1,
        "generation_max_tokens": 10,
        "output_parser": "str_parser",  # Alternative - "json_parser"
    }
)

# Example usage
# configured_chain.invoke("List all the things that cats love and dont like")
