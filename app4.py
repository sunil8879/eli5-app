import streamlit as st
import google.generativeai as genai
from youtube_search import YoutubeSearch

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="ELI5 International",
    page_icon="🌏",
    layout="wide"
)

# --- 2. CUSTOM CSS ---
st.markdown("""
    <style>
    /* 1. Main Background: WHITE */
    .stApp {
        background-color: #FFFFFF;
    }

    /* 2. Text Color: Black */
    p, li, .stMarkdown {
        color: #000000 !important;
        font-weight: 600;
        font-size: 1.1rem;
        line-height: 1.6;
    }

    /* 3. HEADERS */
    h1, h2, h3 {
        color: #000000 !important;
        font-family: 'Verdana', sans-serif;
        font-weight: 900;
        text-shadow: 2px 2px 0px #CCCCCC; 
    }

    /* 4. SEARCH BOX: TURQUOISE (Standard Size) */
    .stTextInput > div > div > input {
        background-color: #40E0D0 !important; /* Turquoise */
        color: #000000 !important;             /* Black Text */
        font-weight: bold !important;
        border: 2px solid #000000 !important;  /* Black Border */
        border-radius: 10px;
        box-shadow: 3px 3px 0px rgba(0,0,0,0.2);
    }
    
    /* Placeholder color */
    ::placeholder {
        color: rgba(0,0,0,0.6) !important;
    }
    
    /* 5. Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #F0F0F0;
        border-radius: 15px;
        padding: 5px;
        border: 2px solid black;
    }
    .stTabs [data-baseweb="tab"] {
        color: #000000;
        font-weight: 800;
    }
    
    .block-container {
        padding-top: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. API SETUP ---
try:
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-flash-latest')
except:
    st.error("⚠️ API Key Missing! Check your Streamlit Secrets.")

# --- 4. THE LOGO ---
st.markdown("""
    <div style="text-align: center; margin-bottom: 30px;">
        <h1 style="font-size: 90px; margin: 0; line-height: 0.9;">
            ELI<span style="color: #FF4500;">5</span>
        </h1>
        <div style="
            background-color: #000000; 
            color: white; 
            display: inline-block; 
            padding: 8px 25px; 
            font-size: 20px; 
            font-weight: bold; 
            border-radius: 50px; 
            box-shadow: 3px 3px 0px #CCCCCC;
            transform: rotate(-3deg);
            margin-top: 10px;
        ">
            INTERNATIONAL EDITION 🌏
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- 5. SEARCH INPUT (WIDE) ---
# [1, 15, 1] ensures the search bar is WIDE (not 50%) but has tiny margins
col1, col2, col3 = st.columns([1, 15, 1])

with col2:
    query = st.text_input("Search Topic:", placeholder="e.g. Gravity...", label_visibility="collapsed")

# --- 6. LOGIC ---
if query:
    st.write("---") 
    
    with st.spinner('⚡ Brainstorming...'):
        
        # TABS
        tab1, tab2 = st.tabs(["📖 THE STORY", "📺 VISUALS"])

        # GENERATE CONTENT
        prompt = f"Explain '{query}' to a 5-year-old. Use a fun, energetic tone. Use simple analogies. Write roughly 400 words. Split into clear sections with bold headers."
        response = model.generate_content(prompt)
        
        clean_query = query.replace(" ", "-")
        image_url = f"https://image.pollinations.ai/prompt/3d-render-of-{clean_query}-bright-colors-pixar-style-white-background-4k"
        
        results = YoutubeSearch(query + " for kids", max_results=1).to_dict()

        # TAB 1: TEXT
        with tab1:
            st.markdown(response.text)

        # TAB 2: VISUALS
        with tab2:
            col_a, col_b = st.columns(2)
            
            with col_a:
                st.markdown("### 🎨 3D Drawing")
                st.image(image_url, use_container_width=True)
                
            with col_b:
                st.markdown("### 🎥 Explanation Video")
                if results:
                    video_id = results[0]['id']
                    st.video(f"https://www.youtube.com/watch?v={video_id}")
                else:
                    st.write("No video found.")
