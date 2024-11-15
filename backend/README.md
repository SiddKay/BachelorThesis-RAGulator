# RAGulator Backend

This directory contains the backend for RAGulator, an evaluation framework for RAG chains created using [LangChain Expression Language (LCEL)](https://python.langchain.com/docs/concepts/lcel/).

In this directory, a [FastAPI server](https://fastapi.tiangolo.com/) is set up in conjuntion with [uvicorn](https://www.uvicorn.org/) to enable communication between the Backend and the Frontend.

WIP/TODO: Add more details about LangServe and the API endpoints.

## Getting Started

These instructions will help you set up and run the backend server seperately.

### Prerequisites

Before you begin, make sure you have the following installed:

- [Python 3.12.x](https://www.python.org/downloads/)
- [pip](https://pip.pypa.io/en/stable/installation/) (Usually comes with python installation)
- [Docker Desktop](https://docs.docker.com/engine/install/) (Recommended)

### Installation

1. After installing the project and entering the project directory, proceed to the **backend** directory:

   ```bash
   cd backend
   ```

2. Setup a virtual environment _(optional but recommended)_:

   ```bash
   python -m venv .venv

   # Activate the virtual environment (Linux/MacOS)
   source .venv/bin/activate

   # Activate the virtual environment (Windows)
   .venv/Scripts/activate
   ```

3. Install all the necessary dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the following command to set up your environment variables:

   ```bash
   cp .env.example .env
   ```

   > This will create a `.env` file from the sample `.env.example` file.
   > You should modify the values in the `.env` file as needed.

5. Start docker desktop and run the following command to setup the database:

   ```bash
   docker-compose up -d
   ```

### Starting the Server

To start a local server, run the following command in the **backend** directory:

```bash
uvicorn main:app --reload
```

Check the terminal for the relevant endpoints and to see where the server is running _(most likely at [http://127.0.0.1:8000](http://127.0.0.1:8000))_.

## Database admin panel

Since we are using `PostgreSQL` as our database, we can use `adminer` to manage the database. To access the admin panel, visit [http://localhost:8080](http://localhost:8080) in your browser. Use the following credentials to login:

- **System**: `PostgreSQL`
- **Server**: `db`
- **Username**: `postgres`
- **Password**: `postgres`
- **Database**: `ragulator`

## API Testing

Once the server is running, you can visit [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) in your browser to access the Swagger documentation and test the available endpoints.
