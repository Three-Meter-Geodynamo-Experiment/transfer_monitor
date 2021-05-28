import matplotlib.pyplot as plt
import datetime
import formulas
import time


def infinite_update_plots():
    pos_log_file = 0
    pos_control_file = 0

    time_array = []
    log_data = 18 * []

    time_control_array = []
    control_log_data = 25 * []

    today = str(datetime.date.today())
    today = today[5:7] + today[8:10] + today[2:4]

    while True:

        # getting data from transfer logs

        start_time = time.time()
        file_name = "logs/pr_temp_" + str(today) + '.log'
        f = open(file_name, "r")
        f.seek(pos_log_file)
        for x in f:
            # print(x)
            try:
                line_data = [float(y) for y in x.split()]
                #
                time_array.append(line_data[0])
                log_data.append(line_data)

            except ValueError:
                continue
        # print(time.time() - start_time)

        pos_log_file = f.tell()
        f.close()

        # getting data from control logs

        control_log_filename = '/data/3m/' + today + '/control.log'
        file_control = open(control_log_filename, 'r')
        file_control.seek(pos_control_file)
        for line in file_control:
            try:
                line_data = [float(y) for y in line.split()]
                time_control_array.append(line_data[0])
                control_log_data.append(line_data)
            except ValueError:
                continue

        pos_control_file = file_control.tell()
        file_control.close()
        #

        # pressure plot
        pressure1 = [formulas.pressure_voltage(log_line[7], log_line[11]) if formulas.pressure_voltage(
            log_line[7]) != 666. else None for log_line in log_data]
        pressure2 = [formulas.pressure_voltage(log_line[8], log_line[11]) if formulas.pressure_voltage(
            log_line[8]) != 666. else None for log_line in log_data]
        pressure3 = [formulas.pressure_voltage(log_line[9], log_line[11]) if formulas.pressure_voltage(
            log_line[9]) != 666. else None for log_line in log_data]
        pressure4 = [formulas.pressure_voltage2(log_line[10], log_line[11]) if formulas.pressure_voltage2(
            log_line[10]) != 666. else None for log_line in log_data]

        plt.plot(time_array, pressure1)
        plt.plot(time_array, pressure2)
        plt.plot(time_array, pressure3)
        plt.plot(time_array, pressure4)

        # ymin = min
        # plt.ylim((-15, 30))
        t = time.localtime()
        current_time = time.strftime("%I:%M:%S %p", t)

        plt.title('All day pressure ' + current_time)

        plt.ylabel('Pressure, psi')
        plt.xlabel('Time, SSM')
        plt.legend(['3M probe 1', 'Tank probe 1', 'Tank probe 2', '3M probe 2'])

        plt.savefig('static/pressure_all.png')

        plt.close()

        # second plot here

        plt.plot(time_array[-200:], pressure1[-200:])
        plt.plot(time_array[-200:], pressure2[-200:])
        plt.plot(time_array[-200:], pressure3[-200:])
        plt.plot(time_array[-200:], pressure4[-200:])

        plt.title('Recent pressure ' + current_time)
        plt.ylabel('Pressure, psi')
        plt.xlabel('Time, SSM')
        plt.legend(['3M probe 1', 'Tank probe 1', 'Tank probe 2', '3M probe 2'])

        plt.savefig('static/pressure_recent.png')
        plt.close()
        # plt.show()

        #  now temperature
        temperature1 = [log_line[13] if log_line[13] > 0 else None for log_line in log_data]
        temperature2 = [log_line[14] if log_line[14] > 0 else None for log_line in log_data]
        temperature3 = [log_line[15] if log_line[15] > 0 else None for log_line in log_data]
        temperature4 = [log_line[16] if log_line[16] > 0 else None for log_line in log_data]
        temperature5 = [formulas.temperature_volt(log_line[4], log_line[5]) if
                        log_line[4] > 0 and formulas.temperature_volt(log_line[4], log_line[5]) < 200 else None
                        for log_line in
                        log_data]
        temperature6 = [formulas.temperature_volt(log_line[1], log_line[5]) if
                        log_line[1] > 0 and formulas.temperature_volt(log_line[1], log_line[5]) < 200
                        else None for log_line in
                        log_data]

        plt.plot(time_array, temperature1)
        plt.plot(time_array, temperature2)
        plt.plot(time_array, temperature3)
        plt.plot(time_array, temperature4)
        plt.plot(time_array, temperature5)
        # plt.plot(time_array, temperature6)

        plt.title('All day temperature ' + current_time)
        plt.ylabel('Temperature, C')
        plt.xlabel('Time, SSM')
        plt.legend(['Na port', 'Tank west bottom ', 'Tank bottom port', 'Tank top east', '3M finger', 'Transfer line'])
        plt.savefig('static/temperature_all.png')
        plt.close()

        # last temp
        plt.plot(time_array[-200:], temperature1[-200:])
        plt.plot(time_array[-200:], temperature2[-200:])
        plt.plot(time_array[-200:], temperature3[-200:])
        plt.plot(time_array[-200:], temperature4[-200:])
        plt.plot(time_array[-200:], temperature5[-200:])
        # plt.plot(time_array[-200:], temperature6[-200:])

        plt.title('Recent temperature ' + current_time)
        plt.ylabel('Temperature, C')
        plt.xlabel('Time, SSM')
        plt.legend(['Na port', 'Tank west bottom ', 'Tank bottom port', 'Tank top east', '3M finger', 'Transfer line'])
        plt.savefig('static/temperature_recent.png')
        plt.close()

        # adding control log plots

        temperature_in = [ctr_log_line[5] if ctr_log_line[5] > 0 else None for ctr_log_line in control_log_data]
        temperature_out = [ctr_log_line[8] if ctr_log_line[8] > 0 else None for ctr_log_line in control_log_data]
        temperature_ta = [ctr_log_line[11] if ctr_log_line[11] > 0 else None for ctr_log_line in control_log_data]
        heater_power = [ctr_log_line[4] if ctr_log_line[4] >= 0 else None for ctr_log_line in control_log_data]

        plt.plot(time_control_array, temperature_in)
        plt.plot(time_control_array, temperature_out)
        plt.plot(time_array, temperature3)
        plt.plot(time_control_array, heater_power)

        plt.title('All day power, heater and tank bottom port temperature ' + current_time)
        plt.ylabel('Temperature, C')
        plt.xlabel('Time, SSM')
        plt.legend(['T oil in, C', 'T oil out, C', 'T tank bottom port, C', 'Heater power, %'])
        plt.savefig('static/temperature_heater.png')
        plt.close()

        plt.plot(time_control_array[-600 * 3:], temperature_in[-600 * 3:])
        plt.plot(time_control_array[-600 * 3:], temperature_out[-600 * 3:])
        plt.plot(time_array[-600 * 3:], temperature3[-600 * 3:])
        plt.plot(time_control_array[-600 * 3:], heater_power[-600 * 3:])

        plt.title('Last ten minutes power, heater and tank bottom port temperature ' + current_time)
        plt.ylabel('Temperature, C')
        plt.xlabel('Time, SSM')
        plt.legend(['T oil in, C', 'T oil out, C', 'T tank bottom port, C', 'Heater power, %'])
        plt.savefig('static/temperature_heater_recent.png')
        plt.close()

        time.sleep(3)


if __name__ == '__main__':
    infinite_update_plots()
