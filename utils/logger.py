import logging


def setup_logging():
    """
    Configures the logging system with a standard format.
    
    - Logs messages to both a file (`system.log`) and the console.
    - Sets logging level to DEBUG to capture all logs (INFO, WARNING, ERROR, etc.).
    """
    logging.basicConfig(
        level=logging.DEBUG,  # Logs all levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        format="%(asctime)s [%(levelname)s] %(message)s",  # Standardized log format
        handlers=[
            logging.FileHandler("system.log"),  # Save logs to a file
            logging.StreamHandler()  # Also print logs to the console
        ]
    )
    logging.info("Logger initialized.")  # Logs that the logger is set up


def log_info(message):
    """
    Logs an informational message.

    Args:
        message (str): The message to log.
    """
    logging.info(message)


def log_error(message):
    """
    Logs an error message.

    Args:
        message (str): The error message to log.
    """
    logging.error(message)
