# app.py

from flask import Flask, render_template, request, Response, send_from_directory
from functools import wraps
import requests
import base64
import os

app = Flask(__name__)

if os.environ.get('FLASK_ENV') == 'production':
    app.config['SERVER_NAME'] = 'mmiroslav.pythonanywhere.com'
else:
    app.config['SERVER_NAME'] = '127.0.0.1:5000'

def check_auth(username, password):
    return username == 'username' and password == 'password'

def request_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return Response('Authorization required', 401,
                          {'WWW-Authenticate': 'Basic realm="Login Required"'})

        try:
            auth_type, auth_string = auth_header.split(' ', 1)
            if auth_type.lower() != 'basic':
                return Response('Basic authentication required', 401)

            credentials = base64.b64decode(auth_string).decode('utf-8')
            username, password = credentials.split(':', 1)

            if check_auth(username, password):
                return f(*args, **kwargs)
        except Exception as e:
            app.logger.error(f"Auth error: {str(e)}")

        return Response('Invalid credentials', 401,
                       {'WWW-Authenticate': 'Basic realm="Login Required"'})

    return decorated

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

@app.route('/sw.js')
def service_worker():
    return send_from_directory('public', 'sw.js', mimetype='application/javascript')


if __name__ == '__main__':
    app.run(debug=True)