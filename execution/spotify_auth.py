#!/usr/bin/env python3
"""
Spotify Authentication Helper

Handles OAuth flow for Spotify API.
This script is designed to be imported by the Streamlit app or other scripts.

Usage:
    from execution.spotify_auth import get_spotify_client, get_auth_url, get_token_from_code
"""

import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")

SCOPE = "user-library-read playlist-modify-public playlist-modify-private"


def get_oauth_manager():
    """Create and return SpotifyOAuth manager."""
    if not CLIENT_ID or not CLIENT_SECRET or not REDIRECT_URI:
        raise ValueError("Missing Spotify credentials in .env file")
        
    return SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=SCOPE,
        cache_handler=None,  # We'll handle token storage in Session State
        show_dialog=True
    )


def get_auth_url():
    """Generates the Spotify authentication URL."""
    auth_manager = get_oauth_manager()
    return auth_manager.get_authorize_url()


def get_token_from_code(code):
    """Exchanges auth code for access token."""
    auth_manager = get_oauth_manager()
    return auth_manager.get_access_token(code)


def get_spotify_client(token_info):
    """
    Returns a Spotipy client instance using the provided token info.
    Checks if token is expired and refreshes if necessary.
    """
    if not token_info:
        return None
        
    auth_manager = get_oauth_manager()
    
    # Check if token is expired
    if auth_manager.is_token_expired(token_info):
        try:
            token_info = auth_manager.refresh_access_token(token_info['refresh_token'])
        except Exception as e:
            print(f"Error refreshing token: {e}")
            return None, None
            
    return spotipy.Spotify(auth=token_info['access_token']), token_info


if __name__ == "__main__":
    print("This module provides authentication helpers.")
    print(f"Client ID present: {bool(CLIENT_ID)}")
    print(f"Redirect URI: {REDIRECT_URI}")
