import logging
import os
from datetime import datetime

today = datetime.now()
cwd = os.getcwd()
cwd = os.path.split(cwd)[0] + "/Logs/"

try:
    logging.basicConfig(filename=cwd + "/" + today.strftime("%d_%m_%Y_%H_%M_%S") + ".log", level=logging.DEBUG)
except FileNotFoundError as e:
    os.mkdir(cwd)
    logging.basicConfig(filename=cwd + "/" + today.strftime("%d_%m_%Y_%H_%M_%S") + ".log", level=logging.DEBUG)

logger = logging.getLogger(__name__)


def log_print(*arg):
    print(arg)
    logger.info(arg)
