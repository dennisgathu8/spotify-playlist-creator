# Spotify Creator Xt 🎵

**The Premium Playlist Experience.**

Unlock the full potential of your music library with advanced filtering, East African Hip Hop discovery, and a sleek "Neon Noir" interface.

## ✨ Features

### 🌟 Discovery Center
- **East African Legends Wall**: One-click access to discographies of **E-Sir, Kalamashaka, Ukoo Flani**, and **Professor Jay**.
- **Smart Search**: Find any artist on Spotify with instant visual feedback.

### 🎚️ Playlist Studio
Once you select an artist, unlock pro-level tools:
- **Vibe Tuner**: Slider controls for **Energy** (Hype) and **Mood** (Happy/Sad).
- **💎 Deep Cuts Mode**: Automatically filter out the radio hits to find hidden gems.
- **📀 Era Selector**: Isolate tracks from specific years (e.g., Golden Era '95-'05).
- **Presets**: Instant "Party", "Sad", or "Old School" configurations.

### 🎨 Premium UI
- **Glassmorphism Design**: sleek dark mode with blur effects.
- **Responsive**: Works beautifully on desktop and mobile.

## 🚀 Deployment

### Prerequisites
- Python 3.8+
- Spotify Developer Credentials

### Local Setup
1. **Clone & Install**
   ```bash
   git clone <your-repo>
   pip install -r requirements.txt
   ```

2. **Configure Secrets**
   Create a `.env` file:
   ```bash
   SPOTIPY_CLIENT_ID=your_id
   SPOTIPY_CLIENT_SECRET=your_secret
   SPOTIPY_REDIRECT_URI=http://localhost:8501/
   ```

3. **Run**
   ```bash
   streamlit run app.py
   ```

## ☁️ Streamlit Cloud Deployment
1. Push this code to GitHub.
2. Connect your repo on [Streamlit Cloud](https://streamlit.io/cloud).
3. Add your secrets in the Advanced Settings.
4. Enjoy!
