import logging
import os
from logging.handlers import RotatingFileHandler

# Ensure logs directory exists
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Log File Configuration
LOG_FILE = os.path.join(LOG_DIR, "app.log")
MAX_LOG_SIZE = 20 * 1024 * 1024  # 20MB max log file size
BACKUP_COUNT = 5  # Keep last 5 logs (app.log.1, app.log.2, etc.)

# Configure Logging with Rotation
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        RotatingFileHandler(
            LOG_FILE, maxBytes=MAX_LOG_SIZE, backupCount=BACKUP_COUNT, encoding="utf-8"
        ),  # Rotating logs
        logging.StreamHandler(),  # Also print logs to console
    ],
)

logger = logging.getLogger(__name__)

# Log rotation test
logger.info("🚀 Logging system initialized. Rotating logs enabled.")
