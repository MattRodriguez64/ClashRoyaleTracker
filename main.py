import requests
from flask import Flask, render_template, url_for, redirect, request, session
import json
from pprint import pprint

player_data_url = "https://api.clashroyale.com/v1/players/"
ext_battlelog = "/battlelog"
headers = {
    'Content-type': 'application/json',
    'User-Agent': 'XY'
}

app = Flask(__name__)
app.secret_key = "ClashRoyaleTrackerKEY"


@app.route('/', methods=["POST", "GET"])
def home():
    if request.method == "POST":
        token = request.form["token"]
        playerTagRaw = request.form["player_uuid"]

        if (token == "") or (playerTagRaw == ""):
            playerTagErr = True
            return render_template("login.html", error=playerTagErr, error_msg="Champ vide !")

        if '#' not in playerTagRaw:
            playerTagErr = True
            return render_template("login.html", error=playerTagErr, error_msg="Player Tag Invalide !")

        playerTagFormatted = f"%23{playerTagRaw.split('#')[1]}"
        headers['Authorization'] = f"Bearer {token}"

        session['playerTag'] = playerTagFormatted

        print(playerTagFormatted)
        print(headers)

        return redirect(url_for("data"))
    return render_template("login.html")


@app.route('/data')
def data():

    if 'playerTag' in session:
        playerTag = session['playerTag']
        player_data = requests.get(url=f"{player_data_url}{playerTag}", headers=headers).json()
        pprint(player_data)

        player_data_battlelog = requests.get(url=f"{player_data_url}{playerTag}{ext_battlelog}",
                                             headers=headers).json()
        pprint(player_data_battlelog)

        return render_template("base.html")
    else :
        return redirect(url_for("home"))



if __name__ == "__main__":

    app.run()
