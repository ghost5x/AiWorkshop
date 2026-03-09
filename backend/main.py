from flask import Flask,jsonify,request
from db import get_conn

app = Flask(__name__)

@app.route("/health")
def health():
    return "server alive"

@app.route("/register",methods=["POST"])
def register():
    conn = get_conn()
    cursor = conn.cursor()
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    if not name or not email or not password:
        return jsonify({"error": "All fields required"}), 400
    try:
        cursor.execute("INSERT INTO USERS (user_name,email,password) VALUES( %s,%s,%s)",(name,email,password))
        conn.commit()
    except Exception as e:
        conn.rollback()
        return jsonify({"error":str(e)}),500
    return jsonify({"message":"user registered"}),201

@app.route("/login",methods=["POST"])
def login():
    conn = get_conn()
    cursor = conn.cursor()
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    try:
        cursor.execute("SELECT id from USERS WHERE email = %s and password = %s",(email,password))
        id = cursor.fetchone()
        return jsonify({"id":id}),200
    except Exception as e:
        return jsonify({"error":str(e)}),400


if __name__ == "__main__":
    app.run()