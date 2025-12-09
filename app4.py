import streamlit as st
import google.generativeai as genai
from youtube_search import YoutubeSearch

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="ELI5 Pro",
    page_icon="🧠",
    layout="wide"
)

# --- 2. CUSTOM CSS (Cleaned Up 3D) ---
st.markdown("""
    <style>
    /* 1. Main Background: Aquamarine */
    .stApp {
        background-color: #7FFFD4;
    }

    /* 2. Text Color: Black & Readable */
    p, li, .stMarkdown {
        color: #000000 !important;
        font-weight: 600;
        font-size: 1.15rem;
        line-height: 1.6;
    }

    /* 3. HEADERS: Clean 3D Bevel (No Blurry Shadow) */
    h1, h2, h3 {
        color: #000000 !important;
        font-family: 'Verdana', sans-serif; /* Clean, wide font */
        font-weight: 900;
        letter-spacing: 0.5px;
        /* The "Clean Bevel" 3D Effect */
        text-shadow: 2px 2px 0px #FFFFFF; 
    }

    /* 4. Search Bar: Clean White Box */
    .stTextInput > div > div > input {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        font-weight: bold;
        border: 2px solid #000000;
        border-radius: 12px;
        /* Sharp simple shadow */
        box-shadow: 4px 4px 0px rgba(0,0,0,0.2); 
    }
    
    /* 5. Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        background-color: rgba(255,255,255, 0.5);
        border-radius: 15px;
        padding: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        color: #000000;
        font-weight: 800;
        font-size: 1.2rem;
    }
    
    /* 6. Remove default top padding to make logo look better */
    .block-container {
        padding-top: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. API SETUP ---
# PASTE YOUR KEY HERE
GOOGLE_API_KEY = "AIzaSyCDbYrDJmKoVRhUGKK0hF6fue4Ayg7keKs" 

try:
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-flash-latest')
except:
    st.error("⚠️ API Key Missing")

# --- 4. THE CLEAN 3D LOGO ---
st.markdown("""
    <div style="text-align: center; margin-bottom: 30px;">
        <!-- The Main 3D Text -->
        <h1 style="font-size: 90px; margin: 0; line-height: 1.0; text-shadow: 4px 4px 0px #FFFFFF;">
            ELI<span style="color: #FF4500; text-shadow: 4px 4px 0px #FFFFFF;">5</span>
        </h1>
        <!-- The Subtitle (Sticker Style) -->
        <div style="
            background-color: #000000; 
            color: #FFFFFF; 
            display: inline-block; 
            padding: 8px 20px; 
            font-weight: bold; 
            font-size: 20px;
            border-radius: 50px;
            box-shadow: 3px 3px 0px #FFFFFF;
            margin-top: 10px;
        ">
            EXPLAIN LIKE I'M FIVE
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- 5. SEARCH INPUT ---
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    query = st.text_input("Search Topic:", placeholder="e.g. Gravity, Moon, Money...", label_visibility="collapsed")

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
        # Updated Image Prompt for cleaner look
        image_url = f"https://image.pollinations.ai/prompt/3d-render-of-{clean_query}-bright-colors-pixar-style-clean-background-4k"
        
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
