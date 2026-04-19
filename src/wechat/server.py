from flask import Flask, request
from src.wechat.wecom import WeComBot

app = Flask(__name__)
bot = WeComBot()

@app.route("/webhook",methods=["POST"])
def webhook():
    data = request.json
    print(data)
    return "success"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

