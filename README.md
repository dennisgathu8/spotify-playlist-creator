# Spotify Artist Playlist Creator

A Streamlit application that generates complete playlists for any artist on Spotify.

## Features

- **OAuth Authentication**: Secure login with your Spotify account
- **Artist Search**: Find any artist on Spotify
- **Discography Fetching**: improved algorithm to fetch albums and singles
- **Smart Filtering**: Ensures artist is a primary performer (filters out compilation appearances)
- **Playlist Generation**: Creates a new playlist in your library with one click

## Setup

1. **Prerequisites**
   - Python 3.8+
   - Spotify Developer Account

2. **Installation**
   ```bash
   # Clone the repository
   git clone <your-repo-url>
   cd <project-folder>

   # Create virtual environment
   python3 -m venv venv
   source venv/bin/activate

   # Install dependencies
   pip install -r requirements.txt
   ```

3. **Configuration**
   - Create a Spotify App at [developer.spotify.com](https://developer.spotify.com/dashboard)
   - Set Redirect URI to `http://localhost:8501/` (or your deployed URL)
   - Create `.env` file:
     ```bash
     SPOTIPY_CLIENT_ID=your_id
     SPOTIPY_CLIENT_SECRET=your_secret
     SPOTIPY_REDIRECT_URI=http://localhost:8501/
     ```

## Usage

```bash
streamlit run app.py
```

## Deployment

To deploy on Streamlit Community Cloud:

1. Push this code to a GitHub repository.
2. Login to [Streamlit Cloud](https://streamlit.io/cloud).
3. Connect your GitHub and select the repository.
4. In the "Advanced Settings" of deployment, add your secrets:
   - `SPOTIPY_CLIENT_ID`
   - `SPOTIPY_CLIENT_SECRET`
   - `SPOTIPY_REDIRECT_URI` (Set this to your deployed app's URL)
   - **Important**: Update your Spotify Dashboard to include the new Deployed URL in Redirect URIs.

## Structure

- `app.py`: Main application logic
- `execution/`: Core logic modules
  - `spotify_auth.py`: Authentication handler
  - `spotify_search_artist.py`: Search functionality
  - `spotify_get_artist_tracks.py`: Algorithm to fetch tracks
  - `spotify_create_playlist.py`: Playlist management logic
