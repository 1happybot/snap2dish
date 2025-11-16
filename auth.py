"""Authentication module for Google OAuth."""
import json
import requests
from flask import Blueprint, redirect, request, url_for, session
from flask_login import login_user, logout_user, login_required
from authlib.integrations.flask_client import OAuth
from models import db, User

auth_bp = Blueprint('auth', __name__)


def init_oauth(app):
    """Initialize OAuth with the Flask app."""
    oauth = OAuth(app)
    
    google = oauth.register(
        name='google',
        client_id=app.config['GOOGLE_CLIENT_ID'],
        client_secret=app.config['GOOGLE_CLIENT_SECRET'],
        server_metadata_url=app.config['GOOGLE_DISCOVERY_URL'],
        client_kwargs={
            'scope': 'openid email profile'
        }
    )
    
    return oauth, google


@auth_bp.route('/login')
def login():
    """Redirect to Google OAuth login."""
    from flask import current_app
    oauth = current_app.extensions.get('oauth')
    if not oauth:
        # For development without OAuth configured
        return redirect(url_for('index'))
    
    google = oauth.google
    redirect_uri = url_for('auth.callback', _external=True)
    return google.authorize_redirect(redirect_uri)


@auth_bp.route('/callback')
def callback():
    """Handle OAuth callback from Google."""
    from flask import current_app
    oauth = current_app.extensions.get('oauth')
    
    if not oauth:
        # For development without OAuth configured
        return redirect(url_for('index'))
    
    try:
        google = oauth.google
        token = google.authorize_access_token()
        user_info = token.get('userinfo')
        
        if user_info:
            # Check if user exists
            user = User.query.filter_by(google_id=user_info['sub']).first()
            
            if not user:
                # Create new user
                user = User(
                    google_id=user_info['sub'],
                    email=user_info['email'],
                    name=user_info.get('name'),
                    profile_pic=user_info.get('picture')
                )
                db.session.add(user)
                db.session.commit()
            
            # Login the user
            login_user(user)
            
    except Exception as e:
        print(f"OAuth error: {e}")
    
    return redirect(url_for('index'))


@auth_bp.route('/logout')
@login_required
def logout():
    """Logout the current user."""
    logout_user()
    return redirect(url_for('index'))
