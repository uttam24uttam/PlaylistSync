import os
from flask import Flask, render_template
from dotenv import load_dotenv
from auth import auth_bp
from spotify import spotify_bp

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')  

app.register_blueprint(auth_bp)
app.register_blueprint(spotify_bp)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=os.getenv('FLASK_DEBUG', 'false').lower() in ['true', '1', 't'])
