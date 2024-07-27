from flask import Flask, render_template, Blueprint, request, redirect, url_for, flash
from spotipy import Spotify
from auth import get_token
from youtube import fetch_youtube_playlist
import validators
from dotenv import load_dotenv
import os
load_dotenv() 

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')


spotify_bp = Blueprint('spotify', __name__)

@spotify_bp.route('/transfer', methods=['POST'])
def transfer():
    youtube_playlist_url = request.form['youtube_playlist_url']

    # Validate playlist URL
    if not validators.url(youtube_playlist_url):
        flash("Invalid YouTube playlist URL", "error")
        return redirect(url_for('spotify.index'))

    token_info = get_token()
    if not token_info:
        return redirect(url_for('auth.login_spotify'))

    sp = Spotify(auth=token_info['access_token'])
    user_id = sp.current_user()['id']

    # Fetch YouTube playlist data
    youtube_data = fetch_youtube_playlist(youtube_playlist_url)

    # Create a new Spotify playlist and add tracks
    sp_playlist = sp.user_playlist_create(user_id, youtube_data['title'])
    sp.user_playlist_add_tracks(user_id, sp_playlist['id'], youtube_data['tracks'])

    # Redirect to sucess page after the transfer of playlist
    return redirect(url_for('spotify.success'))

@spotify_bp.route('/success')
def success():
    return render_template('success.html')

@spotify_bp.route('/know-more')
def know_more():
    return render_template('know-more.html')

@spotify_bp.route('/')
def index():
    return render_template('index.html')

# Register the Blueprint
app.register_blueprint(spotify_bp)

if __name__ == '__main__':
    app.run(debug=True)
