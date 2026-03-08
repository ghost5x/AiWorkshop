from flask import Flask,jsonify,request
import pymysql

app = Flask(__name__)

@app.route("/health")
def health():
    return "server alive"

if __name__ == "__main__":
    app.run()