import streamlit as st

from execution import spotify_auth
from execution import spotify_search_artist
from execution import spotify_get_artist_tracks
from execution import spotify_create_playlist
from execution import ui_components
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Spotify Creator Xt",
    page_icon="🎵",
    layout="wide", # Switch to wide mode for the dashboard feel
    initial_sidebar_state="expanded"
)

# Apply "Neon Noir" Theme
st.markdown(ui_components.get_custom_css(), unsafe_allow_html=True)

# East African Legends Data
# East African Hip Hop Data
EAST_AFRICA_ARTISTS = {
    "Kenyan Legends (The OGs)": [
        {"name": "E-Sir", "img": "https://i.scdn.co/image/ab67616d0000b2732924151fb789648937996c97", "desc": "The South C Finest. Creating timeless bangers."},
        {"name": "Kalamashaka", "img": "https://i.scdn.co/image/ab67616d0000b273c501173aa447d92823053303", "desc": "Pioneering Dandora Hip Hop."},
        {"name": "Ukoo Flani", "img": "https://i.scdn.co/image/ab67616d0000b27344443916295574514571de43", "desc": "The Mau Mau Camp Masters."},
        {"name": "Juacali", "img": "https://i.scdn.co/image/ab67616d0000b273f1f9bf90f2819d2f600d240e", "desc": "King of Genge. Bidii Yangu."},
        {"name": "Nonini", "img": "https://i.scdn.co/image/ab6761610000e5ebc2a38a8c31361fc51824a70c", "desc": "The Godfather of Genge."},
        {"name": "Nameless", "img": "https://i.scdn.co/image/ab6761610000e5eb4f3d2f913612502802279124", "desc": "Megarider Legend."},
    ],
    "Tanzanian Titans": [
        {"name": "Professor Jay", "img": "https://i.scdn.co/image/ab67616d0000b273e925c4efc687258455855239", "desc": "Heavyweight MC. Bongo Flava Pioneer."},
        {"name": "Juma Nature", "img": "https://i.scdn.co/image/ab67616d0000b2731874b335607da61688fa900e", "desc": "Sir Nature. Temeke's Finest."},
        {"name": "Fid Q", "img": "https://i.scdn.co/image/ab6761610000e5eb232e9f688f87a8f3794f2fce", "desc": "The strict lyricist of Bongo Hip Hop."},
        {"name": "AY", "img": "https://i.scdn.co/image/ab6761610000e5eb6ffd0cfc0bffa61a16821941", "desc": "Commercial Hip Hop Pioneer."},
        {"name": "Mwana FA", "img": "https://i.scdn.co/image/ab6761610000e5eb13b578c95bdeba723f533b41", "desc": "The lyrical poet. Binamu."},
    ],
    "New Wave (Sheng Masters)": [
        {"name": "Wakadinali", "img": "https://i.scdn.co/image/ab6761610000e5eb7418e987f9f29992ba9bb9a1", "desc": "Rong Rende. Drill Kings."},
        {"name": "Khaligraph Jones", "img": "https://i.scdn.co/image/ab6761610000e5eb36ce86bbce174db5a330cdbc", "desc": "The OG. Respect the Jones."},
        {"name": "Nyashinski", "img": "https://i.scdn.co/image/ab6761610000e5eb352136e0bfbb563378d30e38", "desc": "From Klepto to Solo King."},
        {"name": "Breeder LW", "img": "https://i.scdn.co/image/ab6761610000e5eb832cb1fabae29508ac893183", "desc": "Bazenga Daddii."},
    ]
}

