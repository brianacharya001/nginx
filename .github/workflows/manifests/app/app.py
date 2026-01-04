from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def hello():
    revision = os.getenv('APP_REVISION', 'unknown')
    return f"<h1>Hello from Flask!</h1><p>Running Revision: <b>{revision}</b></p>"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
