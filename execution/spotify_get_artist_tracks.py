#!/usr/bin/env python3
"""
Spotify Get Artist Tracks

Fetches all tracks for a given artist (albums and singles).
Filters to ensure artist is a primary performer.
"""

import sys
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_all_artist_tracks(sp, artist_id, artist_name, progress_callback=None):
    """
    Fetch all unique tracks for an artist.
    
    Args:
        sp: Spotipy client instance
        artist_id: Spotify Artist ID
        artist_name: Name of the artist (for filtering)
        progress_callback: Optional function to report progress (msg)
        
    Returns:
        list: List of track dictionaries
    """
    if progress_callback:
        progress_callback("Fetching albums...")
        
    # 1. Get all albums (include singles and compilations)
    albums = []
    results = sp.artist_albums(artist_id, album_type='album,single', limit=50)
    albums.extend(results['items'])
    
    while results['next']:
        results = sp.next(results)
        albums.extend(results['items'])
        
    if progress_callback:
        progress_callback(f"Found {len(albums)} releases. Fetching tracks...")
        
    # 2. Get tracks for each album
    all_tracks = []
    seen_track_names = set() # Simple name-based deduplication
    
    for album in albums:
        # Get tracks for this album
        tracks_results = sp.album_tracks(album['id'])
        tracks = tracks_results['items']
        
        while tracks_results['next']:
            tracks_results = sp.next(tracks_results)
            tracks.extend(tracks_results['items'])
            
        for track in tracks:
            # Check if artist is a primary artist on this track
            artists_on_track = [a['id'] for a in track['artists']]
            
            if artist_id in artists_on_track:
                # Deduplicate based on name (ignoring case)
                track_name_key = track['name'].lower().strip()
                
                # Check for "remix", "live", "acoustic" if you want strict studio versions
                # For now, we'll just basic deduplicate
                
                if track_name_key not in seen_track_names:
                    seen_track_names.add(track_name_key)
                    all_tracks.append({
                        'name': track['name'],
                        'uri': track['uri'],
                        'id': track['id'],
                        'album': album['name'],
                        'duration_ms': track['duration_ms']
                    })
                    
    if progress_callback:
        progress_callback(f"Found {len(all_tracks)} unique tracks.")
        
    return all_tracks

if __name__ == "__main__":
    try:
        auth_manager = SpotifyClientCredentials()
        sp = spotipy.Spotify(auth_manager=auth_manager)
        
        if len(sys.argv) > 1:
            artist_id = sys.argv[1]
            # Ideally we'd pass name too, but for CLI test we'll skip strict name check
            tracks = get_all_artist_tracks(sp, artist_id, "Unknown")
            print(f"Found {len(tracks)} tracks.")
            for t in tracks[:5]:
                print(f"- {t['name']} ({t['album']})")
        else:
            print("Usage: python spotify_get_artist_tracks.py <artist_id>")
            
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
