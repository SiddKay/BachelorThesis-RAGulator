from langchain_community.vectorstores import FAISS
from langchain_core.runnables import (
    Runnable,
    ConfigurableField,
    RunnablePassthrough,
)
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.schema import Document
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

# 0. Sample documents to use for the retriever
documents = [
    Document(page_content="Frankfurt is a metropolitan city in Germany."),
    Document(page_content="Berlin is the capital of Germany."),
    Document(
        page_content="Prague a popular tourist destination in Czech Republic."
    ),
    Document(page_content="Madrid is the largest city in Spain."),
]

# 1. Document retriever
vector_store = FAISS.from_documents(documents, embedding=OpenAIEmbeddings())
retriever = vector_store.as_retriever().configurable_fields(
    search_kwargs=ConfigurableField(
        id="search_kwargs_faiss",
        name="Top K Documents",
        description="Number of most relevant documents to retrieve",
    ),
)

# 2. Answer generation prompt template options.
brief_answer = """
Based only on the provided context, answer as briefly as possible:
Question: {question}, Context: {context}
"""

elaborate_answer = """
Based on the provided context, provide a detailed and comprehensive answer:
Question: {question}, Context: {context}
"""

configurable_answer_prompt = PromptTemplate.from_template(
    template=brief_answer
).configurable_alternatives(
    ConfigurableField(
        id="answer_style",
        name="Answer Style",
        description="Style of answer generation - concise or elaborate",
    ),
    elaborate_answer=PromptTemplate.from_template(template=elaborate_answer),
    default_key="brief_answer",
)

# 3. Answer generation model
configurable_generation_model = ChatOpenAI(
    model="gpt-4o-mini"
).configurable_fields(
    max_tokens=ConfigurableField(
        id="generation_max_tokens",
        name="Generation Max Tokens",
        description="Max Tokens allowed for answer generation",
    ),
)

# Full RAG chain
chain: Runnable = (
    RunnablePassthrough()
    | {"context": retriever, "question": lambda x: x}
    | configurable_answer_prompt
    | configurable_generation_model
    | StrOutputParser()
)

# Example configuration
chain_configuration = chain.with_config(
    {
        "search_kwargs_faiss": {"k": 2},  # or {"k": 4}
        "answer_style": "brief",  # or "elaborate"
        "generation_max_tokens": 5,  # or 30
    }
)
