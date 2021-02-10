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
import serial
from pymodbus.client.sync import ModbusSerialClient as ModbusClient


# the multiprocessing array with probes data
data_temp_pressure_array = mp.Array('d', 18*[-2])
# the array of data for writing control.log
data_control_log_array = mp.Array('d', 24*[0])
data_control_log_array[23] = 0  # this one is requested heater power
# the array of the progress data
progress_data = mp.Array('d', 6*[0])
# devices connection requests
devices_connect = mp.Array('i', [1, 1, 1, 1, 0])
# set to zero if don't want to connect
# devices_connect[0] - Arduino
# devices_connect[1] - ADAM
# devices_connect[2] - MAPLE
# devices_connect[3] - wireless temp
# devices_connect[4] - MODBUS

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

            board = pyfirmata2.Arduino('/dev/ard_temp')
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
                    # print([round(5*x, 3) for x in data_temp_pressure_array[0:6]])

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

            board = pyfirmata2.Arduino('/dev/ard_pres')
            board.samplingOn(100)
            analog_0 = board.get_pin('a:0:i')
            analog_1 = board.get_pin('a:1:i')
            analog_2 = board.get_pin('a:2:i')
            analog_3 = board.get_pin('a:3:i')
            analog_4 = board.get_pin('a:4:i')
            analog_5 = board.get_pin('a:5:i')
            time.sleep(0.015011)
            while True:
                try:
                    data_temp_pressure_array[6] = float(analog_0.read())
                    data_temp_pressure_array[7] = float(analog_1.read())
                    data_temp_pressure_array[8] = float(analog_2.read())
                    data_temp_pressure_array[9] = float(analog_3.read())
                    data_temp_pressure_array[10] = float(analog_4.read())
                    data_temp_pressure_array[11] = float(analog_5.read())
                    # print('pressure ard signal')
                    # print([round(5*x, 3) for x in data_temp_pressure_array[10:11]])
                    time.sleep(1)
                    board.digital[13].write(1)
                    board.digital[13].write(0)
                except TypeError:
                    print('trying again Ard2 (pres)')
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
    reading_from_ard1_A4 = [x for x in data_temp_pressure_array[4:5]]
    # print('first Ard 0.66 = ', reading_from_ard1_A5)
    # print(round(32*data_temp_pressure_array[0]*3.3/reading_from_ard1_A4[0], 1),
    #       round(5*data_temp_pressure_array[0]*3.3/5/reading_from_ard1_A4[0], 3),
    #       round(reading_from_ard1_A4[0], 3), round(reading_from_ard1_A4[0]*5, 3))

    arduino_temp = [formulas.temperature_volt(x, reading_from_ard1_A4[0]) for x in data_temp_pressure_array[0:6]]
    # print(arduino_temp[0], arduino_temp[0]/32)
    reading_from_ard2_A4 = [x for x in data_temp_pressure_array[10:11]]
    # print('second Ard 0.66 = ', reading_from_ard2_A4)

    arduino_pressure = [formulas.pressure_voltage(x, reading_from_ard2_A4[0]) for x in data_temp_pressure_array[6:12]]
    arduino_pressure[3] = formulas.pressure_voltage2(data_temp_pressure_array[9], reading_from_ard2_A4[0])  #  adding second type of the pressure probe

    wireless_temp = data_temp_pressure_array[12:18]

    # print(wireless_temp)
    adr_t1 = int(arduino_temp[0])
    adr_t2 = int(arduino_temp[1])
    adr_t3 = int(arduino_temp[2])
    adr_t4 = int(arduino_temp[3])

    wrls_t1 = int(wireless_temp[0])
    wrls_t2 = int(wireless_temp[1])
    wrls_t3 = int(wireless_temp[2])
    wrls_t4 = int(wireless_temp[3])

    adr_p1 = round(arduino_pressure[0], 1)
    adr_p2 = round(arduino_pressure[1], 1)
    adr_p3 = round(arduino_pressure[2], 1)
    adr_p4 = round(arduino_pressure[3], 1)
    # print(*arduino_pressure[0:4])

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
    if adr_p3 > 600 or adr_p2 > 600:
        p_tank = min(adr_p3, adr_p2)
    else:
        p_tank = (adr_p3 + adr_p2)/2

    p_difference = round(adr_p1-p_tank, 2)
    user = {'ard_temp': arduino_temp, 'wrl_temp': wireless_temp, 'ard2_pres': arduino_pressure}
    temperatures = {'T1': wrls_t1, 'T2': wrls_t2, 'T3': wrls_t3, 'T4': adr_t1, 'T5': adr_t2, 'T6': adr_t3, 'T7': wrls_t4, 'T8': adr_t4}
    pressures = {'P1': adr_p1, 'P2': adr_p2, 'P3': adr_p3, 'P4': adr_p4, 'diff': p_difference}
    return render_template('index.html', title='Home', user=user, temperatures=temperatures,
                           pressures=pressures, time_data=time_data, progress=progress_data_web)


