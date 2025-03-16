import logging
from functools import wraps

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def log_function(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Log function start
        logger.info(f"Running function: {func.__name__} with args: {args} kwargs: {kwargs}")
        result = func(*args, **kwargs)  # Execute the function
        # Log function completion
        logger.info(f"Function {func.__name__} completed.")
        return result
    return wrapper