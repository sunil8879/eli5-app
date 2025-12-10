import streamlit as st
import google.generativeai as genai
from youtube_search import YoutubeSearch

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="ELI5 Pro",
    page_icon="🧠",
    layout="wide"
)

# --- CATEGORY DEFINITIONS ---
SUB_CATEGORIES = {
    "Science": [
        "Gravity", "Photosynthesis", "Black Holes", "Microbes/Germs", "Evolution",
        "Atoms and Molecules", "The Human Heart", "Vaccines", "Sound Waves", "Light"
    ],
    "Technology": [
        "Artificial Intelligence (AI)", "Robotics", "How Computers Work", "Blockchain",
        "Virtual Reality (VR)", "3D Printing", "Social Media", "Bluetooth", 
        "Self-Driving Cars", "Algorithms"
    ],
    "History": [
        "The Roman Empire", "Ancient Egypt", "Medieval Castles", "World War II", 
        "The Dinosaurs (Extinction)", "The First Moon Landing", "How Fire Was Discovered", 
        "The Titanic", "The Great Wall of China", "Famous Explorers"
    ],
    "Geography": [
        "Volcanoes", "Deserts", "The North Pole", "Ocean Trenches", "Earthquakes", 
        "Rivers and Lakes", "Mountains", "The Seven Continents", "Maps and Globes", "Tides"
    ],
    "Polity/Government": [
        "Democracy", "What is a Constitution", "Elections", "Taxes", "The United Nations (UN)", 
        "Laws and Rules", "The Police", "Citizenship", "The President/Prime Minister", "The Flag"
    ],
    "Computers": [
        "How CPUs work", "The Internet", "Coding/Programming", "Operating Systems", 
        "Cyber Security", "Viruses and Malware", "The Cloud", "Data Storage (Memory)", 
        "Computer Games", "Apps"
    ],
    "Animals": [
        "Whales", "Insects", "Dinosaurs", "Mammals", "Endangered Species", 
        "Birds (Feathers and Flight)", "Reptiles", "Pet Care", "Camouflage", 
        "Animal Communication"
    ],
    "Everyday Concepts": [
        "Money", "Time", "Electricity", "Magnets", "Reflections (Mirrors)", 
        "How Cars Move", "Why We Need Sleep", "Traffic Lights", "Recycling", "Batteries"
    ],
    "Emotions": [
        "Happiness", "Sadness", "Fear", "Anger", "Empathy", "Dreams", 
        "Memory", "Shyness", "Being Brave", "Kindness"
    ],
    "Space & Astronomy": [
        "The Sun", "The Moon", "Stars", "Galaxies", "Astronauts", "Comets and Meteors", 
        "Mars", "Jupiter (Giant Planet)", "Seasons", "Telescopes"
    ],
    "Art & Culture": [
        "Music and Instruments", "Painting", "Sculptures", "Poetry", "Different Languages", 
        "Theatre", "Festivals", "Sports Rules", "Why People Wear Different Clothes", "Storytelling"
    ],
    "Health & Body": [
        "Bones and Muscles", "Eating Healthy Food", "Breathing", "Why We Get Sick", 
        "Doctors and Hospitals", "Brushing Teeth", "The Brain", "Exercise", "Allergies", "Blood"
    ]
}

# --- 2. CUSTOM CSS (FIXED HEIGHT AND AQUAMARINE SELECTBOXES) ---
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
    
    /* FIX 1: Increase the overall height allocated to the widget container */
    .stTextInput > div {
        min-height: 85px; 
    }

    /* FIX 2: Style and size the actual input element */
    .stTextInput > div > div > input {
        background-color: #40E0D0 !important; /* Turquoise */
        color: #000000 !important;             /* Black Text */
        font-weight: bold;
        border: 2px solid #000000;
        border-radius: 12px;
        box-shadow: 4px 4px 0px rgba(0,0,0,0.2); 
        height: 70px; /* Taller input box */
        font-size: 24px; /* Larger font size to fill the space */
        padding: 15px; /* Add vertical padding */
    }
    
    /* 5. Selectbox Styles (AQUAMARINE) */
    .stSelectbox > label,
    .stSelectbox > div > button,
    .stSelectbox > div[data-baseweb="select"] > div {
        background-color: #7FFFD4 !important; /* Aquamarine */
        border: 1px solid #000000;
        border-radius: 8px;
        font-weight: bold;
        color: #000000 !important; /* Ensure black text */
    }
    
    /* 6. Tabs styling */
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
try:
    GOOGLE_API_KEY = st.secrets["google_api_key"]
except KeyError:
    st.error("⚠️ API Key not found in Streamlit Secrets. Please set 'google_api_key'.")
    st.stop() 

try:
    genai.configure(api_key=GOOGLE_API_KEY)
    # Using the stable and efficient 'gemini-2.5-flash'
    model = genai.GenerativeModel('gemini-2.5-flash')
