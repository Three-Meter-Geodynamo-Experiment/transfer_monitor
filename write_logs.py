import datetime
import time
import logging

today = (datetime.date.today())
# file_name = "logs/temp" + str(today) + ".log"
logging.basicConfig(filename=file_name)

logging.warning('started the monitoring app')

