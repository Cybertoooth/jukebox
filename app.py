from flask import Flask, render_template, url_for, redirect, make_response
from models.user import db, User
from models.artist import Artist
from models.album import Album
from models.genre import Genre
from models.jukebox import Jukebox
from models.playlist import Playlist
from models.song import Song
from dotenv import load_dotenv
from datetime import datetime
from flask_redis import FlaskRedis
import os
import smtplib
from email.message import EmailMessage
import time

load_dotenv('.env')

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER')
app.config['MAIL_PORT'] = os.environ.get('MAIL_PORT')
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS')
app.config['MAIL_USE_SSL'] = os.environ.get('MAIL_USE_SSL')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER')
app.config['MAIL_TEST_RECIPIENT'] = os.environ.get('MAIL_TEST_RECIPIENT')
app.config['REDIS_URL'] = os.environ.get('REDIS_URL')
db.init_app(app)
rc = FlaskRedis(app)



@app.route('/', methods=['GET'])
def index():
   pass

@app.route('/register', methods=['GET', 'POST'])
def register():
    user = {
     'name' : 'Bobby',
     'username' : 'USERNAME HERE',
     'passcode' : User.generate_passcode(),
     'email' : app.config['MAIL_TEST_RECIPIENT']
    }
    template = render_template('email.html', name=user['name'], passcode=user['passcode'])
    registration_data = {
        'email' : user['email'],
        'subject' : 'Welcome to Jukebox - Registration',
        'sender' : app.config['MAIL_DEFAULT_SENDER'],
        'port' : app.config['MAIL_PORT'],
        'template' : template,
        'server' : app.config['MAIL_SERVER'],
        'username' : app.config['MAIL_USERNAME'],
        'password' : app.config['MAIL_PASSWORD']
    }
    User.cache_passcode(rc, user)
    User.mail_passcode(**registration_data)
    return 'message sent'

@app.route('/verify-account', methods=['GET', 'POST'])
def verify_account():
    user = {
      'username' : 'USERNAME HERE',
      'passcode' : 'PASSCODE HERE'
    }
    result = User.verify_passcode(rc, **user)
    response = make_response(result)
    if response.status_code == 401:
        return result
    else:
        return redirect(url_for('explore'))


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    pass

@app.route('/signout', methods=['GET'])
def signout():
    pass

@app.route('/settings', methods=['GET', 'PATCH'])
def settings():
    pass

@app.route('/explore', methods=['GET'])
def explore():
    pass

@app.route('/search', methods=['GET', 'POST'])
def search():
    pass

@app.route('/your-music',methods=['GET', 'POST'])
def music_library():
    pass

@app.route('/song-of-the-day', methods=['GET'])
def sotd():
    pass

if __name__ == '__main__':
    app.run()
