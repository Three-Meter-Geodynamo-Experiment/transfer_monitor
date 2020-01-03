from flask import Flask, render_template

import adruino_connect
import wireless_temp_connect

app = Flask(__name__, static_url_path='/static')


@app.route("/")
def index():
    adruino_temp = (adruino_connect.adruino_temperatures())
    wireless_temp = (wireless_temp_connect.wireless_temp_timed())
    # print(wireless_temp)
    adr_t1 = adruino_temp[0]
    adr_t2 = adruino_temp[1]
    adr_t3 = adruino_temp[2]

    wrls_t1 = wireless_temp[0]
    wrls_t2 = wireless_temp[1]
    wrls_t3 = wireless_temp[2]
    wrls_t4 = wireless_temp[3]

    adr_p1 = '-1'
    adr_p2 = '-1'
    adr_p3 = '-1'

    user = {'adr_temp': adruino_temp, 'wrl_temp': wireless_temp}
    temperatures = {'T1': wrls_t1, 'T2': wrls_t2, 'T3': wrls_t3, 'T4': adr_t1, 'T5': adr_t2, 'T6': adr_t3, 'T7': wrls_t4}
    pressures = {'P1': adr_p1, 'P2': adr_p2, 'P3': adr_p3, }
    return render_template('index.html', title='Home', user=user, temperatures=temperatures, pressures=pressures)


if __name__ == "__main__":
    app.run('0.0.0.0')