def main():
    # Auth Flow (Preserved)
    if 'token_info' not in st.session_state:
        query_params = st.query_params
        if "code" in query_params:
            code = query_params["code"]
            try:
                token_info = spotify_auth.get_token_from_code(code)
                st.session_state['token_info'] = token_info
                st.query_params.clear()
                st.rerun()
            except Exception as e:
                st.error(f"Authentication failed: {str(e)}")
        else:
            try:
                auth_url = spotify_auth.get_auth_url()
                # Use a cleaner login page for the landing
                col1, col2, col3 = st.columns([1,2,1])
                with col2:
                    st.title("🎵 Spotify Creator Xt")
                    st.write("Unlock the full potential of your music library.")
                    st.markdown(f'<a href="{auth_url}" target="_blank" class="stButton"><button style="width:100%">LOGIN WITH SPOTIFY</button></a>', unsafe_allow_html=True)
                    st.info("Premium Account required for full playback features.")
                return
            except Exception as e:
                st.error(f"Config Error: {e}")
                return

    # Authenticated
    token_info = st.session_state.get('token_info')
    sp, token_info = spotify_auth.get_spotify_client(token_info)
    if token_info:
        st.session_state['token_info'] = token_info
    else:
        st.session_state.pop('token_info', None)
        st.rerun()

    # --- MAIN APP UI ---
    
    # Sidebar: User & Nav
    with st.sidebar:
        try:
            user = sp.current_user()
            st.image(user['images'][0]['url'] if user['images'] else "https://via.placeholder.com/150", width=60)
            st.write(f"Logged in as **{user['display_name']}**")
            # Clear old session data if switching users
            if 'current_user_id' not in st.session_state:
                st.session_state['current_user_id'] = user['id']
            elif st.session_state['current_user_id'] != user['id']:
                st.session_state.clear()
                st.rerun()
                
            if st.button("Logout", key="logout_btn"):
                st.session_state.clear()
                st.rerun()
        except:
            st.warning("Needs Re-login")
        
        st.divider()
        if st.button("🏠 Home / Search", use_container_width=True):
            st.session_state.pop('current_artist', None)
            st.rerun()

    # Search Processing
    if 'current_artist' not in st.session_state:
        st.title("🎧 Discovery Center")
        
        # Search Bar
        col1, col2 = st.columns([3, 1])
        with col1:
            search_query = st.text_input("Search for an artist...", placeholder="e.g. Sauti Sol")
        with col2:
            st.write("") 
            st.write("")
            if st.button("GO", key="search_btn", use_container_width=True):
                if search_query:
                    with st.spinner("Searching..."):
                        results = spotify_search_artist.search_artist(sp, search_query)
                        if results:
                            st.session_state['current_artist'] = results[0]
                            st.rerun()
                        else:
                            st.error("Artist not found!")

        st.divider()
        st.divider()
        st.subheader("East African Hip Hop Hall of Fame")
        st.write("Curated selections from across the region.")
        
        for category, artists in EAST_AFRICA_ARTISTS.items():
            st.markdown(f"### {category}")
            # Dynamic columns based on count, wrapping every 4
            cols = st.columns(4)
            for idx, legend in enumerate(artists):
                col_idx = idx % 4
                if idx > 0 and col_idx == 0:
                     # Create new row every 4 items
                     cols = st.columns(4)
                
                with cols[col_idx]:
                    ui_components.render_legend_card(legend['name'], legend['img'], legend['desc'])
                    # Unique key for every button
                    btn_key = f"btn_{legend['name'].replace(' ', '_')}"
                    if st.button(f"Select {legend['name']}", key=btn_key):
                        with st.spinner(f"Loading {legend['name']}..."):
                            results = spotify_search_artist.search_artist(sp, legend['name'])
                            if results:
                                st.session_state['current_artist'] = results[0]
                                st.rerun()

    else:
        # --- ARTIST STUDIO VIEW ---
        artist = st.session_state['current_artist']
        
        # Hero Header
        ui_components.render_artist_header(artist)
        
        # --- PLAYLIST STUDIO SIDEBAR ---
        with st.sidebar:
            st.divider()
            st.subheader("🎚️ Playlist Studio")
            
            # PRESETS
            st.write("Presets")
            preset_cols = st.columns(2)
            with preset_cols[0]:
                if st.button("🕺 Party"):
                    st.session_state['vibe_energy'] = (0.6, 1.0)
                    st.session_state['vibe_dance'] = (0.6, 1.0)
            with preset_cols[1]:
                if st.button("🌧️ Sad"):
                    st.session_state['vibe_energy'] = (0.0, 0.4)
                    st.session_state['vibe_valence'] = (0.0, 0.3)
            
            # Old School Preset (1995-2010)
            if st.button("📀 Old School"):
                 st.session_state['era_range'] = (1995, 2010)

            st.write("Custom Tunes")
            
            # 1. Vibes
            vibe_energy = st.slider("Energy (Hype)", 0.0, 1.0, st.session_state.get('vibe_energy', (0.0, 1.0)), 0.1)
            vibe_valence = st.slider("Mood (Sad ↔ Happy)", 0.0, 1.0, st.session_state.get('vibe_valence', (0.0, 1.0)), 0.1)
            
            # 2. Deep Cuts
            deep_cuts = st.checkbox("💎 Deep Cuts (Hidden Gems)", value=False, help="Removes the top 40% most popular tracks.")
            
            # 3. Era
            current_year = datetime.now().year
            # Load from session if set by preset, else default
            default_era = st.session_state.get('era_range', (1990, current_year))
            era_range = st.slider("Era (Year)", 1990, current_year, default_era)
            
        # --- DATA FETCHING & FILTERING ---
        if 'tracks_cache' not in st.session_state or st.session_state.get('tracks_artist_id') != artist['id']:
            with st.status("Fetching Discography & Analyzing Vibes...", expanded=True) as status:
                tracks = spotify_get_artist_tracks.get_all_artist_tracks(
                    sp, 
                    artist['id'], 
                    artist['name'],
                    progress_callback=lambda msg: status.write(msg)
                )
                st.session_state['tracks_cache'] = tracks
                st.session_state['tracks_artist_id'] = artist['id']
                status.update(label="Analysis Complete!", state="complete", expanded=False)
        
        all_tracks = st.session_state['tracks_cache']
        
        # APPLY FILTERS
        filtered_tracks = []
        for t in all_tracks:
            # 1. Era Filter
            track_year = t.get('release_year', 2000)
            if not (era_range[0] <= track_year <= era_range[1]):
                continue

            # 2. Vibe Filter
            energy = t.get('energy', 0.5)
            valence = t.get('valence', 0.5)
            
            if not (vibe_energy[0] <= energy <= vibe_energy[1]):
                continue
            if not (vibe_valence[0] <= valence <= vibe_valence[1]):
                continue

            # 3. Deep Cuts Filter (Remove popular tracks)
            # Threshold: > 60 is usually a "hit" or at least very well known
            popularity = t.get('popularity', 0)
            if deep_cuts and popularity > 60:
                continue
                
            filtered_tracks.append(t)
            
        st.subheader(f"Playlist Preview ({len(filtered_tracks)} tracks)")
        
        # Create Playlist Action
        if st.button(f"Create Playlist ({len(filtered_tracks)} Songs)", type="primary", use_container_width=True):
            if not filtered_tracks:
                st.error("No tracks match your filters!")
            else:
                try:
                    playlist_name = f"{artist['name']} - Custom Mix"
                    desc = f"Generated by Spotify Creator Xt. Filters: Energy={vibe_energy}, Mood={vibe_valence}, Era={era_range}"
                    playlist = spotify_create_playlist.create_playlist_for_user(sp, user['id'], playlist_name, desc)
                    
                    uris = [t['uri'] for t in filtered_tracks]
                    # Batch add (Spotify limit 100)
                    for i in range(0, len(uris), 100):
                        spotify_create_playlist.add_tracks_to_playlist(sp, playlist['id'], uris[i:i+100])
                        
                    st.balloons()
                    st.success(f"Playlist '{playlist_name}' Created!")
                    st.markdown(f"### [Open on Spotify]({playlist['external_urls']['spotify']})")
                except Exception as e:
                    st.error(f"Error: {e}")

        # Track List Table
        if filtered_tracks:
            display_data = [{
                "Title": t['name'], 
                "Year": t.get('release_year', '-'),
                "Pop": t.get('popularity', '-'),
                "Energy": f"{int(t.get('energy',0)*100)}%",
                "Mood": f"{int(t.get('valence',0)*100)}%"
            } for t in filtered_tracks]
            st.dataframe(display_data, use_container_width=True, hide_index=True)

if __name__ == "__main__":
    main()
