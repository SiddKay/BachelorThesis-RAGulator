import uvicorn
from app.server import app


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="localhost",
        port=8000,
        reload=True,
        log_level="info",
    )
