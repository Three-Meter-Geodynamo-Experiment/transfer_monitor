import serial
import time
# import arduino_connect

ser1 = serial.Serial('/dev/tty.usbmodem14101', 9700)
# ser2 = serial.Serial('/dev/tty.usbmodem14201', 9600)

while True:
    value = ser1.readline()[0:-2].decode("utf-8")
    data = [1/1023*float(x) for x in value.split()]
    print(*[round(x, 2) for x in data])

    # print(arduino_connect.arduino_temperatures())
    # value = ser2.readline()[0:-2].decode("utf-8")
    # data = [1/1023*float(x) for x in value.split()]
    # print(*[round(x, 2) for x in data])

    time.sleep(1.5)
