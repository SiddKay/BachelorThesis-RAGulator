# RAGulator Backend

The overall backend consists of two servers:

- **Main FastAPI server** - This is the main server that serves all the main app endpoints. A [FastAPI server](https://fastapi.tiangolo.com/) is set up in conjunction with [uvicorn](https://www.uvicorn.org/) to enable communication between the Backend and the Frontend.

- **LangServe server** - This is a separate server that runs the [LangServe](https://python.langchain.com/docs/langserve/) service to serve the endpoints that provide access to the LCEL chains placed in the `backend/langserver/chains/` directory.

## Directory Structure

```bash
backend/
├── api/            # API endpoints to enable communication with frontend
├── core/           # Backend custom logging logic
├── db/             # Database config
├── models/         # Database models
├── schemas/        # Pydantic schemas
├── services/       # Business logic to handle API requests
├── langserver/     # LangServe server to serve LCEL chains
├── scripts/        # Scripts to initiate new db in docker container
├── main.py         # Main FastAPI server
```

## Database admin panel

Since we are using `PostgreSQL` as our database, we can use `adminer` to manage the database. To access the admin panel once the backend is completely setup and running (consult [project README](../README.md)), visit [http://localhost:8080](http://localhost:8080) in your browser. Use the following credentials to login:

- **System**: `PostgreSQL`
- **Server**: `db`
- **Username**: `postgres`
- **Password**: `postgres`
- **Database**: `ragulator`
