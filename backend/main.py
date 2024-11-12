import uvicorn
import os

from app.core.logger import setup_logging, get_logger

# from app.server import app

os.system("color")


def main():
    # Setup logging
    setup_logging(log_file="logs/ragulator.log.jsonl")
    logger = get_logger(__name__)

    # Basic code to test logging
    logger.debug("debug message")
    logger.info("info message")
    logger.warning("warning message")
    logger.error("error message")
    logger.critical("critical message")
    logger.info("Starting Uvicorn server...")
    try:
        1 / 0
    except ZeroDivisionError:
        logger.exception("exception message")


if __name__ == "__main__":
    main()
    # uvicorn.run(app, host="localhost", port=8000)
