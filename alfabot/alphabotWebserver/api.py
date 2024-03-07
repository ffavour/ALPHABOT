from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify
import sqlite3
import time
import AlphaBot

app = Flask(__name__)

bottino = AlphaBot.AlphaBot()


@app.route('/api/v1/sensors/left', methods=['GET'])
def sensoreLeft():
    stato = bottino.get_sensors()
    print(stato)

    if stato == "OB_L":
        print("sx")
        risposta = {"sinistra": "occupato"}
    else:
        print("no sx")
        risposta = {"sinistra": "non occupato"}

    return jsonify(risposta)


@app.route('/api/v1/sensors/right', methods=['GET'])
def sensoreRight():
    stato = bottino.get_sensors()
    print(stato)

    if stato == "OB_R":
        print("dx")
        risposta = {"destra": "occupato"}
    else:
        print("no dx")
        risposta = {"destra": "non occupato"}

    return jsonify(risposta)


@app.route('/api/v1/sensors', methods=['GET'])
def sensoreParametro():
    stato = bottino.get_sensors()

    if 'par' in request.args:
        par = str(request.args['par'])
        if par == 's':
            sensoreLeft()
        elif par == 'r':
            sensoreRight()
    else:
        return "Error: No pat field provided"




if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=  10002)
