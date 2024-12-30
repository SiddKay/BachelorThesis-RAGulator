# RAGulator

<!-- @import "[TOC]" {cmd="toc" depthFrom=2 depthTo=6 orderedList=false} -->

<!-- code_chunk_output -->

- [Quick Start](#quick-start)
  - [Prerequisites](#prerequisites)
  - [Initial Setup](#initial-setup)
    - [LCEL Chain Files](#lcel-chain-files)
    - [Backend](#backend)
    - [Frontend](#frontend)
  - [Subsequent Runs](#subsequent-runs)
- [Typical evaluation flow](#typical-evaluation-flow)

<!-- /code_chunk_output -->

RAGulator is a proof-of-concept framework built to enable real-time evaluation of custom RAG chains created using [LangChain Expression Language (LCEL)](https://python.langchain.com/docs/concepts/lcel/).

This project is a culmination of my bachelor thesis at TU Darmstadt.

## Quick Start

These instructions will help you set up the project on your local machine for development and testing purposes. To ensure the persistence of evaluation sessions and the related data, a [postgreSQL](https://www.postgresql.org/docs/) database is used inside a [Docker](https://www.docker.com/products/docker-desktop/) container.

### Prerequisites

Before you begin, make sure you have the following installed:

- [Python 3.12.x](https://www.python.org/downloads/)
- [pip](https://pip.pypa.io/en/stable/installation/) (Usually comes with python installation)
- [Docker Desktop](https://docs.docker.com/engine/install/) (Recommended)

### Initial Setup

1. Clone the repository:

   ```bash
    git clone git@github.com:SiddKay/BachelorThesis-RAGulator.git
   ```

2. Rename the cloned directory to `RAGulator` to avoid any issues with the project structure and navigate to the root directory of the project:

   ```bash
   cd RAGulator
   ```

#### LCEL Chain Files

1. Make sure that (valid) LCEL chain files (.py) to be evaluated are present in the [backend/langserve/chains/](./backend/langserver/chains/) directory. Some example chains can be found in this directory for reference.

2. Next, import the chain file and add a route for it at the end of [backend/langserve/server.py](./backend/langserver/server.py) file. For instance, to add a route for a chain file named `useful_chain.py`, where the name of the LCEL chain is `my_rag_chain`, add the following line at the end of the file:

   ```python
   add_routes(app, my_rag_chain, path="/useful_chain")
   ```

#### Backend

1. Navigate to the `backend/` directory of the root:

   ```bash
   cd backend
   ```

2. Setup a virtual environment _(optional but recommended)_:

   ```bash
   # Create a new virtual environment
   python -m venv .venv

   # Activate the venv
   source .venv/bin/activate    #Linux/MacOS

   .venv/Scripts/activate   # Windows
   ```

3. Install the necessary dependencies for the backend:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the following command to set up your environment variables:

   ```bash
   cp .env.example .env
   ```

   > **Note 1**: This will create a `.env` file from the sample `.env.example` file.
   > Please modify the values in the `.env` file as needed.

   > **Note 2**: The `MAIN_PORT` in the `.env` file is set to `8000`. If the port is already in use, please change it to a different port number. Similarly, adjust the `LANGSERVE_PORT` which is set to `8001` by default.

5. Start Docker desktop on your local machine and run the following command to setup the postgreSQL database in a Docker container:

   ```bash
    docker-compose up -d
   ```

6. Starting the both the Main as well as the LangServe servers:

   ```bash
   python main.py
   ```

Check the terminal for the relevant endpoints and to see where the server is running. The API endpoints can be tested at _[http://localhost:8000/docs](http://localhost:8000/docs)_ & _[http://localhost:8001/docs](http://localhost:8001/docs)_ for Main app and LangServe, respectively.

#### Frontend

1. Open a new terminal and Navigate to the `frontend/` directory of the project root:

   ```bash
   cd frontend
   ```

2. Install the necessary dependencies for the frontend:

   ```bash
   npm install
   ```

3. Start the frontend server:

   ```bash
   npm run dev
   ```

4. Open your browser and navigate to _[http://localhost:3000/sessions](http://localhost:3000/sessions)_ to view the RAGulator web application.

### Subsequent Runs

After the [initial setup](#initial-setup), for every subsequent usage of the app, you can directly start the backend servers and the frontend. Make sure to place the LCEL chain files in the [backend/langserve/chains/](./backend/langserver/chains/) directory.

1. Start Docker desktop app, and check if the the container `ragulator_database` exists and is running. If the container is not present, navigate to the `backend/` directory and create a new one using the following commands:

   ```bash
   cd backend

   docker-compose up -d
   ```

2. To start the backend servers, run the following command in the `backend/` directory:

   ```bash
   python main.py
   ```

3. To start the frontend server, open a new terminal and navigate to the `RAGulator/frontend/` directory and run the following commands:

   ```bash
   npm run dev
   ```

4. Open your browser and navigate to _[http://localhost:3000/sessions](http://localhost:3000/sessions)_ to view the RAGulator web application.

## Typical evaluation flow

> **Note:** It is recommended to have the clipboard history enabled on your system to copy and paste multiple ids at the same time during the evaluation run.

Since the app frontend is currently missing a working sidebar with the relevant functionality to enable real-time evaluation of the LCEL chains, a typical evaluation flow involves the usage of the API endpoints directly via the OpenAPI docs UI. The following steps outline the process:

1. Once a session is created in the RAGulator interface, navigate to the OpenAPI docs UI to access the endpoints related to the chain selection and configuration adjustment at _[http://localhost:8000/docs](http://localhost:8000/docs)_.

2. Under the `sessions` section, run the `GET /v1/sessions/` endpoint by clicking on the `Try it out` button, to get all the available sessions. Copy the `id` (first JSON key-value pair) of the session you want to evaluate.

3. Next, navigate to the `chains` section and run the `GET /v1/available-chains` endpoint to detect all the available chain files in the [backend/langserver/chains/](./backend/langserver/chains/) directory. Form the API response body, copy the `file_name` of the chain you want to evaluate.

4. Now, access the `POST /v1/sessions/{session_id}/select-chains` endpoint and paste the copied session `id` in the `session_id` parameter and the copied `file_name` in the `file_names` field in the request body. Click on the `Execute` button to select the chain for evaluation. From the API response, copy the generated chain `id` of the selected chain.

5. To get the configuration schema of the selected chain, access the `GET /v1/sessions/{session_id}/chains/{chain_id}/configurations/schema` endpoint under the `configurations` section, and paste the copied session `id` in the `session_id` parameter and the chain `id` in the `chain_id` parameter. Click on the `Execute` button to get the configuration schema.

6. Based on the configuration schema, you can create a `config_values` object and access the "Create Configuration" API at `POST /v1/sessions/{session_id}/chains/{chain_id}/configurations` endpoint to set the configuration values for the selected chain. Paste the copied session `id` and the chain `id` in the `session_id` and `chain_id` parameters, respectively. Then paste the `config_values` object in the request body. Click on the `Execute` button to set the configuration values. From the API response, copy the generated `id` of the created configuration.
   For a typical LCEL chain with `search_kwargs_faiss`, `answer_style` and `generation_max_tokens` parameters as the defined configurable fields, the `config_values` object would look like this:

   ```json
   {
     "config_values": {
       "search_kwargs_faiss": { "k": 2 },
       "answer_style": "brief",
       "generation_max_tokens": 5
     }
   }
   ```

7. Once the chain is selected, the configuration is set, and the questions have been added to the session via the RAGulator web-app interface, you can now invoke the chain concurrently for all the provided questions with the selected configuration. Access the `GET /v1/sessions/{session_id}/chains/{chain_id}/configuration/{config_id}/invoke` endpoint under the `chains` section, and paste the copied session `id`, chain `id`, and configuration `id` in the `session_id`, `chain_id`, and `config_id` parameters, respectively. Click on the `Execute` button to invoke the chain. The generated answers will be displayed in the API response as well as the RAGulator web-app interface.

Similarly, create new configurations and invoke the chain multiple times to evaluate the chain with different configurations for all the questions.
