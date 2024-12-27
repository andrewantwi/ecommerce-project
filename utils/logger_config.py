from loguru import logger
import sys

# Remove the default logger to avoid duplicate logs
logger.remove()

# Add loggers with your preferred configurations
logger.add(
    sys.stdout,
    format="{level}--     {time:YYYY-MM-DD HH:mm:ss} {message}",
    level="INFO",
    colorize=True,
    backtrace=True,  # Shows stack trace for errors
    diagnose=True    # Provides variable values during errors
)
logger.add(
    "logs/app_{time:YYYY-MM-DD}.log",
    rotation="10 MB",  # Rotate log file after it reaches 10 MB
    retention="7 days", # Keep logs for 7 days
    level="INFO",
    compression="zip"   # Compress logs older than retention period
)
