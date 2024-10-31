from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langserve import add_routes

from ..routes import extract_chain_config

from ..chains.config_chain import test_chain

app = FastAPI(
    title="Sample App to test LangServe",
    version="0.0.1",
    description="Spin up a simple API server using Langchain's Runnable interfaces",
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

app.include_router(extract_chain_config.router)


add_routes(app, test_chain, path="/configurable_params")
