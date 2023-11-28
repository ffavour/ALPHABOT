from flask import Flask, render_template, request
import AlphaBot

app = Flask(__name__)
bottino = AlphaBot.AlphaBot()


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':

        if request.form.get('avanti') == 'avantiBtn':  # name == value
            print("vado avanti")
            bottino.forward()
        elif request.form.get('indietro') == 'indietroBtn':
            print("vado indietro")
            bottino.backward()
        elif request.form.get('destra') == 'destraBtn':
            print("vado a dx")
            bottino.right()
        elif request.form.get('sinistra') == 'sinistraBtn':
            print("vado a sx")
            bottino.left()
        else:
            print("ERROR")
    elif request.method == 'GET':
        return render_template('index.html')

    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True, host='localhost')
