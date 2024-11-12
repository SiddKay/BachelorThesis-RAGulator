import uvicorn
from app.services.logger import LoggingManager, get_logger

# from app.server import app

logger = get_logger("ragulator_logger")


def main():
    # Setup logging
    logging_manager = LoggingManager()
    logging_manager.setup()

    # Basic code to test logging
    logger.debug("debug message")
    logger.info("info message")
    logger.warning("warning message")
    logger.error("error message")
    logger.critical("critical message")
    try:
        1 / 0
    except ZeroDivisionError:
        logger.exception("exception message")
    logger.info("Starting Uvicorn server...")


if __name__ == "__main__":
    main()
    # uvicorn.run(app, host="localhost", port=8000)
