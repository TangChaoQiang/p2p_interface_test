from app import init_log_config
import logging

init_log_config()
logging.info("info")
logging.error("error")
logging.critical("critical")
logging.debug("debug")