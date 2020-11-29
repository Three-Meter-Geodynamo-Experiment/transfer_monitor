from flask import Flask, render_template, request, send_from_directory, make_response
import os
import datetime
import time
import multiprocessing as mp
import wireless_temp_connect
import logging
import formulas
import pyfirmata2
import draft_plotting

# the multiprocessing array with probes data
data_temp_pressure_array = mp.Array('d', 18*[-2])

progress_data = mp.Array('d', 6*[0])

# defining the app
app = Flask(__name__, static_url_path='/static')
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')


def updating_first_arduino(data_temp_pressure_array=data_temp_pressure_array):
    while True:
        try:
            for chan_ind in range(6):
                data_temp_pressure_array[chan_ind] = 0

            board = pyfirmata2.Arduino('/dev/tty.usbmodem14201')
            board.samplingOn(100)
            analog_0 = board.get_pin('a:0:i')
            analog_1 = board.get_pin('a:1:i')
            analog_2 = board.get_pin('a:2:i')
            analog_3 = board.get_pin('a:3:i')
            analog_4 = board.get_pin('a:4:i')
            analog_5 = board.get_pin('a:5:i')
            time.sleep(0.5)
            while True:
                try:
                    data_temp_pressure_array[0] = float(analog_0.read())
                    data_temp_pressure_array[1] = float(analog_1.read())
                    data_temp_pressure_array[2] = float(analog_2.read())
                    data_temp_pressure_array[3] = float(analog_3.read())
                    data_temp_pressure_array[4] = float(analog_4.read())
                    data_temp_pressure_array[5] = float(analog_5.read())
                    # print(analog_0.read())
                    time.sleep(1)
                    board.digital[13].write(1)
                    board.digital[13].write(0)
                except TypeError:
                    print('trying again Ard 1')
                    time.sleep(1)
                    continue

        except:
            print('Something is wrong, connecting Arduino 1 again')
            time.sleep(1)
            continue


def updating_second_arduino(data_temp_pressure_array=data_temp_pressure_array):
    while True:
        try:
            for chan_ind in range(6, 12):
                data_temp_pressure_array[chan_ind] = 0

            board = pyfirmata2.Arduino('/dev/tty.usbmodem14101')
            board.samplingOn(100)
            analog_0 = board.get_pin('a:0:i')
            analog_1 = board.get_pin('a:1:i')
            analog_2 = board.get_pin('a:2:i')
            analog_3 = board.get_pin('a:3:i')
            analog_4 = board.get_pin('a:4:i')
            analog_5 = board.get_pin('a:5:i')
            time.sleep(0.501)
            while True:
                try:
                    data_temp_pressure_array[6] = float(analog_0.read())
                    data_temp_pressure_array[7] = float(analog_1.read())
                    data_temp_pressure_array[8] = float(analog_2.read())
                    data_temp_pressure_array[9] = float(analog_3.read())
                    data_temp_pressure_array[10] = float(analog_4.read())
                    data_temp_pressure_array[11] = float(analog_5.read())
                    # print(analog_0.read())
                    time.sleep(1)
                    board.digital[13].write(1)
                    board.digital[13].write(0)
                except TypeError:
                    print('trying again Ard2')
                    time.sleep(1)
                    continue

        except:
            print('Something is wrong, connecting Arduino 2 again')
            time.sleep(1)
            continue


