import pyfirmata
import time

global board, it, V0, V1, V2
board = pyfirmata.Arduino('/dev/tty.usbmodem14201')

it = pyfirmata.util.Iterator(board)
it.start()

V0 = board.get_pin('a:0:i')
V1 = board.get_pin('a:1:i')
V2 = board.get_pin('a:2:i')


def adruino_temperatures():
    global board, it, V0, V1, V2
    try:
        board.digital[13].write(1)
    except:
        board = pyfirmata.Arduino('/dev/tty.usbmodem14201')

        it = pyfirmata.util.Iterator(board)
        it.start()

        V0 = board.get_pin('a:0:i')
        V1 = board.get_pin('a:1:i')
        V2 = board.get_pin('a:2:i')

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
        return adruino_temperatures()


if __name__ == '__main__':
    print(adruino_temperatures())

