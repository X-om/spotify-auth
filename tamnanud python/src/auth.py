from flask import Flask, request, redirect, session, render_template, url_for
import requests
import os
from urllib.parse import urlencode

app = Flask(__name__)
app.secret_key = os.urandom(24)

client_id = "ff7e93d10fb44718b8ee986a1c32f14a"
client_secret = "9856d7100ceb4010901db998dbec107c"
redirect_uri = "http://127.0.0.1:5000/callback"

auth_url = "https://accounts.spotify.com/authorize"
token_url = "https://accounts.spotify.com/api/token"

@app.route('/')
def index():
    params = {
        "client_id": client_id,
        "response_type": "code",
        "redirect_uri": redirect_uri,
        "scope": "user-read-playback-state user-modify-playback-state"
    }
    return redirect(auth_url + "?" + urlencode(params))

@app.route("/callback")
def callback():
    code = request.args.get("code")
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri,
        "client_id": client_id,
        "client_secret": client_secret
    }
    try:
        response = requests.post(token_url, data=data)
        response.raise_for_status()  # Raise exception for non-2xx responses
        token_data = response.json()

        session["access_token"] = token_data["access_token"]
        session["refresh_token"] = token_data["refresh_token"]

        return redirect(url_for("success"))
    except requests.RequestException as e:
        # Handle request exceptions
        return "Error occurred: " + str(e)

@app.route("/success")
def success():
    return render_template("success.html")

if __name__ == "__main__":
    app.run(debug=True)
