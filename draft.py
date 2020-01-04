import logging
import datetime

today = str(datetime.date.today())
today = today[5:7] + today[8:10] + today[2:4]
file_name = "logs/pr_temp_" + str(today) + '.log'
logging.basicConfig(filename=file_name, level=logging.DEBUG, format='%(message)s')

now = datetime.datetime.now()
ssm = (now - now.replace(hour=0, minute=0, second=0)).total_seconds()

logging.info(str(ssm) + '\tStarted the monitoring app')