def run_the_app():
    app.run(host='0.0.0.0', port=2020)


def data_gathering(data_temp_pressure_array=data_temp_pressure_array):
    while True:
        # checking every second for the data from the probes
        data_temp_pressure_array[12:18] = wireless_temp_connect.wireless_temp_timed()
        time.sleep(1)


def data_control_gathering(data_control_log_array=data_control_log_array):
    # connect the Arduino, Maple, Adam, modbus, and ADAM

    # just lest wait a couple seconds to start comms
    time.sleep(0.2)
    # devices_connect

    # connectind ADAM
    if devices_connect[1]:
        # connecting to ADAM for getting heater temperatures
        serial_arg = dict(port='/dev/ttyS1',
                          baudrate=9600,
                          stopbits=serial.STOPBITS_ONE,
                          parity=serial.PARITY_NONE,
                          bytesize=serial.EIGHTBITS,
                          timeout=0.03)
        adam_ser = None
        try:
            if adam_ser:
                adam_ser.close()
            adam_ser = serial.Serial(**serial_arg)
            print('ADAM is connected')
        except serial.SerialException as e:
            print(e)

    # now connecting MAPLE
    if devices_connect[2]:
        serial_arg = dict(port='/dev/maple',
                          baudrate=115200,
                          stopbits=serial.STOPBITS_ONE,
                          parity=serial.PARITY_NONE,
                          bytesize=serial.EIGHTBITS)
        maple_ser = None

        try:
            if maple_ser:
                maple_ser.close()
            maple_ser = serial.Serial(**serial_arg)
            print('MAPLE connected')
            # time.sleep(1)
        except serial.SerialException as e:
            print(e)

    # and just getting the Na temperature from wireless_temp_connect.wireless_temp_timed()
    # if connecting_devices[3]:

    # and the modbus connections
    # if connecting_devices[4]:


    # lest wait a bit and start
    time.sleep(2)

    while True:
        # data_control_log_array[0:23] = 23*[0]

        # working on the ADAM updates
        if devices_connect[1]:
            adam_ser.write('#015\r'.encode())     # reads sphere inlet temp
            time.sleep(0.03)
            sp_in_t = adam_ser.read(1)
            sp_in_t += adam_ser.read(adam_ser.inWaiting())

            adam_ser.write('#013\r'.encode())     # reads sphere outlet temp
            time.sleep(0.03)
            sp_out_t = adam_ser.read(1)
            sp_out_t += adam_ser.read(adam_ser.inWaiting())

            adam_ser.write('#014\r'.encode())     # reads the heater temperature
            time.sleep(0.03)
            heat_t = adam_ser.read(1)
            heat_t += adam_ser.read(adam_ser.inWaiting())

            data_control_log_array[4] = float(sp_in_t.decode().strip('>+\r'))
            data_control_log_array[7] = float(sp_out_t.decode().strip('>+\r'))
            data_control_log_array[2] = float(heat_t.decode().strip('>+\r'))
        # Maple
        if devices_connect[2]:
            maple_data = maple_ser.read(1)
            maple_data += maple_ser.read(maple_ser.inWaiting())

            if '\r\n' in maple_data.decode():
                maple_lines = maple_data.decode().splitlines()
                # print(maple_lines)
                second_to_last_line = [int(x) for x in maple_lines[-2].split()]
                if len(second_to_last_line) == 4:
                    data_control_log_array[6] = round(second_to_last_line[0] * 0.03085 - 13.02, 3)
                    data_control_log_array[5] = round(second_to_last_line[1] * 0.03085 - 13.02, 3)
                    data_control_log_array[8] = round(second_to_last_line[3] * 0.03085 - 13.02, 3)
                    data_control_log_array[9] = round(second_to_last_line[2] * 0.03085 - 13.02, 3)
        # wireless temp
        if devices_connect[3]:
            data_control_log_array[1] = data_temp_pressure_array[13]
        # Modbus, unit = 3 - heater
        # if connecting_devices[4]:
            # print(mobucon.read_holding_registers(159, 1, unit=3).getRegister(0)/10)


        time.sleep(0.1)


