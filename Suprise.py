import streamlit as st
import os
import uuid

# Set page configuration
st.set_page_config(
    page_title="Chapri Party Zone 🎉",
    page_icon="😎",
    layout="wide"
)

# Apply colorful and funny CSS styling
st.markdown(
    """
    <style>
    .main {
        background: linear-gradient(135deg, #ff6ec4, #7873f5, #00f7ff);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 0 20px rgba(0,0,0,0.3);
    }
    .title {
        color: #ffffff;
        font-family: 'Comic Sans MS', cursive, sans-serif;
        font-size: 3.5rem;
        text-align: center;
        text-shadow: 3px 3px #ff1744;
        animation: bounce 2s infinite;
    }
    .greeting {
        color: #00ff00;
        font-size: 6rem;
        font-family: 'Comic Sans MS', cursive, sans-serif;
        text-align: center;
        animation: pulse 1.5s infinite;
        margin-bottom: 20px;
    }
    .stButton>button {
        background-color: #ffeb3b;
        color: #d81b60;
        font-size: 1.2rem;
        font-weight: bold;
        border-radius: 10px;
        padding: 10px 20px;
        border: 2px solid #d81b60;
        transition: transform 0.2s;
        margin: 10px;
    }
    .stButton>button:hover {
        transform: scale(1.1);
        background-color: #d81b60;
        color: #ffeb3b;
    }
    .banger-button {
        background-color: #ff1744;
        color: white;
        padding: 10px 20px;
        border-radius: 10px;
        font-size: 1.2rem;
        font-weight: bold;
        cursor: pointer;
        display: block;
        text-align: center;
        margin: 20px auto;
    }
    .debug-text {
        color: #ffffff;
        font-family: 'Arial', sans-serif;
        background-color: rgba(0, 0, 0, 0.7);
        padding: 10px;
        border-radius: 5px;
        text-align: center;
    }
    @keyframes bounce {
        0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
        40% { transform: translateY(-20px); }
        60% { transform: translateY(-10px); }
    }
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.1); }
        100% { transform: scale(1); }
    }
    .fullscreen {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        background: linear-gradient(45deg, #ff0000, #00ff00, #0000ff);
        z-index: 1000;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Directory to store uploaded songs
UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# Initialize session state
if 'clicked' not in st.session_state:
    st.session_state.clicked = False
if 'song_path' not in st.session_state:
    # Check for existing audio files in the upload directory
    audio_files = [f for f in os.listdir(UPLOAD_DIR) if f.endswith(('.mp3', '.wav', '.ogg'))]
    st.session_state.song_path = os.path.join(UPLOAD_DIR, audio_files[0]) if audio_files else None
if 'show_uploader' not in st.session_state:
    st.session_state.show_uploader = False

# Function to toggle clicked state
def toggle_click():
    st.session_state.clicked = True
    st.session_state.show_uploader = False
    st.balloons()

# Function to toggle uploader visibility
def toggle_uploader():
    st.session_state.show_uploader = True

# Function to save uploaded song
def save_song(uploaded_file):
    try:
        # Generate unique filename using UUID to avoid overwrites
        file_extension = uploaded_file.name.split('.')[-1]
        song_path = os.path.join(UPLOAD_DIR, f"song_{uuid.uuid4()}.{file_extension}")
        with open(song_path, "wb") as f:
            f.write(uploaded_file.read())
        st.session_state.song_path = song_path
        st.markdown(
            """
            <p class="debug-text">
            Yo, Chapri! Your song is saved! To keep it FOREVER, download it below and commit it to GitHub! 🚀
            </p>
            """,
            unsafe_allow_html=True
        )
        return song_path
    except Exception as e:
        st.error(f"Oops, couldn’t save the song! 😿 Error: {str(e)}")
        return None

# Home page
if not st.session_state.clicked:
    # Title of the dashboard
    st.markdown('<h1 class="title">Welcome to the Dashboard! 🦄🎶</h1>', unsafe_allow_html=True)

    # Smash for Chapri button
    st.button("Smash for Chapri! 😜", key="greet_button", on_click=toggle_click)

# Greeting page
if st.session_state.clicked:
    # Full-screen greeting
    with st.container():
        st.markdown(
            """
            <div class="fullscreen">
                <h1 class="greeting">Hello Chapri! 🌈</h1>
                <button class="banger-button">Play Saved Banger! 🎵</button>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Play Saved Banger button functionality
    if st.button("Play Saved Banger! 🎵", key="play_saved_song", on_click=toggle_uploader):
        if st.session_state.song_path and os.path.exists(st.session_state.song_path):
            try:
                with open(st.session_state.song_path, "rb") as f:
                    st.audio(f.read(), format="audio/mp3")
                st.markdown('<p class="debug-text">Debug: Rockin’ the saved song! 🤘</p>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Can’t play the saved song! 😿 Error: {str(e)}")
        else:
            st.error("No saved banger found! Upload a song below! 😿")

    # Show file uploader only after clicking Play Saved Banger
    if st.session_state.show_uploader:
        uploaded_file = st.file_uploader(
            "Upload your banger song! 🎵 (MP3, WAV, etc.)",
            type=["mp3", "wav", "ogg"],
            key="audio_uploader"
        )
        if uploaded_file is not None:
            song_path = save_song(uploaded_file)
            if song_path:
                with open(song_path, "rb") as f:
                    st.audio(f.read(), format=uploaded_file.type)
                st.download_button(
                    label="Download Your Banger! 💾",
                    data=open(song_path, "rb"),
                    file_name=uploaded_file.name,
                    mime=uploaded_file.type,
                    key="download_song"
                )
