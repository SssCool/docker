import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

required_env_vars = ["DB_HOST", "DB_USER", "DB_PASSWORD", "DB_NAME"]
missing_vars = [var for var in required_env_vars if not os.getenv(var)]
if missing_vars:
    raise EnvironmentError(f"Missing required environment variables: {', '.join(missing_vars)}")

DB_CONFIG = {
    "host": os.environ["DB_HOST"],
    "user": os.environ["DB_USER"],
    "password": os.environ["DB_PASSWORD"],
    "database": os.environ["DB_NAME"]
}

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

@app.route("/register", methods=["POST"])
def register_user():
    data = request.json
    username = data.get("username")
    email = data.get("email")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (username, email) VALUES (%s, %s)",
        (username, email)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "User registered successfully"})

@app.route("/list", methods=["GET"])
def list_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, email FROM users")
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(users)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8090, debug=True)