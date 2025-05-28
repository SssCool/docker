import os
from flask import Flask, render_template, request
import requests

app = Flask(__name__)

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8090")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/userlist")
def user_list():
    users = requests.get(f"{BACKEND_URL}/list").json()
    return render_template("userlist.html", users=users)

@app.route("/register", methods=["POST"])
def register():
    data = {
        "username": request.form["username"],
        "email": request.form["email"]
    }
    requests.post(f"{BACKEND_URL}/register", json=data)
    return "User registered successfully!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)