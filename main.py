from flask import Flask, request
app = Flask(__name__)

@app.route('/collect', methods=['POST'])
def collect():
    data = request.form
    print(f"📡 Incoming data: {data}")
    with open("log.txt", "a") as f:
        f.write(str(data) + "\n")
    return "OK"

app.run(host='0.0.0.0', port=3000)
