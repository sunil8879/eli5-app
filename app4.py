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
        font-size: 1.15rem;
        line-height: 1.6;
    }

    /* 3. HEADERS: Clean 3D Look */
    h1, h2, h3 {
        color: #000000 !important;
        font-family: 'Verdana', sans-serif;
        font-weight: 900;
        letter-spacing: 0.5px;
        text-shadow: 2px 2px 0px #CCCCCC; /* Light gray shadow for white bg */
    }

    /* 4. SEARCH BOX: TURQUOISE & JUMBO SIZE */
    .stTextInput > div > div > input {
        background-color: #40E0D0 !important; /* Turquoise Color */
        color: #000000 !important;             /* Black Font */
        font-weight: 900 !important;           /* Extra Bold */
        font-size: 28px !important;            /* Big Font */
        height: 70px !important;               /* Tall Box */
        padding: 10px 20px !important;
        border: 4px solid #000000 !important;  /* Thick Black Border */
        border-radius: 20px;
        box-shadow: 5px 5px 0px rgba(0,0,0,0.2); 
    }
    
    /* Change the placeholder text color (so it's visible on Turquoise) */
    ::placeholder {
        color: rgba(0,0,0,0.6) !important;
        font-weight: normal;
    }
    
    /* 5. Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #F0F0F0;
        border-radius: 15px;
        padding: 10px;
        border: 2px solid black;
    }
    .stTabs [data-baseweb="tab"] {
        color: #000000;
        font-weight: 800;
        font-size: 1.2rem;
    }
    
    /* 6. Logo Spacing */
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

# --- 4. THE TILTED LOGO ---
st.markdown("""
    <div style="text-align: center; margin-bottom: 40px;">
        <h1 style="font-size: 100px; margin: 0; line-height: 0.9;">
            ELI<span style="color: #FF4500;">5</span>
        </h1>
        <div style="
            background-color: #000000; 
            color: white; 
            display: inline-block; 
            padding: 12px 35px; 
            font-size: 24px; 
            font-weight: bold; 
            border-radius: 50px; 
            box-shadow: 4px 4px 0px #CCCCCC;
            transform: rotate(-3deg);
            margin-top: 10px;
        ">
            INTERNATIONAL EDITION 🌏
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- 5. SEARCH INPUT ---
# Using the Wide Columns [1, 10, 1] logic so it fills the screen well
col1, col2, col3 = st.columns([1, 10, 1])

with col2:
    query = st.text_input("Search Topic:", placeholder="Type here (e.g. Gravity)...", label_visibility="collapsed")

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
        # Image
        image_url = f"https://image.pollinations.ai/prompt/3d-render-of-{clean_query}-bright-colors-pixar-style-white-background-4k"
        
        # Video
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
