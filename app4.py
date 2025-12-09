import streamlit as st
import google.generativeai as genai
from youtube_search import YoutubeSearch

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="ELI5 International",
    page_icon="🌏",
    layout="wide"
)

# --- 2. THE DESIGNER CSS (The Magic) ---
st.markdown("""
    <style>
    /* 1. BACKGROUND: Aquamarine with a Retro Grid Pattern */
    .stApp {
        background-color: #7FFFD4;
        background-image: 
            linear-gradient(rgba(255,255,255,0.5) 2px, transparent 2px),
            linear-gradient(90deg, rgba(255,255,255,0.5) 2px, transparent 2px);
        background-size: 40px 40px; /* Makes the grid squares */
    }

    /* 2. JUMBO SEARCH BAR */
    .stTextInput > div > div > input {
        font-size: 28px !important;  /* Huge Text */
        height: 70px !important;     /* Tall Box */
        padding: 10px 20px !important;
        background-color: #FFFFFF !important;
        border: 4px solid #000000 !important; /* Thick Black Border */
        border-radius: 50px !important; /* Rounded Pills */
        box-shadow: 6px 6px 0px rgba(0,0,0,0.2) !important;
        color: #000000 !important;
    }
    
    /* 3. HEADERS */
    h1, h2, h3 {
        color: #000000 !important;
        font-family: 'Verdana', sans-serif;
        font-weight: 900;
        text-shadow: 3px 3px 0px #FFFFFF;
    }

    /* 4. RESULT CARDS (The white boxes) */
    .result-card {
        background-color: #FFFFFF;
        border: 3px solid #000000;
        border-radius: 15px;
        padding: 25px;
        box-shadow: 8px 8px 0px rgba(0,0,0,0.15);
        color: #000000;
        font-size: 1.3rem; /* Bigger Font */
        line-height: 1.6;
        margin-bottom: 20px;
    }

    /* 5. TABS Styling */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #FFFFFF;
        border-radius: 50px;
        border: 3px solid black;
        padding: 5px;
        box-shadow: 4px 4px 0px rgba(0,0,0,0.2);
    }
    .stTabs [data-baseweb="tab"] {
        font-size: 1.2rem;
        font-weight: bold;
        color: black;
    }
    
    /* Hide the top colored bar */
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- 3. API SETUP ---
# Securely read key from Secrets
try:
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-flash-latest')
except:
    st.error("🚨 API Key not found! Please check your Streamlit Secrets.")

# --- 4. THE LOGO SECTION ---
st.markdown("""
    <div style="text-align: center; padding-top: 20px; padding-bottom: 20px;">
        <h1 style="font-size: 100px; margin: 0; line-height: 0.9;">
            ELI<span style="color: #FF4500;">5</span>
        </h1>
        <div style="
            background-color: #000000; 
            color: white; 
            display: inline-block; 
            padding: 10px 30px; 
            font-size: 22px; 
            font-weight: bold; 
            border-radius: 50px; 
            box-shadow: 4px 4px 0px #FFFFFF;
            transform: rotate(-2deg);
        ">
            INTERNATIONAL EDITION 🌏
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- 5. THE JUMBO SEARCH ---
# We use columns to center the search bar nicely
col_left, col_center, col_right = st.columns([1, 6, 1])

with col_center:
    query = st.text_input("Search", placeholder="Type a topic (e.g. Gravity)...", label_visibility="collapsed")

# --- 6. THE RESULTS LOGIC ---
if query:
    st.write("") # Spacer
    st.write("") 
    
    with st.spinner('🚀 Launching AI Research...'):
        
        # 1. Get Text
        prompt = f"Explain '{query}' to a 5-year-old. Use a fun, energetic tone. Use simple analogies. Write roughly 400 words. Split into clear sections with bold headers."
        try:
            response = model.generate_content(prompt)
            text_response = response.text
        except:
            text_response = "Sorry, I'm having trouble thinking right now. Try again!"

        # 2. Get Image Link
        clean_query = query.replace(" ", "-")
        image_url = f"https://image.pollinations.ai/prompt/3d-render-of-{clean_query}-bright-colors-pixar-style-clean-background-4k-soft-lighting"
        
        # 3. Get Video
        try:
            results = YoutubeSearch(query + " explanation for kids", max_results=1).to_dict()
        except:
            results = None

        # --- DISPLAY RESULTS ---
        
        # We create the tabs
        tab1, tab2 = st.tabs(["📖 READ THE STORY", "📺 WATCH & SEE"])

        with tab1:
            # We wrap the text in a custom white card using HTML
            st.markdown(f"""
                <div class="result-card">
                    {text_response}
                </div>
            """, unsafe_allow_html=True)

        with tab2:
            col_a, col_b = st.columns(2)
            
            with col_a:
                st.markdown('<div class="result-card" style="text-align: center;"><h3>🎨 AI Drawing</h3></div>', unsafe_allow_html=True)
                st.image(image_url, use_container_width=True)
                
            with col_b:
                st.markdown('<div class="result-card" style="text-align: center;"><h3>🎥 Video Clip</h3></div>', unsafe_allow_html=True)
                if results:
                    video_id = results[0]['id']
                    st.video(f"https://www.youtube.com/watch?v={video_id}")
                else:
                    st.write("No video found.")
