import telnetlib
import time
import multiprocessing

HOST = "192.168.1.200"
PORT = "2000"

wrls_temp_array = multiprocessing.Array('d', 6*[-2])

tn = telnetlib.Telnet(HOST, PORT)  # make connection
#
# global last_time_checked_wrls
# last_time_checked_wrls = time.time()


def wireless_temp(wrls_temp_array=wrls_temp_array):

    attempts = 0

    # defining when to stop
    stop_sign = b'\r\n'
    stop_sign2= b'Warn: No data received from end device yet\r\n'
    #  Preassuming the temperatures are not known

    T = ([-1, -1, -1, -1, -1, -1])

    # sending a request to return values
    tn.write("ERDG00A\n".encode('ascii'))
    # lets read while we can
    while attempts < 20:
        attempts += 1
        response = tn.read_until("\n".encode('ascii'))
        # print(response)
        if response == stop_sign or response == stop_sign2:
            # print('Stop sign reached')
            break

        response_array = (response[0:-2].decode("ascii")).split()

        if response_array[3] == "Open":
            T[int(response_array[0]) - 1] = 0
        else:
            # print(response_array[3])
            try:
                T[int(response_array[0])-1] = float(response_array[3])
            except ValueError:
                print('Value error pew pew')
            except IndexError:
                print('Index error pew pew')


    # print('T', T)
    # time.sleep(3)

    tn.write("EQNG00A\n".encode('ascii'))
    attempts = 0
    while attempts < 20:
        attempts += 1
        response = tn.read_until("\n".encode('ascii'))
        # print(response)
        if response == stop_sign or response == stop_sign2:
            # print('Stop sign reached')
            break

        response_array = (response.decode("ascii")).split()
        # print(response_array)
        if response_array[2][1] == "1":
            T[int(response_array[0]) - 1] = -0.5
        # else:
        #     # print(response_array[3])
        #     T[int(re


    wrls_temp_array[:] = T
    # print('wrls_temp_array', wrls_temp_array)
    return T


def wireless_temp_timed():
    p = multiprocessing.Process(target=wireless_temp, name="Thread1", args=(wrls_temp_array,))
    p.start()
    p.join(5)
    if p.is_alive():
        print('Wireless Temp Response Max Time Reached')
        # tn = telnetlib.Telnet(HOST, PORT)
        p.terminate()
        p.join()
        wrls_temp_array[:] = 6*[-2]
    # print(wrls_temp_array[:])
    return wrls_temp_array[:]


if __name__ == '__main__':
    print(wireless_temp())
    time.sleep(3)
    print()
    print(wireless_temp())
    # print(wireless_temp())

    print('__main__ executed pew pew')
    # print(wireless_temp_timed())
    # print(wrls_temp_array[:])


# b'2    Shell 01000000 1.0 \r\n'
# b'4  Floater 11000000 1.0 \r\n'