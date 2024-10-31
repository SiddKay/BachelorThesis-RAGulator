# RAGulator Backend

This directory contains the backend for RAGulator, an evaluation framework for RAG chains created using [LangChain Expression Language (LCEL)](https://python.langchain.com/docs/concepts/lcel/).

In this directory, a [FastAPI server](https://fastapi.tiangolo.com/) is set up in conjuntion with [uvicorn](https://www.uvicorn.org/) to enable communication between the Backend and the Frontend.

WIP/TODO: Add more details about LangServe and the API endpoints.

## Getting Started

These instructions will help you set up and run the backend server seperately.

### Prerequisites

Before you begin, make sure you have the following installed:

- `Python 3.12.x`
- `pip (Python package installer)`

### Installation

1. After installing the project and entering the project directory, proceed to the **backend** directory:

   ```bash
   cd backend
   ```

2. Setup a virtual environment _(optional but recommended)_:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

   > For Windows users, the command to activate the virtual environment is:
   >
   > ```bash
   > .venv/Scripts/activate
   > ```

3. Install all the necessary dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up your environment variables:

   - Create a `.env` file in the **backend** directory, which contains the relevant environment variables.
   - The example content for the `.env` file can be found in the `.env.example` file.

### Starting the Server

To start a local server, run the following command in the **backend** directory:

```bash
uvicorn src.main:app --reload
```

Check the terminal for the relevant endpoints and to see where the server is running _(most likely at [http://127.0.0.1:8000](http://127.0.0.1:8000))_.

## API Testing

Once the server is running, you can visit [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) in your browser to access the Swagger documentation and test the available endpoints.
