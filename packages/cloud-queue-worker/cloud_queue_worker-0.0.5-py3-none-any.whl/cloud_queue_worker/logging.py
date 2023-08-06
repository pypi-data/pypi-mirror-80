from logging import basicConfig, getLogger
from os import getenv


basicConfig(
    format="[%(levelname)s]: %(message)s",
    level=getenv("CLOUD_QUEUE_WORKER_ENV") or "INFO"
)


logger = getLogger("cloud_queue_worker")
