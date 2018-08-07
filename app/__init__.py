from flask import Flask, send_from_directory
from flask_ask import Ask

app = Flask(__name__)
ask = Ask(app, '/')

from app import alexa

@app.route('/pek')
def hello_world():
    return 'Hello World!'





if __name__ == '__main__':
    app.run()
