from math import pi


def temperature_volt(arduino_signal, v33=3.38/5):
    # print('v33= ', v33)
    if v33 < 0.1:
        v33 = 3.38/5
    return round(5*32*arduino_signal*3.38/5/v33, 2)


def pressure_voltage(arduino_signal, v33=3.3/5):
    if v33 < 0.1:
        v33 = 3.3/5
    # print(arduino_signal)
    # print('v33= ', v33)
    pressure = 44.7/4*(5*arduino_signal*3.3/5/v33-1) - 14.7
    if arduino_signal < 1/5:
        return 666
    return round(pressure, 3)


def pressure_voltage2(arduino_signal, v33=3.3/5):
    if v33 < 0.1:
        v33 = 3.3/5
    pressure = 15/4*(5*arduino_signal*3.3/5/v33-1)
    if arduino_signal < 1/5:
        return 666
    return round(pressure, 3)


def remaining_volume(measurement):
    dx = 0.3
    x = measurement - dx
    R = 1.46
    r = 0.52
    d = R-r
    a = 2*0.05

    if measurement < dx or measurement > dx+2*R:
        return 0

    volume_total = 4./3*pi*(R**3-r**3) - 2*pi*a**2*d
    if x < d:
        volume = volume_total - pi/3*x**2*(3*R-x) + pi*a**2*x
    elif d <= x < d + 2*r:
        volume = volume_total - pi/3*x**2*(3*R-x) + pi*a**2*d + pi/3*(x-d)**2*(3*r - (x-d))
    else:
        volume = volume_total - pi/3*x**2*(3*R-x) + pi*a**2*d + 4./3*pi*r**3 + pi*a**2*(x-2*r-d)
    return volume


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    print(remaining_volume(0.1))
    amount_of_points = 300
    dx = 0.2
    R = 1.46
    measure_array = [dx + x*(2*R-dx)/amount_of_points for x in range(amount_of_points+1)]

    volume_array = [remaining_volume(measure) for measure in measure_array]
    print([x/2/1.46 for x in measure_array])
    print(volume_array)

    fig = plt.scatter(measure_array, volume_array)


    dv_array = [volume_array[i] - volume_array[i+1] for i in range(len(volume_array)-1)]
    # fig2 = plt.scatter(measure_array[0:-1], dv_array)

    plt.show()
    # plt.show(fig2)

