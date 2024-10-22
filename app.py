# app.py

from flask import Flask

app = Flask(__name__)

app.config['SERVER_NAME'] = 'mmiroslav.pythonanywhere.com'

@app.route('/')
def hello():
    return 'Hello world!'

if __name__ == '__main__':
    app.run(debug=True)