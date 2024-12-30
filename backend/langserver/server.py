from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .chains.simple_chain import rag_chain as simple_rag_chain
from .chains.complex_configurable_chain import rag_chain
from .chains.experimental_chain import chain
from langserve import add_routes

app = FastAPI(
    title="Simple App to serve chains using LangServe",
    version="0.0.1",
)

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


add_routes(app, simple_rag_chain, path="/simple_chain")
add_routes(app, rag_chain, path="/complex_configurable_chain")
add_routes(app, chain, path="/experimental_chain")
