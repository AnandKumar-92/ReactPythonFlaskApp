import logging
from datetime import datetime

LOG_FORMAT= "%(asctime)s - %(levelname)s | %(filename)s | %(funcName)s : %(message)s"
logging.basicConfig(filename=f"./logs/log_{datetime.now().date()}_{int(datetime.now().timestamp())}.log",level=logging.DEBUG,format=LOG_FORMAT,filemode='w')
logger=logging.getLogger() 