def writing_data_log(data_temp_pressure_array=data_temp_pressure_array):
    while True:
        data = str(data_temp_pressure_array[:]).replace('[', '').replace(']', '').replace(',', '').replace(' ', '\t')
        now = datetime.datetime.now()
        ssm = str((now - now.replace(hour=0, minute=0, second=0)).total_seconds())
        logger.info(ssm + '\t' + data)
        time.sleep(3)


def writing_control_log(data_control_log_array=data_control_log_array):
    # waiting a bit till everything is connected
    time.sleep(5)
    while True:
        data_control_log = str(data_control_log_array[:]).replace('[', '').replace(']', '').replace(',', '').replace(' ', '\t');
        now = datetime.datetime.now()
        ssm = str((now - now.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds())
        control_logger.info(ssm + '\t' + data_control_log)
        time.sleep(0.5)


def setup_logger(name, log_file, level=logging.INFO):
    """To setup as many loggers as you want"""

    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    if name == 'control_log':
        try:
            os.chmod(log_file, 0o777)
        except PermissionError:
            print('File already was created by someone else')

    return logger


@app.route("/input")
def input_height():
    return render_template('input-form.html', title='Input')


@app.route("/heater")
def input_heater():
    return render_template('heater.html', title='Heater input')


@app.route("/heater_table_plots")
def heater_table_plots():
    t = time.localtime()
    current_time = time.strftime("%I:%M %p", t)
    heater_data = {'time': current_time, 'power': data_control_log_array[3], 'temp_oil_in': data_control_log_array[4],
                   'temp_oil_out': data_control_log_array[7], 'temp_heater': data_control_log_array[2],
                   'pressure_in': data_control_log_array[6], 'pressure_out': data_control_log_array[5],
                   'pressure_pump': data_control_log_array[8], 'temp_na': data_temp_pressure_array[13]}
    return render_template('heater_table_plots.html', heater_data=heater_data)


@app.route('/links')
def add_links():
    return render_template('links.html')


def buttons_state():
    if devices_connect[4] == 0:
        buttons_state = {'connect': 'Yes', 'turn_off': 'none', 'disconnect': 'none'}
    else:
        buttons_state = {'connect': 'none', 'turn_off': 'Yes', 'disconnect': 'Yes'}
    return buttons_state


@app.route('/heater_input_form')
def heater_input_form():

    return render_template('heater_input_form.html', buttons_state=buttons_state())


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

    return render_template('input-form.html', title='Input')


@app.route('/heater_input_form', methods=['POST'])
def heater_post():

    if request.method == 'POST':
        if request.remote_addr != '128.8.86.195':
            return 'Control is only possible from Sodium computer'

        page_respond = request.form
        # print(page_respond)

        if 'turn_off_heater' in page_respond:
            data_control_log_array[23] = 0
            return render_template('heater_input_form.html', buttons_state=buttons_state())
        elif 'connect_heater' in page_respond:
            devices_connect[4] = 1
            return render_template('heater_input_form.html', buttons_state=buttons_state())
        elif 'disconnect_heater' in page_respond:
            devices_connect[4] = 0
            return render_template('heater_input_form.html', buttons_state=buttons_state())

        if devices_connect[4] == 0:
            return 'MODBUS is not connected'
        power_txt = page_respond['heater_form']
        try:
            power = float(power_txt)
            if power < 0 or power > 100:
                return 'should be between 0 and 100'
        except ValueError:
            return 'Not a number, try again'

        data_control_log_array[23] = power

        return render_template('heater_input_form.html', buttons_state=buttons_state())


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


def make_modbus_connection():
    mobucon = ModbusClient(
        port='/dev/ttyS0',
        stopbits=1,
        bytesize=8,
        parity='N',
        baudrate=19200,
        method='rtu',
        timeout=0.07)
    return mobucon


def update_modbus(devices_connect=devices_connect, data_control_log_array=data_control_log_array):
    # this cycle connects to MODBUS every once in a while and checks it, also updates the values on the heater
    while True:
        if devices_connect[4] == 1:
            try:
                power = data_control_log_array[23]
                mobucon.write_register(5102, int(10.0 * power), unit=3)
            except NameError or AttributeError:
                mobucon = make_modbus_connection()
                mobucon.connect()
                print('Modbus connected, CHOO-CHOO')

            if not mobucon.connect():
                print('Modbus_disconnected, trying again')
                mobucon = make_modbus_connection()
                mobucon.connect()
                print('Modbus connected again, CHOO-CHOO')
            try:
                # print(mobucon.read_holding_registers(159, 1, unit=3).getRegister(0)/10)
                # time.sleep(0.05)
                data_control_log_array[3] = mobucon.read_holding_registers(159, 1, unit=3).getRegister(0) / 10
            except AttributeError:
                print('error with modbus communication')
                data_control_log_array[3] = 0
        else:
            # if we are not talking to MAPLE set up the desirable power back to zero
            data_control_log_array[23] = 0
            try:
                mobucon.write_register(5102, int(0), unit=3)
                mobucon.close()
            except NameError:
                pass

        time.sleep(0.1)


if __name__ == "__main__":
    print('Starting the app')

    # create a modbus connection if it's requested by default
    # if devices_connect[4] == 1:
    #     mobucon = make_modbus_connection()
    #     mobucon.connect()

    # process for gathering data
    data_gatherer = mp.Process(target=data_gathering, args=(data_temp_pressure_array,))
    first_arduino = mp.Process(target=updating_first_arduino, args=(data_temp_pressure_array,))
    second_arduino = mp.Process(target=updating_second_arduino, args=(data_temp_pressure_array,))
    control_data_gatherer = mp.Process(target=data_control_gathering, args=(data_control_log_array,))
    update_modbus_process = mp.Process(target=update_modbus, args=(devices_connect, data_control_log_array, ))

    # defining the app using mp
    app_run = mp.Process(target=run_the_app)

    #  THIS PART IS FOR STARTING LOGGER
    today = str(datetime.date.today())
    today = today[5:7] + today[8:10] + today[2:4]
    file_name = "logs/pr_temp_" + str(today) + '.log'
    file_name2 = "logs/progress_" + str(today) + '.log'

    # making the today's directory in /data/3m
    control_log_path = '/data/3m/' + str(today)
    if not os.path.isdir(control_log_path):
        os.mkdir(control_log_path)
        os.chmod(control_log_path, 0o777)
    file_name_logger = '/data/3m/' + str(today) + '/control.log'

    formatter = logging.Formatter('%(message)s')

    # main logger for the transfer data
    logger = setup_logger('first_logger', file_name)
    # progress logger
    progress_logger = setup_logger('progress_log', file_name2)
    #
    control_logger = setup_logger('control_log', file_name_logger)

    now = datetime.datetime.now()
    ssm = (now - now.replace(hour=0, minute=0, second=0)).total_seconds()

    # writing one line and starting the log process
    logger.info(str(ssm) + '\tStarted the monitoring app')
    log_process = mp.Process(target=writing_data_log, args=(data_temp_pressure_array,))
    log_process.start()

    # starting control log process
    control_log_process = mp.Process(target=writing_control_log, args=(data_control_log_array,))
    control_log_process.start()

    # the process to make plots
    update_plots = mp.Process(target=draft_plotting.infinite_update_plots, args=())

    #  Here we start the apps
    app_run.start()
    # print('PEW PEW PEW')
    data_gatherer.start()
    control_data_gatherer.start()
    first_arduino.start()
    second_arduino.start()
    update_plots.start()
    update_modbus_process.start()

    update_progress()
    print('started everything')

    #  this area is unreachable

    app_run.join()
    data_gatherer.join()
    log_process.join()
    first_arduino.join()
    second_arduino.join()
    update_plots.join()
    update_modbus_process.join()
