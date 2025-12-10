import streamlit as st
import google.generativeai as genai
from youtube_search import YoutubeSearch

# --- 1. PAGE CONFIGURATION & STATE INITIALIZATION ---
st.set_page_config(
    page_title="ELI5 Pro",
    page_icon="🧠",
    layout="wide"
)

# Initialize session state for query translation cache
if 'translation_cache' not in st.session_state:
    st.session_state['translation_cache'] = {}


# --- LANGUAGE DEFINITIONS ---
LANGUAGES = {
    "English": {"name": "English", "code": "en", "suffix": "for children"},
    "Hindi (हिंदी)": {"name": "Hindi", "code": "hi", "suffix": "बच्चों के लिए"},
    "Gujarati (ગુજરાતી)": {"name": "Gujarati", "code": "gu", "suffix": "બાળકો માટે"},
    "Spanish (Español)": {"name": "Spanish", "code": "es", "suffix": "para niños"},
    "French (Français)": {"name": "French", "code": "fr", "suffix": "pour enfants"},
    "Mandarin (普通话)": {"name": "Mandarin Chinese", "code": "zh", "suffix": "给孩子们"},
    "German (Deutsch)": {"name": "German", "code": "de", "suffix": "für kinder"},
    "Japanese (日本語)": {"name": "Japanese", "code": "ja", "suffix": "子供向け"}
}

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
    .stTextInput > div {
        min-height: 85px; 
    }

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
    model = genai.GenerativeModel('gemini-2.5-flash')
except Exception as e:
    st.error(f"⚠️ API Key configuration failed: {e}")
    st.stop()


# --- MULTILINGUAL TRANSLATION FUNCTION (CACHED) ---
def translate_query_for_search(query, target_language_name, model):
    if target_language_name == "English":
        return query
    
    # Use session state cache key
    cache_key = f"translation_{query}_{target_language_name}"
    if cache_key in st.session_state:
        return st.session_state[cache_key]
        
    # Prompt the AI ONLY for the translated topic name
    prompt = f"Provide ONLY the single best translated topic name for '{query}' into {target_language_name}. Do not include any surrounding text, quotes, or explanations."
    try:
        response = model.generate_content(prompt)
        translated_topic = response.text.strip().replace('"', '').replace("'", '').split('\n')[0].strip()
        st.session_state[cache_key] = translated_topic
        return translated_topic
    except Exception:
        # Fallback to the original English query if translation fails
        st.session_state[cache_key] = query
        return query


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
html_intro = '<div style="background-color: #1877F2; padding: 20px; border-radius: 15px; border: 3px dashed #FF4500; margin-bottom: 40px;">'
html_intro += '<h2 style="text-align: center; color: #FFFFFF; text-shadow: none; margin-top: 0;">Welcome to ELI5 - EXPLAIN LIKE I AM 5! 🧠</h2>'
html_intro += '<h3 style="text-align: center; color: #FFFFFF; text-shadow: none; margin-bottom: 20px; margin-top: -10px;">(FOR KIDS LEARNING & DEVELOPMENT)</h3>'
html_intro += '<p style="text-align: center; color: #FFFFFF; font-size: 1.1rem; font-weight: 700;">Have you ever wondered how something works, but all the answers felt like they were written in a secret adult code? 🤯 We are here to help!</p>'
html_intro += '<p style="text-align: center; color: #FFFFFF; font-size: 1.1rem; font-weight: 700;">We use the power of AI to break down the biggest ideas—from **Black Holes** to **Bitcoin**—into stories so easy, even a 5-year-old can understand!</p>'
html_intro += '<p style="text-align: center; color: #FFFFFF; font-size: 1.1rem; font-weight: 700;">Start by telling us if you want to **Search** or **Choose** your topic below. Let\'s learn! 👇</p>'
html_intro += '</div>'

st.markdown(html_intro, unsafe_allow_html=True)

# --- 4.6. MONETIZATION / DONATION BUTTON ---
BMC_LINK = "https://buymeacoffee.com/sunilvasarkar"  # <<< IMPORTANT: REPLACE THIS LINK

st.sidebar.markdown("---")
st.sidebar.markdown(
    """
    <div style="text-align: center; padding: 10px; border-radius: 10px; background-color: #FFEEAA; border: 2px dashed #D3A500;">
        <h3 style="color: #000000; text-shadow: none; margin-bottom: 5px;">Enjoying ELI5 Pro?</h3>
        <p style="font-size: 1rem; color: #000000; font-weight: 500;">
            Help keep the AI brain running and buy the developer a coffee! ☕
        </p>
        <a href="https://buymeacoffee.com/sunilvasarkar" target="_blank">
            <img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 45px !important;width: 162px !important;" >
        </a>
    </div>
    """,
    unsafe_allow_html=True,
)
st.sidebar.markdown("---")


# --- 5. SEARCH INPUT & CATEGORY LOGIC (New Branching System with Language) ---

# Initialize variables to avoid NameError if user doesn't interact
query = None
category = "General Knowledge"

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    
    # LANGUAGE SELECTOR
    selected_language = st.selectbox(
        "Select Language for Explanation:",
        options=list(LANGUAGES.keys()),
        index=0,
        key="language_select"
    )
    st.write("---") 
    
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
    
    # Get the language data
    lang_data = LANGUAGES[selected_language]
    language_keyword = lang_data["name"]
    
    with st.spinner(f'⚡ Brainstorming in {language_keyword}...'):
        
        # 1. GENERATE TEXT (With Safety Net)
        # Use the original English query for text prompt clarity
        text_response = ""
        try:
            prompt = (
                f"Explain '{query}' (Category: {category}) to a 5-year-old. "
                f"Generate the entire explanation in **{language_keyword}**. "
                f"Use a fun, engaging tone. Keep the explanation concise, around 500 words, using simple analogies."
            )
            response = model.generate_content(prompt)
            text_response = response.text
        except Exception as e:
            # Fallback text simplified
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
        
        # 3. SEARCH VIDEO (Highly Localized using both English and Suffix)
        results = None
        try:
            language_suffix = lang_data["suffix"]

            # Strategy: Search using both the original English query AND the strong localized suffix 
            # This search is highly likely to find the Hindi/Gujarati video if it exists.
            video_search_query = f"{query} | {language_suffix}" 
            
            results = YoutubeSearch(video_search_query, max_results=1).to_dict()
        
        except Exception:
            # Fallback to general English search if the localized search fails
            try:
                results = YoutubeSearch(f"{query} educational video for kids", max_results=1).to_dict()
                st.warning(f"YouTube search failed for {language_keyword} keywords.")
            except:
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
                    st.write(f"No suitable video found related to {language_keyword}. Try a simple search topic.")
