from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langserve import add_routes

from ..chains.simple_chain import chain

app = FastAPI(
    title="Sample App to test LangServe",
    version="0.0.1",
    description="This app acts as a server for LangServe",
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


add_routes(app, chain, path="/simple_chain")
