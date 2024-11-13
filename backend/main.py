import uvicorn
import os

from app.core.logger import setup_logging, get_logger
from app.server import app

os.system("color")


def main():
    # Setup logging
    setup_logging(log_file="logs/ragulator.log.jsonl")
    logger = get_logger(__name__)
    logger.info("Logger setup complete")


if __name__ == "__main__":
    main()
    uvicorn.run(app, host="localhost", port=8000)
