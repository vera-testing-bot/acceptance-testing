from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/status/1", methods=["GET"])
def status_1():
    return jsonify({"round": 1, "status": "ok"}), 200


if __name__ == "__main__":
    app.run()
