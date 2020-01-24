import pyfirmata2
import time
import multiprocessing as mp


both_arduinos_analog_pins = mp.Array('d', 12*[0])


def updating_first_arduino(both_arduinos_analog_pins=both_arduinos_analog_pins):
    while True:
        try:
            for chan_ind in range(6):
                both_arduinos_analog_pins[chan_ind] = 0

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
                    both_arduinos_analog_pins[0] = float(analog_0.read())
                    both_arduinos_analog_pins[1] = float(analog_1.read())
                    both_arduinos_analog_pins[2] = float(analog_2.read())
                    both_arduinos_analog_pins[3] = float(analog_3.read())
                    both_arduinos_analog_pins[4] = float(analog_4.read())
                    both_arduinos_analog_pins[5] = float(analog_5.read())
                    # print(analog_0.read())
                    time.sleep(1)
                    board.digital[13].write(1)
                    board.digital[13].write(0)
                except TypeError:
                    print('trying again')
                    time.sleep(1)
                    continue

        except:
            print('Something is wrong, connecting Arduino 1 again')
            time.sleep(1)
            continue


def updating_second_arduino(both_arduinos_analog_pins=both_arduinos_analog_pins):
    while True:
        try:
            for chan_ind in range(6, 12):
                both_arduinos_analog_pins[chan_ind] = 0

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
                    both_arduinos_analog_pins[6] = float(analog_0.read())
                    both_arduinos_analog_pins[7] = float(analog_1.read())
                    both_arduinos_analog_pins[8] = float(analog_2.read())
                    both_arduinos_analog_pins[9] = float(analog_3.read())
                    both_arduinos_analog_pins[10] = float(analog_4.read())
                    both_arduinos_analog_pins[11] = float(analog_5.read())
                    # print(analog_0.read())
                    time.sleep(1)
                    board.digital[13].write(1)
                    board.digital[13].write(0)
                except TypeError:
                    print('trying again')
                    time.sleep(1)
                    continue

        except:
            print('Something is wrong, connecting Arduino 2 again')
            time.sleep(1)
            continue


def printing_data(both_arduinos_analog_pins=both_arduinos_analog_pins):
    while True:
        print([round(x, 2) for x in both_arduinos_analog_pins[:]])
        time.sleep(1)


if __name__ == '__main__':

    first_arduino = mp.Process(target=updating_first_arduino, args=(both_arduinos_analog_pins, ))
    second_arduino = mp.Process(target=updating_second_arduino, args=(both_arduinos_analog_pins,))
    print_both_arduinos = mp.Process(target=printing_data, args=(both_arduinos_analog_pins,))

    first_arduino.start()
    second_arduino.start()

    print_both_arduinos.start()

    first_arduino.join()
    second_arduino.join()
    print_both_arduinos.join()
