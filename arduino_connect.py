import pyfirmata
import time

board = pyfirmata.Arduino('/dev/tty.usbmodem14201')

it = pyfirmata.util.Iterator(board)
it.start()

V0 = board.get_pin('a:0:i')
V1 = board.get_pin('a:1:i')
V2 = board.get_pin('a:2:i')


def arduino_temperatures():
    try:
        board.digital[13].write(1)
    except:
        import arduino_connect
        # time.sleep(1)
        return [0, 0, 0]

    analog_value = V0.read()
    analog_value2 = V1.read()
    analog_value3 = V2.read()
    if analog_value is not None:
        T1 = round(32 * 5 * float(analog_value), 1)
        T2 = round(32 * 5 * float(analog_value2), 1)
        T3 = round(32 * 5 * float(analog_value3), 1)

        return [T1, T2, T3]
    else:
        time.sleep(1)
        return arduino_temperatures()


if __name__ == '__main__':
    print(arduino_temperatures())

