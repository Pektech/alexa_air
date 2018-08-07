from flask import Flask, send_from_directory
from flask_ask import Ask

app = Flask(__name__)
ask = Ask(app, '/')

from app import alexa

@app.route('/pek')
def hello_world():
    return 'Hello World!'

@app.route('/static/images/<path:filename>')
def ret_image(filename):
    return send_from_directory('static/images', filename,)



if __name__ == '__main__':
    app.run()
