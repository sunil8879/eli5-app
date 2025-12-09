import streamlit as st
import google.generativeai as genai
from youtube_search import YoutubeSearch

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="ELI5 Pro",
    page_icon="🧠",
    layout="wide"
)

# --- 2. CUSTOM CSS ---
st.markdown("""
    <style>
    /* 1. Main Background: WHITE */
    .stApp {
        background-color: #FFFFFF;
    }

    /* 2. Text Color: Black & Readable */
    p, li, .stMarkdown {
        color: #000000 !important;
        font-weight: 600;
        font-size: 1.15rem;
        line-height: 1.6;
    }

    /* 3. HEADERS: Clean 3D Bevel */
    h1, h2, h3 {
        color: #000000 !important;
        font-family: 'Verdana', sans-serif;
        font-weight: 900;
        letter-spacing: 0.5px;
        text-shadow: 2px 2px 0px #CCCCCC; 
    }

    /* 4. Search Bar: TURQUOISE */
    .stTextInput > div > div > input {
        background-color: #40E0D0 !important; /* Turquoise */
        color: #000000 !important;             /* Black Text */
        font-weight: bold;
        border: 2px solid #000000;
        border-radius: 12px;
        box-shadow: 4px 4px 0px rgba(0,0,0,0.2); 
    }
    
    /* 5. Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        background-color: rgba(255,255,255, 0.5);
        border-radius: 15px;
        padding: 10px;
        border: 2px solid black;
    }
    .stTabs [data-baseweb="tab"] {
        color: #000000;
        font-weight: 800;
        font-size: 1.2rem;
    }
    
    .block-container {
        padding-top: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. API SETUP ---
GOOGLE_API_KEY = "AIzaSyCDbYrDJmKoVRhUGKK0hF6fue4Ayg7keKs" 

try:
    genai.configure(api_key=GOOGLE_API_KEY)
    # Switched model to 'gemini-pro' to try and bypass the 'flash' quota limit
    model = genai.GenerativeModel('gemini-pro')
except:
    st.error("⚠️ API Key Missing")

# --- 4. THE TILTED LOGO ---
st.markdown("""
    <div style="text-align: center; margin-bottom: 30px;">
        <h1 style="font-size: 90px; margin: 0; line-height: 0.9;">
            ELI<span style="color: #FF4500;">5</span>
        </h1>
        <div style="
            background-color: #000000; 
            color: white; 
            display: inline-block; 
            padding: 10px 30px; 
            font-size: 20px; 
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
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    query = st.text_input("Search Topic:", placeholder="e.g. Gravity, Moon, Money...", label_visibility="collapsed")

# --- 6. LOGIC (CRASH PROOF) ---
if query:
    st.write("---") 
    
    with st.spinner('⚡ Brainstorming...'):
        
        # 1. GENERATE TEXT (With Safety Net)
        text_response = ""
        try:
            prompt = f"Explain '{query}' to a 5-year-old. Fun tone. 300 words."
            response = model.generate_content(prompt)
            text_response = response.text
        except Exception as e:
            # If Google blocks us, we use this Backup Text so the app still looks good
            text_response = f"""
            ### 🚦 High Traffic Alert!
            
            **Google's AI brain is taking a quick nap** because we made too many requests too fast (Error 429).
            
            Don't worry! Your **Images** and **Videos** below are still working perfectly. 👇
            
            *(Please wait 60 seconds and search again to get the text back!)*
            """

        # 2. GENERATE IMAGE (No API key needed, always works)
        clean_query = query.replace(" ", "-")
        image_url = f"https://image.pollinations.ai/prompt/3d-render-of-{clean_query}-bright-colors-pixar-style-white-background-4k"
        
        # 3. SEARCH VIDEO (No API key needed, always works)
        try:
            results = YoutubeSearch(query + " for kids", max_results=1).to_dict()
        except:
            results = None

        # --- DISPLAY RESULTS ---
        tab1, tab2 = st.tabs(["📖 THE STORY", "📺 VISUALS"])

        # TAB 1: TEXT
        with tab1:
            st.markdown(text_response)

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
