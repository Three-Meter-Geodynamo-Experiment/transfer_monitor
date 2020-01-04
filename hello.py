from flask import Flask, render_template

import datetime
import time
import multiprocessing
import arduino_connect
import wireless_temp_connect
import logging


data_temp_pressure_array = multiprocessing.Array('d', 12*[-2])

app = Flask(__name__, static_url_path='/static')


@app.route("/")
def index():

    arduino_temp = data_temp_pressure_array[0:4]

    wireless_temp = data_temp_pressure_array[8:12]

    # print(wireless_temp)
    adr_t1 = arduino_temp[0]
    adr_t2 = arduino_temp[1]
    adr_t3 = arduino_temp[2]

    wrls_t1 = wireless_temp[0]
    wrls_t2 = wireless_temp[1]
    wrls_t3 = wireless_temp[2]
    wrls_t4 = wireless_temp[3]

    adr_p1 = '-1'
    adr_p2 = '-1'
    adr_p3 = '-1'

    user = {'adr_temp': arduino_temp, 'wrl_temp': wireless_temp}
    temperatures = {'T1': wrls_t1, 'T2': wrls_t2, 'T3': wrls_t3, 'T4': adr_t1, 'T5': adr_t2, 'T6': adr_t3, 'T7': wrls_t4}
    pressures = {'P1': adr_p1, 'P2': adr_p2, 'P3': adr_p3, }
    return render_template('index.html', title='Home', user=user, temperatures=temperatures, pressures=pressures)


@app.route("/input")
def input():
    return render_template('input.html', title='Input')


def run_the_app():
    app.run('0.0.0.0')


def data_gathering(data_temp_pressure_array=data_temp_pressure_array):
    while True:
        data_temp_pressure_array[0:4] = arduino_connect.arduino_temperatures()
        data_temp_pressure_array[8:12] = wireless_temp_connect.wireless_temp_timed()
        time.sleep(1)


def writing_data_log(data_temp_pressure_array=data_temp_pressure_array):
    while True:
        data = str(data_temp_pressure_array[:]).replace('[', '').replace(']', '').replace(',', '').replace(' ', '\t')
        now = datetime.datetime.now()
        ssm = str((now - now.replace(hour=0, minute=0, second=0)).total_seconds())
        logging.info(ssm + '\t' + data)
        time.sleep(1)


if __name__ == "__main__":
    # process for gathering data
    data_gatherer = multiprocessing.Process(target=data_gathering, args=(data_temp_pressure_array,))
    # defining the app using mp
    app_run = multiprocessing.Process(target=run_the_app)

    app_run.start()
    data_gatherer.start()

    #  THIS PART IS FOR STARTING LOGGER
    today = str(datetime.date.today())
    today = today[5:7] + today[8:10] + today[2:4]
    file_name = "logs/pr_temp_" + str(today) + '.log'
    logging.basicConfig(filename=file_name, level=logging.DEBUG, format='%(message)s')

    now = datetime.datetime.now()
    ssm = (now - now.replace(hour=0, minute=0, second=0)).total_seconds()

    logging.info(str(ssm) + '\tStarted the monitoring app')

    log_process = multiprocessing.Process(target=writing_data_log, args=(data_temp_pressure_array,))
    log_process.start()
    #  this area is unreachable

    app_run.join()
    data_gatherer.join()
    log_process.join()
