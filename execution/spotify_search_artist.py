#!/usr/bin/env python3
"""
Spotify Artist Search Script

Searches for an artist and returns matches.
"""

import argparse
import sys
import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def search_artist(sp, artist_name, limit=5):
    """
    Search for an artist on Spotify.
    
    Args:
        sp: Spotipy client instance
        artist_name: Name of artist to search
        limit: Number of results to return
        
    Returns:
        list: List of artist dictionaries (name, id, image, followers)
    """
    results = sp.search(q=artist_name, type='artist', limit=limit)
    
    artists = []
    for item in results['artists']['items']:
        image_url = item['images'][0]['url'] if item['images'] else None
        artists.append({
            'name': item['name'],
            'id': item['id'],
            'uri': item['uri'],
            'popularity': item['popularity'],
            'followers': item['followers']['total'],
            'image': image_url,
            'url': item['external_urls']['spotify']
        })
        
    return artists

if __name__ == "__main__":
    # This allows standalone testing using Client Credentials flow (no user login needed for search)
    try:
        auth_manager = SpotifyClientCredentials()
        sp = spotipy.Spotify(auth_manager=auth_manager)
        
        if len(sys.argv) > 1:
            query = " ".join(sys.argv[1:])
            results = search_artist(sp, query)
            print(json.dumps(results, indent=2))
        else:
            print("Usage: python spotify_search_artist.py <artist_name>")
            
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
