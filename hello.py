from flask import Flask, render_template
import arduino_connect
import wireless_temp_connect
import datetime
import os.path
import time
import multiprocessing


def write_log_file():
    print('Starting writing log file')
    # time.sleep(10)
    today = (datetime.date.today())
    file_location = "logs/temp" + str(today) + ".log"
    if not os.path.isfile(file_location):
        print('does not exist, creating it')
        log_file = open(file_location, "w+")
    else:
        log_file = open(file_location, "a")

    while True:
        now = datetime.datetime.now()
        seconds_since_midnight = (now - now.replace(hour=0, minute=0, second=0)).total_seconds()


        arduino_temp = (arduino_connect.arduino_temperatures())

        wireless_temp = (wireless_temp_connect.wireless_temp_timed())

        d = str(seconds_since_midnight) + ' ' + str(arduino_temp).replace(',', '').replace('[', '').replace(']', '') + ' ' + str(wireless_temp).replace(',', '').replace('[', '').replace(']', '')
        log_file.write(d.replace(' ', '\t') + '\n')
        # print(d)
        time.sleep(2)

    log_file.close()


app = Flask(__name__, static_url_path='/static')


@app.route("/")
def index():

    arduino_temp = (arduino_connect.arduino_temperatures())

    wireless_temp = (wireless_temp_connect.wireless_temp_timed())
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


if __name__ == "__main__":
    # defining the app using mp
    p2 = multiprocessing.Process(target=run_the_app)
    # defining writing log files using mp
    p3 = multiprocessing.Process(target=write_log_file)
    #  starting both processes
    p3.start()
    p2.start()

    # this one is unreachable, sorry
    p2.join()
    p3.join()
