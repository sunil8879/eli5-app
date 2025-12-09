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
# NOTE: Replace this placeholder key with your actual Gemini API Key
GOOGLE_API_KEY = "AIzaSyCDbYrDJmKoVRhUGKK0hF6fue4Ayg7keKs" 

try:
    genai.configure(api_key=GOOGLE_API_KEY)
    # Using 'gemini-pro' for general explanation tasks
    model = genai.GenerativeModel('gemini-pro')
except:
    st.error("⚠️ API Key Missing or Invalid. Please check the setup.")

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


# --- 4.5. APP INTRODUCTION (New Section) ---
st.markdown("""
    <div style="background-color: #1877F2; padding: 20px; border-radius: 15px; border: 3px dashed #FF4500; margin-bottom: 40px;">
        <h2 style="text-align: center; color: #FF4500; text-shadow: none; margin-top: 0;">
            Welcome to the Simplest Corner of the Internet! 🧠
        </h2>
        <p style="text-align: center; color: #FFFFFF; font-size: 1.1rem; font-weight: 700;">
            Have you ever wondered how something works, but all the answers felt like they were written in a secret adult code? 🤯
        </p>
        <p style="text-align: center; color: #FFFFFF; font-size: 1.1rem; font-weight: 700;">
            We use the power of AI to break down the biggest ideas—from **Black Holes** to **Bitcoin**—into stories so easy, even a 5-year-old can understand!
        </p>
        <p style="text-align: center; color: #FFFFFF; font-size: 1.1rem; font-weight: 700;">
            Just type your topic into the **magical turquoise box** below and prepare for a fun explanation, a cool 3D picture, and a perfect video. Let's learn! 👇
        </p>
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
            prompt = f"Explain '{query}' to a 5-year-old. Use a fun, engaging tone. Keep the explanation concise, around 300 words, using simple analogies."
            response = model.generate_content(prompt)
            text_response = response.text
        except Exception as e:
            # Fallback text if the API fails (e.g., Error 429)
            text_response = f"""
            ### 🚦 High Traffic Alert!
            
            **Google's AI brain is taking a quick nap** because we made too many requests too fast (Error 429: {e}).
            
            Don't worry! Your **Images** and **Videos** below are still working perfectly. 👇
            
            *(Please wait 60 seconds and search again to get the text back!)*
            """

        # 2. GENERATE IMAGE (Uses the Pollinations API, which is external and free)
        clean_query = query.replace(" ", "-")
        image_url = f"https://image.pollinations.ai/prompt/3d-render-of-{clean_query}-bright-colors-pixar-style-white-background-4k"
        
        # 3. SEARCH VIDEO (Uses Youtube Search Library)
        results = None
        try:
            # Search for videos suitable for kids
            results = YoutubeSearch(query + " for kids", max_results=1).to_dict()
        except Exception as e:
            # Error handling for the video search itself
            st.error(f"Video search failed: {e}")

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
                st.image(image_url, use_container_width=True, caption=f"A 3D image of '{query}'")
                
            with col_b:
                st.markdown("### 🎥 Explanation Video")
                if results and results[0].get('id'):
                    video_id = results[0]['id']
                    # Use the standard YouTube embed format
                    st.video(f"https://www.youtube.com/watch?v={video_id}")
                else:
                    st.write("No suitable video found.")

