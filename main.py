import requests
from flask import Flask, render_template, url_for, redirect, request
import json
from pprint import pprint

player_data_url = "https://api.clashroyale.com/v1/players/"
ext_battlelog = "/battlelog"
headers = {
    'Content-type': 'application/json',
    'User-Agent': 'XY'
}

app = Flask(__name__)


@app.route('/', methods=["POST", "GET"])
def home():
    if request.method == "POST":
        token = request.form["token"]
        playerTagRaw = request.form["player_uuid"]

        playerTagFormatted = f"%23{playerTagRaw.split('#')[1]}"
        headers['Authorization'] = f"Bearer {token}"

        print(playerTagFormatted)
        print(headers)

        player_data = requests.get(url=f"{player_data_url}{playerTagFormatted}", headers=headers).json()
        pprint(player_data)

        player_data_battlelog = requests.get(url=f"{player_data_url}{playerTagFormatted}{ext_battlelog}",
                                             headers=headers).json()
        pprint(player_data_battlelog)

        return redirect(url_for("data"))
    return render_template("login.html")


@app.route('/data')
def data():
    return render_template("base.html")


if __name__ == "__main__":
    app.run()
