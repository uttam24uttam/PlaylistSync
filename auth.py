from flask import Blueprint, redirect, request, session, url_for, render_template
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os
import time

load_dotenv()

SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
SPOTIPY_REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI')
SCOPE = os.getenv('SCOPE')

auth_bp = Blueprint('auth', __name__)

sp_oauth = SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                        client_secret=SPOTIPY_CLIENT_SECRET,
                        redirect_uri=SPOTIPY_REDIRECT_URI,
                        scope=SCOPE)

@auth_bp.route('/')
def index():
    token_info = get_token()
    if not token_info:
        return redirect(url_for('auth.login_spotify'))
    return render_template('index.html')

@auth_bp.route('/login_spotify')
def login_spotify():
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@auth_bp.route('/callback')
def callback():
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session['token_info'] = token_info
    return redirect(url_for('auth.index'))

def get_token():
    token_info = session.get('token_info', None)
    if not token_info:
        return None
    now = int(time.time())
    is_token_expired = token_info['expires_at'] - now < 60
    if is_token_expired:
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
    return token_info

