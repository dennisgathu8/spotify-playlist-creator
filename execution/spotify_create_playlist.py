#!/usr/bin/env python3
"""
Spotify Create Playlist

Creates a playlist and adds tracks to it.
"""

import sys
import spotipy

def create_playlist_for_user(sp, user_id, name, description, public=True):
    """Create a new playlist."""
    return sp.user_playlist_create(
        user=user_id,
        name=name,
        public=public,
        description=description
    )

def add_tracks_to_playlist(sp, playlist_id, track_uris):
    """
    Add tracks to playlist in batches of 100 (Spotify API limit).
    """
    # Split into chunks of 100
    chunk_size = 100
    for i in range(0, len(track_uris), chunk_size):
        chunk = track_uris[i:i + chunk_size]
        sp.playlist_add_items(playlist_id, chunk)
        
    return len(track_uris)

if __name__ == "__main__":
    print("This module is designed to be imported by the main app.")
    print("It requires an authenticated user session.")
