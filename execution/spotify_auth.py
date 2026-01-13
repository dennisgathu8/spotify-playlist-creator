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

import streamlit as st

# Load environment variables
load_dotenv()

SCOPE = "user-library-read playlist-modify-public playlist-modify-private"


def get_credentials():
    """
    Retrieve credentials from Streamlit secrets (deployment) or environment variables (local).
    Returns tuple (client_id, client_secret, redirect_uri)
    """
    # Try Streamlit Secrets first (for Cloud deployment)
    try:
        client_id = st.secrets.get("SPOTIPY_CLIENT_ID")
        client_secret = st.secrets.get("SPOTIPY_CLIENT_SECRET")
        redirect_uri = st.secrets.get("SPOTIPY_REDIRECT_URI")
        
        if client_id and client_secret and redirect_uri:
            return client_id, client_secret, redirect_uri
    except FileNotFoundError:
        pass  # secrets.toml not found, fall back to env vars

    # Fall back to environment variables (for local dev)
    client_id = os.getenv("SPOTIPY_CLIENT_ID")
    client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")
    redirect_uri = os.getenv("SPOTIPY_REDIRECT_URI")
    
    return client_id, client_secret, redirect_uri


def get_oauth_manager():
    """Create and return SpotifyOAuth manager."""
    CLIENT_ID, CLIENT_SECRET, REDIRECT_URI = get_credentials()
    
    if not CLIENT_ID or not CLIENT_SECRET or not REDIRECT_URI:
        raise ValueError((
            "Missing Spotify credentials. "
            "Set SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, and SPOTIPY_REDIRECT_URI "
            "in .env (local) or Streamlit Secrets (deployment)."
        ))
        
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



