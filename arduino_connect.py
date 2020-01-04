import pyfirmata
import time
import multiprocessing


board = pyfirmata.Arduino('/dev/tty.usbmodem14201')
# board.exit()
it = pyfirmata.util.Iterator(board)
it.start()

V0 = board.get_pin('a:0:i')
V1 = board.get_pin('a:1:i')
V2 = board.get_pin('a:2:i')

ard_temp_array = multiprocessing.Array('d', 3*[-2])


def arduino_temperatures(ard_temp_array=ard_temp_array):
    global board, it, V0, V1, V2

    try:
        board.digital[13].write(1)
        board.digital[13].write(0)
    except:
        try:
            board = pyfirmata.Arduino('/dev/tty.usbmodem14201')
            # board.exit()
            it = pyfirmata.util.Iterator(board)
            it.start()
            print('Arduino 1 is coming back')
            V0 = board.get_pin('a:0:i')
            V1 = board.get_pin('a:1:i')
            V2 = board.get_pin('a:2:i')
        except:
            print('Arduino 1 is down, waiting to reconnect')
            time.sleep(1)
            return [0, 0, 0]

        return [0, 0, 0]

    analog_value = V0.read()
    analog_value2 = V1.read()
    analog_value3 = V2.read()

    while not analog_value:
        time.sleep(1)

    T1 = round(32 * 5 * float(analog_value), 1)
    T2 = round(32 * 5 * float(analog_value2), 1)
    T3 = round(32 * 5 * float(analog_value3), 1)

    ard_temp_array[:] = [T1, T2, T3]

    return [T1, T2, T3]


def arduino_temperatures_timed():
    ard1 = multiprocessing.Process(target='arduino_temperatures', args=(ard_temp_array,))
    ard1.start()
    ard1.join(10)
    if ard1.is_alive():
        print('Arduino 1 Response Max Time Reached')
        ard1.terminate()
        ard1.join()
        ard_temp_array[:] = 3*[-2]
    # print(ard_temp_array[:])
    return ard_temp_array[:]


if __name__ == '__main__':
    print(arduino_temperatures())
    # print(arduino_temperatures_timed())
