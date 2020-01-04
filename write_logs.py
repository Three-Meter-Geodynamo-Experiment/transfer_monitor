import datetime
import os.path

def write_log_file():
    today = (datetime.date.today())

    # print(today.strftime('%m%d%y'))

    file_location = "logs/temp" + str(today) + ".log"

    # print(file_location)
    if not os.path.isfile(file_location):
        print('does not exist, creating it')
        log_file = open(file_location, "w+")
    else:
        log_file = open(file_location, "a")

    while True:
        now = datetime.datetime.now()
        seconds_since_midnight = (now - now.replace(hour=0, minute=0, second=0)).total_seconds()

        temperature = [12.1, 34, 43]

        arduino_temp = (arduino_connect.arduino_temperatures())

        wireless_temp = (wireless_temp_connect.wireless_temp_timed())

        d = str(seconds_since_midnight) + ' ' + str(temperature).replace(',', '').replace('[', '').replace(']', '')
        log_file.write(d + '\n')
        print(d)
        time.sleep(2)

    log_file.close()
