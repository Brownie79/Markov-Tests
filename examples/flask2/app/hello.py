from facebook import get_user_from_cookie, GraphAPI
from flask import Flask, g, render_template, redirect, request, session, url_for


app = Flask(__name__)

# Facebook app details
FB_APP_ID = '460299580843062'
FB_APP_NAME = 'markov'
FB_APP_SECRET = 'a892688755cd673d914e075ca377f824'


@app.route('/')
def index():
    return render_template('index.html', app_id=FB_APP_ID, name=FB_APP_NAME)


if __name__ == '__main__':
    app.run()
