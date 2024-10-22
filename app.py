# app.py

from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

if os.environ.get('FLASK_ENV') == 'production':
    app.config['SERVER_NAME'] = 'mmiroslav.pythonanywhere.com'
else:
    app.config['SERVER_NAME'] = '127.0.0.1:5000'

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/fetch-page')
def fetch_page():
    headers = dict(request.headers)

    title = "Welcome to the second page"

    return render_template('second_page.html',
                           title=title,
                           headers=headers)

if __name__ == '__main__':
    app.run(debug=True)