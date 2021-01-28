import matplotlib.pyplot as plt
import datetime
import formulas
import time


def update_from_logs_and_plot():
    time_array = []
    log_data = 18*[]

    today = str(datetime.date.today())
    today = today[5:7] + today[8:10] + today[2:4]
    file_name = "logs/pr_temp_" + str(today) + '.log'


    f = open(file_name, "r")

    for x in f:
        # print(x)
        try:
            line_data = [float(y) for y in x.split()]
            #
            # if line_data[0] < 1*3600:
            #     line_data[0] += 24*3600

            time_array.append(line_data[0])
            log_data.append(line_data)
        except ValueError:
            continue

    f.close()

    # print(time_array[-1])
    # print(len(line_data))

    # print(log_data[-1])
    # t = range(10)
    # y = [t_i**2 for t_i in t]


    # pressure plot
    pressure1 = [formulas.pressure_voltage(log_line[7]) if formulas.pressure_voltage(log_line[7]) != 666. else None for log_line in log_data]
    pressure2 = [formulas.pressure_voltage(log_line[8]) if formulas.pressure_voltage(log_line[8]) != 666. else None for log_line in log_data]
    pressure3 = [formulas.pressure_voltage(log_line[9]) if formulas.pressure_voltage(log_line[9]) != 666. else None for log_line in log_data]
    pressure4 = [formulas.pressure_voltage2(log_line[10]) if formulas.pressure_voltage2(log_line[10]) != 666. else None for log_line in log_data]

    plt.plot(time_array, pressure1)
    plt.plot(time_array, pressure2)
    plt.plot(time_array, pressure3)
    plt.plot(time_array, pressure4)

    # ymin = min
    # plt.ylim((-15, 30))
    t = time.localtime()
    current_time = time.strftime("%I:%M:%S %p", t)

    plt.title('All day pressure '+current_time)

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


    plt.title('Recent pressure '+current_time)
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
    temperature5 = [formulas.temperature_volt(log_line[4]) if log_line[4] > 0 else None for log_line in log_data]
    temperature6 = [formulas.temperature_volt(log_line[1]) if log_line[1] > 0 else None for log_line in log_data]

    plt.plot(time_array, temperature1)
    plt.plot(time_array, temperature2)
    plt.plot(time_array, temperature3)
    plt.plot(time_array, temperature4)
    plt.plot(time_array, temperature5)
    plt.plot(time_array, temperature6)


    plt.title('All day temperature '+current_time)

    plt.ylabel('Temperature, C')
    plt.xlabel('Time, SSM')
    plt.legend(['Na port', 'Top 3M', 'Bottom 3M', 'Tank', '3M finger', 'Transfer line'])


    plt.savefig('static/temperature_all.png')

    plt.close()

    # last temp

    plt.plot(time_array[-200:], temperature1[-200:])
    plt.plot(time_array[-200:], temperature2[-200:])
    plt.plot(time_array[-200:], temperature3[-200:])
    plt.plot(time_array[-200:], temperature4[-200:])
    plt.plot(time_array[-200:], temperature5[-200:])
    plt.plot(time_array[-200:], temperature6[-200:])


    plt.title('Recent temperature '+current_time)

    plt.ylabel('Temperature, C')
    plt.xlabel('Time, SSM')
    plt.legend(['Na port', 'Top 3M', 'Bottom 3M', 'Tank', '3M finger', 'Transfer line'])

    plt.savefig('static/temperature_recent.png')

    plt.close()

    # print(len(log_data[0]))
    # print([log_line[16] for log_line in log_data])


def infinite_update_plots():
    while True:
        update_from_logs_and_plot()
        time.sleep(3)


if __name__ == '__main__':
    update_from_logs_and_plot()
    # infinite_update_plots()
