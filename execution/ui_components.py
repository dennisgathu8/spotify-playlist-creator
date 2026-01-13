import streamlit as st

def get_custom_css():
    """
    Returns the global CSS for the 'Neon Noir' theme.
    """
    return """
    <style>
    /* Global Theme Overrides */
    .stApp {
        background-color: #121212;
        color: #FFFFFF;
    }
    
    /* Buttons */
    .stButton>button {
        background-color: #1DB954;
        color: white;
        border-radius: 500px;
        border: none;
        padding: 12px 24px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #1ed760;
        transform: scale(1.05);
        box-shadow: 0 4px 15px rgba(29, 185, 84, 0.4);
    }
    
    /* Inputs */
    .stTextInput>div>div>input {
        background-color: #282828 !important;
        color: white !important;
        border: 1px solid #404040;
        border-radius: 4px;
    }
    .stTextInput>div>div>input:focus {
        border-color: #1DB954;
        box-shadow: none;
    }
    
    /* Custom Card Containers */
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
        transition: transform 0.2s;
    }
    .glass-card:hover {
        transform: translateY(-2px);
        background: rgba(255, 255, 255, 0.08);
    }
    
    /* Text Styling */
    h1, h2, h3 {
        font-family: 'Circular', -apple-system, BlinkMacSystemFont, Roboto, Helvetica, Arial, sans-serif;
        font-weight: 700 !important; 
    }
    
    /* Progress Bars */
    .stProgress > div > div > div > div {
        background-color: #1DB954;
    }
    </style>
    """

def render_artist_header(artist):
    """
    Renders a hero header for the selected artist.
    """
    if not artist:
        return ""
    
    image_url = artist['image'] if artist['image'] else "https://via.placeholder.com/300"
    
    return st.markdown(f"""
        <div style="
            display: flex; 
            align-items: center; 
            background: linear-gradient(180deg, rgba(83, 83, 83, 1) 0%, #121212 100%);
            padding: 40px; 
            border-radius: 8px;
            margin-bottom: 20px;
        ">
            <img src="{image_url}" style="
                width: 200px; 
                height: 200px; 
                border-radius: 50%; 
                object-fit: cover; 
                box-shadow: 0 8px 24px rgba(0,0,0,0.5);
                margin-right: 32px;
            ">
            <div>
                <h6 style="color: #fff; text-transform: uppercase; font-weight: 700; margin: 0;">Artist</h6>
                <h1 style="color: #fff; font-size: 4rem; margin: 8px 0;">{artist['name']}</h1>
                <p style="color: #b3b3b3; margin: 0;">
                    {artist['followers']:,} Followers • {artist['popularity']}% Popularity
                </p>
            </div>
        </div>
    """, unsafe_allow_html=True)

def render_legend_card(name, image_url, description):
    """
    Renders a clickable card for a Legend.
    Note: Since we can't easily put buttons inside custom HTML in Streamlit without components,
    we will use this mainly for visual display, and use standard buttons below it.
    """
    st.markdown(f"""
        <div class="glass-card" style="text-align: center;">
            <img src="{image_url}" style="
                width: 120px; 
                height: 120px; 
                border-radius: 50%; 
                object-fit: cover; 
                margin-bottom: 16px;
                border: 2px solid #1DB954;
            ">
            <h3 style="margin: 0; color: white;">{name}</h3>
            <p style="color: #b3b3b3; font-size: 0.9em;">{description}</p>
        </div>
    """, unsafe_allow_html=True)

def render_track_stat(label, value, color="#1DB954"):
    """
    Renders a small circular stat (like for Vibes).
    """
    st.markdown(f"""
        <div style="text-align: center;">
            <div style="
                font-size: 24px; 
                font-weight: bold; 
                color: {color};
            ">{value}</div>
            <div style="
                font-size: 12px; 
                color: #b3b3b3; 
                text-transform: uppercase;
            ">{label}</div>
        </div>
    """, unsafe_allow_html=True)
