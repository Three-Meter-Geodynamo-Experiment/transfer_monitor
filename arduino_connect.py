# import pyfirmata
# import time
# import multiprocessing
#
# board = pyfirmata.Arduino('/dev/tty.usbmodem14201')
# # board2 = pyfirmata.Arduino('/dev/tty.usbmodem14101')
#
# # board.exit()
#
# it = pyfirmata.util.Iterator(board)
# it.start()
# # #
# # it2 = pyfirmata.util.Iterator(board2)
# # it2.start()
#
#
# V0 = board.get_pin('a:0:i')
# V1 = board.get_pin('a:1:i')
# V2 = board.get_pin('a:2:i')
# V3 = board.get_pin('a:3:i')
# # # # ard_temp_array = multiprocessing.Array('d', 3*[-2])
# # V02 = board2.get_pin('a:0:i')
# # V12 = board2.get_pin('a:1:i')
# # V22 = board2.get_pin('a:2:i')
# # V32 = board2.get_pin('a:3:i')
#
#
# def arduino_temperatures():
#     global board, it, V0, V1, V2, V3
#
#     try:
#         # print('JO')
#         board.digital[13].write(1)
#         board.digital[13].write(0)
#     except:
#         try:
#             board = pyfirmata.Arduino('/dev/tty.usbmodem14201')
#             # board.exit()
#             board.iterate()
#
#             it = pyfirmata.util.Iterator(board)
#             it.start()
#             print('Arduino 1 is coming back')
#             V0 = board.get_pin('a:0:i')
#             V1 = board.get_pin('a:1:i')
#             V2 = board.get_pin('a:2:i')
#             V3 = board.get_pin('a:3:i')
#
#             # return [0, 0, 0, 0]
#         except:
#             print('Arduino 1 is down, waiting to reconnect')
#             time.sleep(0.3)
#             return [0, -1, -1, -1]
#
#     analog_value = V0.read()
#     # print(analog_value)
#     analog_value2 = V1.read()
#     analog_value3 = V2.read()
#     analog_value4 = V3.read()
#     print(analog_value, analog_value2, analog_value3, analog_value4)
#     # print('got to waiting')
#     # while not analog_value:
#     #     time.sleep(0.1)
#     try:
#         T1 = round(32 * 5 * float(analog_value), 1)
#         T2 = round(32 * 5 * float(analog_value2), 1)
#         T3 = round(32 * 5 * float(analog_value3), 1)
#         T4 = round(32 * 5 * float(analog_value4), 1)
#
#         # ard_temp_array[:] = [T1, T2, T3]
#     except TypeError:
#         return [-1, 0, -1, -1]
#     # print(float(analog_value)*5)
#     return [T1, T2, T3, T4]
#
#
# # def arduino_pressures():
# #     global board2, it2, V02, V12, V22, V32
# #
# #     try:
# #         # print('JO')
# #         board2.digital[13].write(1)
# #         board2.digital[13].write(0)
# #     except:
# #         try:
# #             board2 = pyfirmata.Arduino('/dev/tty.usbmodem14101')
# #             # board.exit()
# #             it2 = pyfirmata.util.Iterator(board2)
# #             it2.start()
# #             print('Arduino 2 is coming back')
# #             V02 = board2.get_pin('a:0:i')
# #             V12 = board2.get_pin('a:1:i')
# #             V22 = board2.get_pin('a:2:i')
# #             V32 = board2.get_pin('a:3:i')
# #
# #             # return [0, 0, 0, 0]
# #         except:
# #             print('Arduino 2 is down, waiting to reconnect')
# #             time.sleep(0.3)
# #             return [0, -1, -1, -1]
# #
# #     analog_value_2 = V02.read()
# #     analog_value2_2 = V12.read()
# #     analog_value3_2 = V22.read()
# #     analog_value4_2 = V32.read()
# #
# #     # print(analog_value_2)
# #     # print('got to waiting')
# #     # while not analog_value:
# #     #     time.sleep(0.1)
# #     try:
# #         p1 = pressure_voltage(float(analog_value_2))
# #         p2 = pressure_voltage(float(analog_value2_2))
# #         p3 = pressure_voltage(float(analog_value3_2))
# #         p4 = pressure_voltage(float(analog_value4_2))
# #
# #         # ard_temp_array[:] = [T1, T2, T3]
# #     except TypeError:
# #         return [-1, 0, -1, -1]
# #     # print(float(analog_value)*5)
# #     return [p1, p2, p3, p4]
#
#
#
#
# if __name__ == '__main__':
#     time.sleep(5)
#     print(arduino_temperatures())
#     # print(arduino_pressures())
#     # print(arduino_temperatures_timed())
