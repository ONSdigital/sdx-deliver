import os
import structlog

from app import cloud_config

logger = structlog.get_logger()


if __name__ == '__main__':
    logger.info('Starting SDX Deliver')
    cloud_config()
    os.system("uvicorn app.routes:app --host 0.0.0.0 --port 5000 --workers 2")
