import streamlit as st
import time
from execution import spotify_auth
from execution import spotify_search_artist
from execution import spotify_get_artist_tracks
from execution import spotify_create_playlist

# Page configuration
st.set_page_config(
    page_title="Spotify Playlist Creator",
    page_icon="🎵",
    layout="centered"
)

# Custom CSS
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        background-color: #1DB954;
        color: white;
        border-radius: 25px;
        border: none;
        padding: 10px 20px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #1ed760;
        color: white;
    }
    .artist-card {
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 10px;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

def main():
    st.title("🎵 Spotify Artist Playlist Creator")
    st.write("Generate a complete playlist of every song by your favorite artist.")

    # Check for authentication
    if 'token_info' not in st.session_state:
        # Check if we have a code from redirect
        query_params = st.query_params
        if "code" in query_params:
            code = query_params["code"]
            try:
                token_info = spotify_auth.get_token_from_code(code)
                st.session_state['token_info'] = token_info
                # Clear query params to clean URL
                st.query_params.clear()
                st.rerun()
            except Exception as e:
                st.error(f"Authentication failed: {str(e)}")
        else:
            # Show login button
            auth_url = spotify_auth.get_auth_url()
            
            # Use HTML link with target="_top" to break out of iframe (fix for Firefox/Streamlit Cloud)
            st.markdown(f"""
                <a href="{auth_url}" target="_top" style="text-decoration: none;">
                    <button style="
                        width: 100%;
                        background-color: #1DB954;
                        color: white;
                        border-radius: 25px;
                        border: none;
                        padding: 10px 20px;
                        font-weight: bold;
                        cursor: pointer;
                        font-family: inherit;
                        font-size: 1rem;
                    ">
                        Login with Spotify
                    </button>
                </a>
            """, unsafe_allow_html=True)
            
            st.info("Please login to verify your Spotify premium account and enable playlist creation.")
            return

    # Authenticated State
    token_info = st.session_state.get('token_info')
    sp, token_info = spotify_auth.get_spotify_client(token_info)
    
    # Update token in session if it was refreshed
    if token_info:
        st.session_state['token_info'] = token_info
    else:
        st.error("Session expired. Please reload and login again.")
        del st.session_state['token_info']
        st.rerun()

    # User Info
    try:
        user = sp.current_user()
        st.sidebar.image(user['images'][0]['url'] if user['images'] else "https://via.placeholder.com/150", width=50)
        st.sidebar.write(f"Logged in as **{user['display_name']}**")
        if st.sidebar.button("Logout"):
            del st.session_state['token_info']
            st.rerun()
    except Exception as e:
        st.error("Error fetching user info. Please re-login.")
        del st.session_state['token_info']
        st.rerun()

    # Application Logic
    artist_name = st.text_input("Enter Artist Name", placeholder="e.g. Wakadinali")

    if artist_name:
        # Search Artist
        if 'current_artist' not in st.session_state or st.session_state.current_artist['name'].lower() != artist_name.lower():
            with st.spinner(f"Searching for '{artist_name}'..."):
                results = spotify_search_artist.search_artist(sp, artist_name)
                
            if not results:
                st.warning("Artist not found. Please try again.")
            else:
                # If multiple results, let user choose (simplified: taking top result for now)
                # In a more advanced version, we'd show a grid to pick from
                artist = results[0]
                st.session_state['current_artist'] = artist
                
        # Display Artist Check
        if 'current_artist' in st.session_state:
            artist = st.session_state['current_artist']
            
            col1, col2 = st.columns([1, 2])
            with col1:
                if artist['image']:
                    st.image(artist['image'], width=150)
            with col2:
                st.subheader(artist['name'])
                st.write(f"Followers: {artist['followers']:,}")
                st.write(f"Popularity: {artist['popularity']}/100")
            
            # Create Playlist Button
            if st.button(f"Create '{artist['name']} - Complete' Playlist"):
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                def update_progress(msg):
                    status_text.write(msg)
                
                try:
                    # 1. Fetch Tracks
                    update_progress("Fetching artist discography...")
                    tracks = spotify_get_artist_tracks.get_all_artist_tracks(
                        sp, 
                        artist['id'], 
                        artist['name'],
                        progress_callback=update_progress
                    )
                    
                    if not tracks:
                        st.error("No tracks found for this artist.")
                        return

                    st.write(f"Found {len(tracks)} unique tracks.")
                    progress_bar.progress(50)
                    
                    # 2. Create Playlist
                    playlist_name = f"{artist['name']} - Complete Collection"
                    playlist_desc = f"All songs by {artist['name']}. Generated by Spotify Playlist Creator."
                    
                    update_progress(f"Creating playlist '{playlist_name}'...")
                    playlist = spotify_create_playlist.create_playlist_for_user(
                        sp, 
                        user['id'], 
                        playlist_name, 
                        playlist_desc
                    )
                    
                    # 3. Add Tracks
                    update_progress("Adding tracks to playlist...")
                    track_uris = [t['uri'] for t in tracks]
                    spotify_create_playlist.add_tracks_to_playlist(sp, playlist['id'], track_uris)
                    
                    progress_bar.progress(100)
                    status_text.success("Done!")
                    
                    # Success State
                    st.success(f"Playlist Created Successfully! ({len(tracks)} songs)")
                    st.markdown(f"### [Open on Spotify]({playlist['external_urls']['spotify']})")
                    st.balloons()
                    
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