# the main page
@app.route("/")
def index():
    # gathering data from the multiprocessing array
    arduino_temp = [formulas.temperature_volt(x) for x in data_temp_pressure_array[0:6]]
    arduino_pressure = [formulas.pressure_voltage(x) for x in data_temp_pressure_array[6:12]]
    wireless_temp = data_temp_pressure_array[12:18]

    # print(wireless_temp)
    adr_t1 = arduino_temp[0]
    adr_t2 = arduino_temp[1]
    adr_t3 = arduino_temp[2]

    wrls_t1 = wireless_temp[0]
    wrls_t2 = wireless_temp[1]
    wrls_t3 = wireless_temp[2]
    wrls_t4 = wireless_temp[3]

    adr_p1 = arduino_pressure[0]
    adr_p2 = arduino_pressure[1]
    adr_p3 = arduino_pressure[2]
    adr_p4 = arduino_pressure[3]

    # setting up time
    t = time.localtime()
    current_time = time.strftime("%I:%M %p", t)

    current_ssm = (datetime.datetime.now() - datetime.datetime.now().replace(hour=0, minute=0, second=0)).total_seconds()

    # NEEDS TO BE FIXED
    if progress_data[0] == 0:
        time_since_started_str = '00:00:00'
    else:
        time_since_started = round(current_ssm - progress_data[0])
        time_since_started_str = str(datetime.timedelta(seconds=time_since_started).total_seconds())

    if progress_data[0] == 0:
        time_since_updated = 0
    else:
        time_since_updated = str(datetime.timedelta(seconds=round(current_ssm - progress_data[2])).total_seconds())

    # creating the array of times for giving it to the page
    time_data = {'current_time': current_time, 'since_started': time_since_started_str,
                 'since_updated': time_since_updated}

    if progress_data[1] == 0:
        percents_done = 0
        current_flux = 0
        average_flux = 0
        eta = 0
    else:
        try:
            percents_done = round(100 * (1 - formulas.remaining_volume(0.001*progress_data[3])/formulas.remaining_volume(0.001*progress_data[1])), 1)
        except ZeroDivisionError:
            percents_done = 0
        current_flux = round(1000*progress_data[4], 1)
        average_flux = round(1000*progress_data[5], 1)
        if progress_data[4] > 0:
            eta = datetime.timedelta(seconds=formulas.remaining_volume(0.001*progress_data[3])/progress_data[4])
            eta = str(eta - datetime.timedelta(microseconds=eta.microseconds))
        else:
            eta = -1

    progress_data_web = {'percents_done': percents_done,
                         'current_flux': current_flux, 'average_flux': average_flux, 'eta': eta}

    user = {'ard_temp': arduino_temp, 'wrl_temp': wireless_temp, 'ard2_pres': arduino_pressure}
    temperatures = {'T1': wrls_t1, 'T2': wrls_t2, 'T3': wrls_t3, 'T4': adr_t1, 'T5': adr_t2, 'T6': adr_t3, 'T7': wrls_t4}
    pressures = {'P1': adr_p1, 'P2': adr_p2, 'P3': adr_p3, 'P4': adr_p4, 'diff': round(adr_p1-adr_p3, 2)}
    return render_template('index.html', title='Home', user=user, temperatures=temperatures,
                           pressures=pressures, time_data=time_data, progress=progress_data_web)


def run_the_app():
    app.run(host='0.0.0.0', port=80)


def data_gathering(data_temp_pressure_array=data_temp_pressure_array):
    while True:
        # checking every second for the data from the probes
        data_temp_pressure_array[12:18] = wireless_temp_connect.wireless_temp_timed()
        time.sleep(1)


def writing_data_log(data_temp_pressure_array=data_temp_pressure_array):
    while True:
        data = str(data_temp_pressure_array[:]).replace('[', '').replace(']', '').replace(',', '').replace(' ', '\t')
        now = datetime.datetime.now()
        ssm = str((now - now.replace(hour=0, minute=0, second=0)).total_seconds())
        logger.info(ssm + '\t' + data)
        time.sleep(3)


def setup_logger(name, log_file, level=logging.INFO):
    """To setup as many loggers as you want"""

    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger


@app.route("/input")
def input_height():
    return render_template('my-form.html', title='Input')


@app.route("/plot_pressure")
def plot_pressure():
    r = make_response(render_template('plot_pressure.html'))
    r.headers['Cache-Control'] = 'public, no-store, no-cache, max-age=0'
    return r


@app.route("/plot_temperature")
def plot_temperature():
    r = make_response(render_template('plot_temperature.html'))
    r.headers['Cache-Control'] = 'public, no-store, no-cache, max-age=0'
    return r


