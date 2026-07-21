import logging
import sys
from app.core.config import settings

def setup_logging():
    log_level = logging.INFO if settings.ENV == "production" else logging.DEBUG
    
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Disable spammy third-party logs
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("motor").setLevel(logging.WARNING)
    logging.getLogger("pymongo").setLevel(logging.WARNING)
    
    logger = logging.getLogger("crimelens")
    logger.info(f"Logging initialized with level: {logging.getLevelName(log_level)}")
    return logger

logger = setup_logging()