except Exception as e:
    st.error(f"⚠️ API Key configuration failed: {e}")
    st.stop()


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


# --- 4.5. APP INTRODUCTION (Revised and Fixed Section) ---
st.markdown("""
    <div style="background-color: #1877F2; padding: 20px; border-radius: 15px; border: 3px dashed #FF4500; margin-bottom: 40px;">
        
        <h2 style="text-align: center; color: #FFFFFF; text-shadow: none; margin-top: 0;">
            Welcome to ELI5 - EXPLAIN LIKE I AM 5! 🧠
        </h2>
        
        <h3 style="text-align: center; color: #FFFFFF; text-shadow: none; margin-bottom: 20px; margin-top: -10px;">
            (FOR KIDS LEARNING & DEVELOPMENT)
        </h3>
        
        <p style="text-align: center; color: #FFFFFF; font-size: 1.1rem; font-weight: 700;">
            Have you ever wondered how something works, but all the answers felt like they were written in a secret adult code? 🤯 We are here to help!
        </p>
        <p style="text-align: center; color: #FFFFFF; font-size: 1.1rem; font-weight: 700;">
            We use the power of AI to break down the biggest ideas—from **Black Holes** to **Bitcoin**—into stories so easy, even a 5-year-old can understand!
        </p>
        <p style="text-align: center; color: #FFFFFF; font-size: 1.1rem; font-weight: 700;">
            Start by telling us if you want to **Search** or **Choose** your topic below. Let's learn! 👇
        </p>
    </div>
    """, unsafe_allow_html=True)


# --- 5. SEARCH INPUT & CATEGORY LOGIC (New Branching System) ---

# Initialize variables to avoid NameError if user doesn't interact
query = None
category = "General Knowledge"

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    # Initial choice: Search OR Choose
    mode = st.radio(
        "How do you want to find your topic?", 
        ["Search Any Topic", "Choose Specific Category"], 
        horizontal=True, 
        index=0
    )

    st.write("---")
    
    if mode == "Search Any Topic":
        # PATH 1: Direct Search Bar
        query = st.text_input("Enter your topic:", placeholder="e.g. Gravity, Moon, Money...", label_visibility="collapsed")
        category = "General Knowledge" # Use default category for the prompt
        
    elif mode == "Choose Specific Category":
        # PATH 2: Guided Selection
        
        # Step 1: Main Category
        main_category = st.selectbox(
            "1. Select a Main Area:",
            options=list(SUB_CATEGORIES.keys()),
            key="main_cat_select"
        )
        
        # Step 2: Sub-Category based on Main Category
        if main_category in SUB_CATEGORIES:
            sub_options = SUB_CATEGORIES[main_category]
            sub_category = st.selectbox(
                f"2. Choose a Sub-Topic under {main_category}:",
                options=sub_options,
                key="sub_cat_select"
            )
            
            # Set the final query and category context for the AI
            query = sub_category
            category = main_category
            
            # Visual check for the user
            st.info(f"You selected: **{query}** (in the {category} category)")


# --- 6. LOGIC (CRASH PROOF) ---
if query:
    st.write("---") 
    
    with st.spinner('⚡ Brainstorming...'):
        
        # 1. GENERATE TEXT (With Safety Net)
        text_response = ""
        try:
            # Modified prompt to include the category for better context
            prompt = f"Explain '{query}' as it relates to {category} to a 5-year-old. Use a fun, engaging tone. Keep the explanation concise, around 500 words, using simple analogies."
            response = model.generate_content(prompt)
            text_response = response.text
        except Exception as e:
            # Fallback text simplified to remove technical error details for the user
            error_message = str(e)
            
            if 'Quota exceeded' in error_message:
                detail = "We've hit our usage limit for a few moments (Free Tier restriction). Try again in 30 minutes."
            else:
                detail = "The AI brain is temporarily busy or resting. Check your API key security if this persists."
                
            text_response = f"""
            ### 🚦 High Traffic Alert: Limit Reached!
            
            **Reason:** {detail}
            
            Don't worry! Your **Images** and **Videos** below are still working perfectly. 👇
            
            *(Please wait 60 seconds and search again to get the text back!)*
            """

        # 2. GENERATE IMAGE (Pollinations API)
        clean_query = query.replace(" ", "-")
        image_url = f"https://image.pollinations.ai/prompt/3d-render-of-{clean_query}-bright-colors-pixar-style-white-background-4k"
        
        # 3. SEARCH VIDEO (Youtube Search Library)
        results = None
        try:
            results = YoutubeSearch(query + " for kids", max_results=1).to_dict()
        except Exception:
            pass 

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
                    st.video(f"https://www.youtube.com/watch?v={video_id}")
                else:
                    st.write("No suitable video found.")
