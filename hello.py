from flask import Flask, render_template
import importlib
import arduino_connect
import wireless_temp_connect

app = Flask(__name__, static_url_path='/static')
global old_arduino_temp 
old_arduino_temp = []


@app.route("/")
def index():
    global old_arduino_temp
    arduino_temp = (arduino_connect.arduino_temperatures())
    # if old_arduino_temp == arduino_temp:
    #     print('The same values of arduino temperatures detected, trying to connect again in a sec')
    #     importlib.reload(arduino_temp)
    # else:
    #     old_arduino_temp = arduino_temp
        
    wireless_temp = (wireless_temp_connect.wireless_temp_timed())
    # print(wireless_temp)
    adr_t1 = arduino_temp[0]
    adr_t2 = arduino_temp[1]
    adr_t3 = arduino_temp[2]

    wrls_t1 = wireless_temp[0]
    wrls_t2 = wireless_temp[1]
    wrls_t3 = wireless_temp[2]
    wrls_t4 = wireless_temp[3]

    adr_p1 = '-1'
    adr_p2 = '-1'
    adr_p3 = '-1'

    user = {'adr_temp': arduino_temp, 'wrl_temp': wireless_temp}
    temperatures = {'T1': wrls_t1, 'T2': wrls_t2, 'T3': wrls_t3, 'T4': adr_t1, 'T5': adr_t2, 'T6': adr_t3, 'T7': wrls_t4}
    pressures = {'P1': adr_p1, 'P2': adr_p2, 'P3': adr_p3, }
    return render_template('index.html', title='Home', user=user, temperatures=temperatures, pressures=pressures)


if __name__ == "__main__":
    app.run('0.0.0.0')