@app.route("/plot_recent")
def plot_recent():
    r = make_response(render_template('plot_data.html'))
    r.headers['Cache-Control'] = 'public, no-store, no-cache, max-age=0'
    return r


@app.route("/debug")
def debug():
    return render_template('debug.html')


@app.route('/input', methods=['POST'])
def my_form_post(progress_data=progress_data):
    text = request.form['text']
    try:
        processed_text = float(text)
    except ValueError:
        return 'Not a number, try again'

    now = datetime.datetime.now()
    ssm = (now - now.replace(hour=0, minute=0, second=0)).total_seconds()
    # writing the progress data to the log file
    progress_logger.info(str(ssm) + '\t' + str(processed_text) + '\t' + str(formulas.remaining_volume(processed_text/1000)))

    update_progress()

    return render_template('my-form.html', title='Input')


def update_progress():
    log2_file = open(file_name2, 'r')

    lines = 0
    ssm_array = []
    height_array = []

    for line in log2_file:
        # print(float(line.split()[0]))
        ssm_array.append(float(line.split()[0]))
        height_array.append(float(line.split()[1]))

        if lines > 0 and progress_data[0] == 0:  # checking if starting time was not defined yet
            if height_array[lines] > 1 + height_array[lines - 1]:
                print('found the beginning, ' + str(ssm_array[lines - 1]))
                progress_data[0] = ssm_array[lines - 1]
                progress_data[1] = height_array[lines - 1]

        progress_data[2] = ssm_array[lines]
        progress_data[3] = height_array[lines]

        if lines > 0:
            volume_drop = formulas.remaining_volume(0.001 * height_array[lines - 1]) - formulas.remaining_volume(
                0.001 * height_array[lines])
            volume_change = formulas.remaining_volume(0.001 * progress_data[1]) - formulas.remaining_volume(
                0.001 * height_array[lines])
            time_step = ssm_array[lines] - ssm_array[lines - 1]
            time_change = ssm_array[lines] - progress_data[0]

            if time_step > 1:
                progress_data[4] = volume_drop / time_step
            if time_change > 1:
                progress_data[5] = volume_change / time_change

        lines += 1

    log2_file.close()
    # print(progress_data[:])


@app.route('/progress')
def progress_page():
    file_object = open(file_name2, "r")
    progress_file_data = file_object.read()
    file_object.close()
    return progress_file_data


if __name__ == "__main__":
    print('Starting the app')
    # process for gathering data
    data_gatherer = mp.Process(target=data_gathering, args=(data_temp_pressure_array,))
    first_arduino = mp.Process(target=updating_first_arduino, args=(data_temp_pressure_array,))
    second_arduino = mp.Process(target=updating_second_arduino, args=(data_temp_pressure_array,))

    # defining the app using mp
    app_run = mp.Process(target=run_the_app)

    #  THIS PART IS FOR STARTING LOGGER
    today = str(datetime.date.today())
    today = today[5:7] + today[8:10] + today[2:4]
    file_name = "logs/pr_temp_" + str(today) + '.log'
    file_name2 = "logs/progress_" + str(today) + '.log'

    formatter = logging.Formatter('%(message)s')

    # logging.basicConfig(filename=file_name, level=logging.DEBUG, format='%(message)s')
    logger = setup_logger('first_logger', file_name)

    progress_logger = setup_logger('progress_log', file_name2)

    now = datetime.datetime.now()
    ssm = (now - now.replace(hour=0, minute=0, second=0)).total_seconds()

    logger.info(str(ssm) + '\tStarted the monitoring app')
    log_process = mp.Process(target=writing_data_log, args=(data_temp_pressure_array,))
    log_process.start()

    #
    update_plots = mp.Process(target=draft_plotting.infinite_update_plots, args=())

    #  Here we start the apps
    app_run.start()
    data_gatherer.start()
    first_arduino.start()
    second_arduino.start()
    update_plots.start()

    update_progress()
    print('started everything')
    #  this area is unreachable

    app_run.join()
    data_gatherer.join()
    log_process.join()
    first_arduino.join()
    second_arduino.join()
