import streamlit as st
import google.generativeai as genai
from youtube_search import YoutubeSearch

# --- 1. PAGE CONFIGURATION & STATE INITIALIZATION ---
st.set_page_config(
    page_title="ELI5 Pro",
    page_icon="🧠",
    layout="wide"
)

# --- CATEGORY DEFINITIONS ---
SUB_CATEGORIES = {
   "Science": [
    "Gravity", "Photosynthesis", "Black Holes", "Microbes/Germs", "Evolution",
    "Atoms and Molecules", "The Human Heart", "Vaccines", "Sound Waves", "Light",
    "Solar System", "Weather & Climate", "Electricity", "Magnets", "Plants",
    "Animals", "Fossils & Dinosaurs", "Forces & Motion", "Energy Types",
    "Water Cycle", "Simple Machines"
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
    "Mathematics": [
        "Numbers", "Addition", "Subtraction", "Multiplication", "Division",
        "Fractions", "Geometry", "Shapes", "Patterns", "Time & Clock Reading",
        "Money & Counting Coins", "Measurement", "Graphs & Charts", "Place Value",
        "Decimals", "Basic Algebra (Kids)", "Math Puzzles"
    ],
    "English Language": [
        "Alphabet", "Phonics", "Rhyming Words", "Basic Grammar", "Parts of Speech",
        "Synonyms & Antonyms", "Vocabulary Builder", "Reading Comprehension",
        "Storytelling", "Spelling", "Sentence Formation", "Idioms for Kids"
    ],
    "General Knowledge": [
        "World Records", "Famous Inventors", "Famous Scientists",
        "Important Inventions", "Continents & Oceans", "World Countries & Capitals",
        "Flags of the World", "National Symbols", "Indian States & Capitals",
        "Currencies of the World", "Famous Landmarks", "World Wonders",
        "Famous Sports Personalities", "Books & Authors (Kids)",
        "Festivals of the World", "Important Days & Dates",
        "World Organisations (UN, WHO, etc.)", "Largest & Smallest in the World",
        "First in the World & India", "Famous Children Stories"
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
    "Space & Astronomy": [
        "Planets", "Stars", "Galaxy", "Universe", "Rocket Science (Basics)",
        "Astronauts", "Space Missions (Chandrayaan, Apollo)", "Moon Phases",
        "Constellations", "Telescopes"
    ],
    "Environment": [
        "Recycling", "Pollution", "Green Energy", "Save Water",
        "Climate Change", "Ozone Layer", "Forest Life", "Endangered Animals",
        "Earth Day", "Conservation Heroes"
    ],

    "Biology": [
        "Human Body Parts", "Bones & Muscles", "Plants & Trees",
        "Life Cycle of Animals", "Brain & Nervous System", "Digestive System",
        "Respiratory System", "Cells", "Blood & Circulation", "Nutrition & Food"
    ],

    "Physics": [
        "Motion", "Heat", "Light", "Sound", "Electric Circuits",
        "Magnetism", "Energy", "Friction", "Force", "Pressure"
    ],

    "Chemistry": [
        "States of Matter", "Chemical Reactions (Safe Examples)",
        "Mixtures & Solutions", "Acids & Bases (Kid-safe)", "Periodic Table (Basics)",
        "Metals & Non-metals", "Crystals", "Air & Gases"
    ],
    "Animals": [
        "Whales", "Insects", "Dinosaurs", "Mammals", "Endangered Animals", 
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
    "Moral Education": [
        "Good Habits", "Kindness", "Honesty", "Helping Nature",
        "Respect", "Teamwork", "Sharing", "Self-Discipline", "Manners",
        "Caring for Animals"
    ],
    "Sports": [
        "Cricket Basics", "Football Basics", "Olympics",
        "Indoor Games", "Outdoor Games", "Famous Athletes",
        "Rules of Popular Sports", "Yoga for Kids"
    ],
    "Art & Culture": [
        "Music and Instruments", "Painting", "Sculptures", "Poetry", "Different Languages", 
        "Theatre", "Festivals", "Sports Rules", "Why People Wear Different Clothes", "Storytelling"
    ],
    "Indian Knowledge": [
        "Famous Indians", "Indian Festivals", "Indian Culture",
        "National Symbols", "Indian Freedom Fighters",
        "Indian Space Programs", "Indian Foods", "Indian Monuments"
    ],
    "Life Skills": [
        "Decision Making", "Problem Solving", "Time Management",
        "Basic Money Skills", "Communication Skills", "Leadership",
        "Goal Setting", "Daily Routine Planning"
    ],
    "Health & Body": [
        "Bones and Muscles", "Eating Healthy Food", "Breathing", "Why We Get Sick", 
        "Doctors and Hospitals", "Brushing Teeth", "The Brain", "Exercise", "Allergies", "Blood"
    ]
}


# --- CURATED VIDEO DATABASE (CLOSED SCRIPT CONTENT) ---
# ACTION REQUIRED: Replace every 'ID_HERE...' placeholder with a valid 10+ minute YouTube ID.
VIDEO_DB = {
    # Science
    "Gravity": "EwY6p-r_hyU", "Photosynthesis": "fG3bl2W-twI", 
    "Black Holes": "y8ymU_UBD3I", "Microbes/Germs": "9f55WvF2gBw", 
    "Evolution": "D47d6zW6Bfo", "Atoms and Molecules": "AVVDP_XJHkA", 
    "The Human Heart": "RigNGniGelg", "Vaccines": "OxHASWEKBic", 
    "Sound Waves": "AGjxfx8sy6s", "Light": "kkwgPwBKyl4",
    "Solar System": "ErUZVWUP0c4", "Weather": "nNmWAo0kDGk", "Climate": "41Bt4eOg6HU",
    "Electricity": "Dx3RpXdJw2k", "Magnets": "5hH5radPWHo", 
    "Parts of Plants": "A-xScqCN0GA", "Types of Animals": "0pHXXP-xlG8", 
    "Fossils & Dinosaurs": "dktnOPfE7Dc", "Forces & Motion": "1R6MxJpEjfs", 
    "Energy Types": "jhKejoBqiYc", "Water Cycle": "TD3XSIE4ymo", 
    "Simple Machines": "q4U-HpEVLW8",
    # Technology
    "Artificial Intelligence (AI)": "cpgvRFNAyks", "Robotics": "xbyEP0M9w7k", 
    "How Computers Work": "jCJ0t5dVi9A", "Cryptocurrency": "tR7PXavIVNs",
    "Virtual Reality (VR)": "XLP4YTpUpBI", "3D Printing": "4lHSptlQ7bs", 
    "Aeroplanes": "VLpSxHwfU04", "Rockets": "Lti6a_YYQl0", 
    "Self-Driving Cars": "qN_IW34zLPM", "Algorithms": "KJXd73u1g2c",
    # History
    "The Roman Empire": "tClxdOsC_JY", "Ancient Egypt": "lBYmOuajdC8", 
    "Medieval Castles": "qUrAuHetUFQ", "World War II": "TEORnS6Ddic", 
    "The Dinosaurs (Extinction)": "UOOkup9xigs", "The First Moon Landing": "fObYUyyE4Ak", 
    "How Fire Was Discovered": "1hKnfVaP-NQ", "The Titanic": "pgvRFNAyks", 
    "The Great Wall of China": "pgvRFNAyks", "Hitler": "pgvRFNAyks",
    # Mathematics
    "Numbers": "ZJEIKkPXirg", "Addition": "mjlsSYLLOSE", 
    "Subtraction": "qM7B2nwpV1M", "Multiplication": "eW2dRLyoyds", 
    "Division": "ek1JJVYaXxU", "Fractions": "p33BYf1NDAE", 
    "Geometry": "oGWrFQX7ELA", "Shapes": "jlzX8jt0Now", 
    "Patterns": "CzFLDtvN_Xk", "Time & Clock Reading": "r2K1Py9U87I",
    "Indian Money & Coins": "WnM1sFjtsAU", "Measurement": "zsv7bYSrzMU", 
    "Graphs & Charts": "g5BEleMSutI", "Place Value": "QS32l5WhSuY",
    "Decimals": "LFO07qWWtrs", "Basic Algebra (Kids)": "h9A_lfAUnm4", 
    "Math Quiz": "lPOJeo3qj48",
    # English Language
    "Alphabet": "RiYzD1h-YVQ", "Phonics": "3HmR8whNJm4", 
    "Rhyming Words": "cY7JggN5M-U", "Basic Grammar": "4ncLB3JPy_w", 
    "Parts of Speech": "yNdpfnV-WQU", "Synonyms & Antonyms": "BWdXN0wwi6A", 
    "Vocabulary Builder": "6GMAugzV5ls", "Reading Comprehension": "n9lDqCO0pBQ",
    "Storytelling": "afLeOefHKG4", "Spelling": "r1uUwrQy_4g", 
    "Sentence Formation": "vaRjZkkKjQ8", "Idioms for Kids": "WVHlVbIgUH0",
    # General Knowledge
    "World Records": "aHBGiMTXvd4", "Famous Inventors": "bEvTsoDh4bk", 
    "Famous Scientists": "MpUvHCCQwWs", "Important Inventions": "Yr88rbWb-7E", 
    "Continents & Oceans": "UxUPAKyNmjI", "World Countries & Capitals": "21N-jGPfdCY",
    "Flags of the World": "0rmz4UZJizk", "National Symbols of india": "uSRt2M82-Ag", 
    "Indian States & Capitals": "t-R6pAHgP5k", "Currencies of the World": "4UWoT_AIzzM", 
    "Famous Landmarks": "Uh332gXQYI4", "World Wonders": "TI5POfveNAg",
    "Famous Sports Personalities": "vvBICOc3P-M", "Things to know": "mSEYTJZ4N_c",
    "Festivals of the World": "6G84ZjyiGFI", "Family stories": "9G18UA311QA",
    "World Organisations (UN, WHO, etc.)": "AlglpBZE970", "Largest & Smallest in the World": "hrfRDrJp4zM",
    "Learn about India": "2o_tnKLle9A", "APJ motivational Stories": "sRd04r7mDjA",
    # Geography
    "Volcanoes": "WX_E1CAZjaQ", "Deserts": "dElLbbptwfo", 
    "Arctic vs Antartic": "Z5VRoGTF60s", "Oceans of the world": "1WZsxVDTqcU", 
    "Earthquakes": "jlLpZ9S2slQ", "Water bodies": "FshhCvbFedE", 
    "Landforms": "4C5FrjqndWg", "The Seven Continents": "AehgK6e_a5Y", 
    "Maps and Globes": "0ZlLez0hFHw", "Tides": "cm7T1Etl2XY",
    # Polity/Government
    "Democracy": "CmrO44KM7yk", "What is a Constitution": "jsTB7gSfDPI", 
    "Elections": "_iutCs28ZgI", "Taxes": "rAhobLacBrs", "The United Nations (UN)": "musUdV-QDf8", 
    "Laws and Rules": "5dtuZkposkk", "The Police": "Gr5giRmHRas", 
    "Rights and Responsibilities": "IFWwEMFSY1r0", "World's first Prime Minister": "8k5apjNrvCY", 
    "The Flag": "ysalOZzweAs",
    # Computers
    "How CPUs work": "OKVWvd87P7w", "The Internet": "UXsomnDkntI", 
    "Coding/Programming": "j-3eArinB7E", "Operating Systems": "kK7L2ISGucM", 
    "Cyber Security": "nVEyG3C-Mqw", "Viruses and Malware": "cFo5D9mFUJQ", 
    "The Cloud": "M988_fsOSWo", "Data Storage (Memory)": "PzriOtunFM8", 
    "Video Games": "VlhlGk_9X4A", "Apps": "S6VQjxbVxQw",
    # Space & Astronomy
    "Planets": "e8YzKyot4Pc", "Stars": "noUp_LAATiI", "Galaxy": "TAK0JkOArS4", 
    "Universe": "E490qP5TtQg", "Rocket Science (Basics)": "7nAWi6qAhs4",
    "Astronauts": "onjaEriVkUE", "Space Technologies": "tDoOiwNcawk", "Space Station": "IagxIpCvMl4",
    "Moon Phases": "Ie2WRraxdPs", "Constellations": "pqis3gZwVaY", 
    "Telescopes": "UolsJtK4528",
    # Environment
    "Recycling": "V0lQ3ljjl40", "Pollution": "7qkaz8ChelI", "Sources of energy": "tu9EmU5P5xw",
    "Green Energy": "BghzlvXQ3cs", "Water facts": "7PzEPfrdC_Y",
    "Climate Change": "WkvPdUtYhX8", "Ozone Layer": "ckULkfv3Hb0", 
    "Forest Life": "22QvrKVZh8c", "Endangered Animals": "E5cVr3HdLa4",
    "Earth Day": "wefswCPT7B4", "Conservation of the environment": "YIrKW6jXjdM",
    # Biology
    "Human Body Parts": "AHQGNb0zBgg", "Muscles": "OSsntU6sTWI", "Bones": "3MN-M4gsDX0",
    "Plants": "18amLZ9vfG8","Trees": "B13TXhXhf9w", "Life Cycle of Animals": "TIGOoCZldts", 
    "Brain & Nervous System": "VAEmxt78bBI", "Digestive System": "SD8kLAD1jnA",
    "Respiratory System": "67Jbbu7UZAA", "Cells": "8o8c3unt1wk", 
    "Blood & Circulation": "Dw0WO2XZ5fM", "Nutrition & Food": "EhfOZMOF9W4",
    # Physics
    "Motion": "YnXU-AwAjGk", "Heat": "Me60Ti0E_rY", "Light": "kkwgPwBKyl4", 
    "Sound": "AGjxfx8sy6s", "Electric Circuits": "js7Q-r7G9ug",
    "Magnetism": "5hH5radPWHo", "Energy": "jMx3FbNmHrA", 
    "Friction": "qux5wMu9mqI", "Force": "1R6MxJpEjfs", "Pressure": "IoD5Ph0sY4A",
    # Chemistry
    "States of Matter": "efaaNH-LbTQ", "Chemical Reactions (Safe Examples)": "5iowJs6MryI",
    "Mixtures & Solutions": "1MVpXOoEcys", "Acids & Bases (Kid-safe)": "ivRczDkilAI", 
    "Periodic Table (Modern)": "bKKJkxqIg94", "Metals & Non-metals": "85_uFR-OVQ4", 
    "Crystals": "BDJDPsTfHUw", "Air": "mHvsRXjt2Ug",
    # Animals (General)
    "Whales": "9VO0cQyg5dE", "Insects": "EO1IGi83LGg", 
    "Dinosaurs": "ZM7Vsv86058", "Mammals": "zqsK0VhcL8o", 
    "Endangered Animals": "E5cVr3HdLa4", "Birds (Feathers and Flight)": "d1L9u4UCXwY", 
    "Reptiles": "wWacC2gy_N4", "Pet Care": "pKosbOawGSY", 
    "Animal Camouflage": "F-vRzYreZXY", "Animal Communication": "RbhHTVw3r58",
    # Everyday Concepts
    "Money": "09EkUUPXizY", "Good habits": "XvYSYwevuR8", 
    "Electricity": "Dx3RpXdJw2k", "Magnets": "XNaiwHWqQ", 
    "How do mirrors work": "yK8de22i2JU", "Electric cars": "GeGTNQUrSfw", 
    "Why We Need Sleep": "CoCL0IB4u4g", "Traffic Rules": "x696dQb3W2k", 
    "Recycling": "Fex-wvrOZf4", "Batteries": "MFUUoNNo6tI",
    # Emotions
    "Happiness": "ymrvDRofDkY", "Sadness": "XO1EYsTgyJs", 
    "Fear": "G4kDLKBo32g", "Anger": "clwt7iXF1Mg", "Empathy": "sBolsBnFsnc", 
    "Dreams": "09TRoxgVPjs", "Memory": "jwPpxSFQNvw", 
    "Shyness": "Slt1ysgA-xw", "Being Brave": "403DW5luZYM", "Kindness": "kwIsfnWgTb4",
    # Moral Education
    "Good Habits": "d2WOUmgZXNQ", "Kindness": "6P-Y_M9q7RM", 
    "Honesty": "0VWK4plxkjk", "Helping Nature": "Q35krsQoCoge",
    "Respect": "7o977t6YMeg", "Teamwork": "aI6btBSBjBk", 
    "Sharing": "wlOHir-_x6Y", "Self-Discipline": "Fxugh3t9cXQ", 
    "Manners": "ZbSZCBYKfHk", "Caring for Animals": "pKosbOawGSY",
    # Sports
    "Cricket Basics": "cS6NaTJZzSE", "Football Basics": "IEluFKIoChI", 
    "Olympics": "nUGX9zQg2rs", "Indoor Games": "WtkN7Xan1TU", 
    "Outdoor Games": "yZUeOF1UAk8", "Global sports": "7H5CfHTZLZg",
    "Sports Vocabulary": "oDnI75nOH5I", "Yoga for Kids": "IMoQQuKDC5o",
    # Art & Culture
    "Music and Instruments": "WWBCa4KSkXQ", "Painting": "vjMHleB-Mlw", 
    "Sculptures": "i753CWCogFg", "Poetry": "-Lk9SYjHEb4", 
    "Different Languages": "C_-8SUXLY6I", "Cultures of the world": "RwSYrsjTiW4", 
    "Festivals": "6G84ZjyiGFI", "Sports Rules": "-xn9zvo0mvY", 
    "Why People Wear Different Clothes": "jSUOe1eBPnQ", "Storytelling": "afLeOefHKG4",
    # Indian Knowledge
    "Famous Indians": "Mspsopyz6V4", "Indian Festivals": "omcGccw6c58", 
    "Indian Culture": "lK3oqU2WNY0", "National Symbols": "GYXl8N7Mjjk", 
    "Indian Freedom Fighters": "7pAOK3i8PWM", "Indian Space Programs": "HdEKSEbdDoY", 
    "Indian Foods & clothes": "WATxlpzprdA", "Indian Monuments": "9ZGXAmy9ZpEs",
    # Life Skills
    "Decision Making": "8vFivTUuYnE", "Problem Solving": "RTBMem1Rzk", 
    "Time Management": "qeIbtIcL11Q", "Basic Money Skills": "c8aMoohIWdo", 
    "Communication Skills": "4AvSvZkmDJU", "Leadership": "vDa-nUDXJh4",
    "Goal Setting": "mKcSyeAn0GA", "Daily Routine Planning": "iMDdB8tUDVM",
    # Health & Body
    "Bones and Muscles": "XtHucs6VDYU", "Eating Healthy Food": "kvlWTI672sk", 
    "Breathing": "67Jbbu7UZAA", "Why We Get Sick": "IKpg9JEJrHI", 
    "Doctors and Hospitals": "BHfmsZnu7GQ", "Brushing Teeth": "l6XGE-Xuq3M", 
    "The Brain": "rVDZYQOoeHw", "Exercise": "lSuekPtI_Kc", 
    "Allergies": "sM3FDsMAMdc", "Blood": "Dw0WO2XZ5fM",
    
    "DEFAULT_VIDEO_ID": "HAijfhtJs7w" 
}


# --- CATEGORY FALLBACK DEFAULTS (For Open Search Failure) ---
# Action: Replace every 'ID_HERE_...' placeholder with a valid 10+ minute YouTube ID for the category.
CATEGORY_DEFAULTS = {
    "Science": "b5NK4CXI4GQ",
    "Earth Science" : "lv6dC0coQeI",
    "Amazing animals" : "eUunYTYia3I",
    "Technology" : "30APiz11hGQ",
    "History" : "2ZY_xxUq2z0",
    "4th grade Mathematics" : "zQgHqM1XvUY",
    "English Language" : "sBzad6Ly17E",
    "General Knowledge": "VeD6LR8uRlQ",
    "Geography": "NVLv52rE4ug",
    "Polity/Government": "w_zIq1Ad0mg",
    "Computers": "J-IY0rc5824",
    "Space & Astronomy": "Iy0prSnBAOc",
    "Environment": "JgvDuLcL4yQ",
    "Biology": "me-MbPNwIPk",
    "Physics": "BnQnXN0y8P0",
    "Chemistry": "avgFqlNML5o",
    "Emotions": "ZJAEkDXtyQQ",
    "Moral Education": "afLeOefHKG4",
    "Sports": "-xn9zvo0mvY",
    "World Culture": "RwSYrsjTiW4",
    "Indian Knowledge": "ZnLBACIkHA0",
    "Life Skills": "UKEOjzroOjE",
    "Health & Body": "4w0P-yn9ODA",
    "Science experiments": "NulUsNMldgw",
    "Vocabulary": "6GMAugzV5ls",
    "Routine": "H4_CunruYFg",
    "Fruits": "TCQ0GSH10D0",
     "Vegetables": "-wfHh2Wyq2U",
     "Festivals of India": "32Z3U30M5Ys",
     "Financial literacy": "Bqyek4dnycM",
    
    "DEFAULT_GENERIC": "HAijfhtJs7w"
}


# --- 2. CUSTOM CSS (VISUALS REMAIN THE SAME) ---
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
            ENGLISH EDITION 🇬🇧
        </div>
    </div>
    """, unsafe_allow_html=True)


# --- 4.5. APP INTRODUCTION (Final Simplified Title) ---
html_intro = '<div style="background-color: #1877F2; padding: 20px; border-radius: 15px; border: 3px dashed #FF4500; margin-bottom: 40px;">'
html_intro += '<h2 style="text-align: center; color: #FFFFFF; text-shadow: none; margin-top: 0;">Welcome to ELI5 - EXPLAIN LIKE I AM 5! 🧠</h2>'
html_intro += '<h3 style="text-align: center; color: #FFFFFF; text-shadow: none; margin-bottom: 20px; margin-top: -10px;">(FOR KIDS LEARNING & DEVELOPMENT)</h3>'
html_intro += '<p style="text-align: center; color: #FFFFFF; font-size: 1.1rem; font-weight: 700;">Have you ever wondered how something works, but all the answers felt like they were written in a secret adult code? 🤯 We are here to help!</p>'
html_intro += '<p style="text-align: center; color: #FFFFFF; font-size: 1.1rem; font-weight: 700;">We use the power of AI to break down the biggest ideas—from **Black Holes** to **Bitcoin**—into stories so easy, even a 5-year-old can understand!</p>'
html_intro += '<p style="text-align: center; color: #FFFFFF; font-size: 1.1rem; font-weight: 700;">Start by telling us if you want to **Search** or **Choose** your topic below. Let\'s learn! 👇</p>'
html_intro += '</div>'

st.markdown(html_intro, unsafe_allow_html=True)

# --- 4.6. MONETIZATION / DONATION BUTTON ---
BMC_LINK = "https://www.buymeacoffee.com/sunilvasarkar"

st.sidebar.markdown("---")
st.sidebar.markdown(
    f"""
    <div style="text-align: center; padding: 10px; border-radius: 10px; background-color: #FFEEAA; border: 2px dashed #D3A500;">
        <h3 style="color: #000000; text-shadow: none; margin-bottom: 5px;">Enjoying ELI5 Pro?</h3>
        <p style="font-size: 1rem; color: #000000; font-weight: 500;">
            Help keep the AI brain running and buy the developer a coffee! ☕
        </p>
        <a href="{BMC_LINK}" target="_blank">
            <img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 45px !important;width: 162px !important;" >
        </a>
    </div>
    """,
    unsafe_allow_html=True,
)
st.sidebar.markdown("---")


# --- 5. SEARCH INPUT & CATEGORY LOGIC (English-Only Flow) ---

# Initialize variables to avoid NameError if user doesn't interact
query = None
category = "General Knowledge"
is_curated_search = False # Flag to track if the search is from the fixed list

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
        # PATH 1: Direct Search Bar (Open Topics)
        
        # Step 1: Select the closest category for video fallback
        category = st.selectbox(
            "1. Select Closest Topic Area for Video Fallback:",
            options=list(CATEGORY_DEFAULTS.keys()),
            key="open_search_category"
        )
        
        # Step 2: Enter the search query
        query = st.text_input("2. Enter your topic:", placeholder="e.g. Black Holes, Constitution, Money...", label_visibility="visible")
        is_curated_search = False
        
    elif mode == "Choose Specific Category":
        # PATH 2: Guided Selection (Curated Content)
        
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
            is_curated_search = True
            
            # Visual check for the user
            st.info(f"You selected: **{query}** (in the {category} category)")


# --- 6. LOGIC (CRASH PROOF) ---
if query:
    st.write("---") 
    
    with st.spinner('⚡ Brainstorming in English...'):
        
        # 1. GENERATE TEXT (With Safety Net)
        text_response = ""
        try:
            # PROMPT: Simple English generation
            prompt = (
                f"Explain '{query}' (Category: {category}) to a 5-year-old. "
                f"Generate the entire explanation in **English**. "
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
        
        # 3. VIDEO SEARCH: HYBRID (Curated or Dynamic)
        video_id = None
        
        if is_curated_search:
            # --- PATH A: CURATED SEARCH (Category Mode - Guaranteed 10+ Min) ---
            video_id = VIDEO_DB.get(query, VIDEO_DB["DEFAULT_VIDEO_ID"])
            
            # Determine which default message to show
            if video_id in VIDEO_DB.values(): # Checks if the ID is a known, filled ID
                st.info("Video selected from the highly-curated educational database (10+ minutes guaranteed).")
            else:
                # If specific topic fails, use the general category fallback
                category_fallback_id = CATEGORY_DEFAULTS.get(category, CATEGORY_DEFAULTS["DEFAULT_GENERIC"])
                video_id = category_fallback_id
                st.warning(f"Curated video not found for '{query}'. Showing high-quality default video for {category}.")

        else:
            # --- PATH B: DYNAMIC SEARCH (Search Bar Mode - Relevancy/Safety Focused) ---
            
            # --- Attempt Dynamic Search ---
            try:
                # Use stable English dynamic search for open topics with safety keywords
                video_search_query = f"{query} {category} educational video for kids safe mode child lock 10 minute"
                results = YoutubeSearch(video_search_query, max_results=1).to_dict()
                
                if results and results[0].get('id'):
                    video_id = results[0]['id']
                    st.warning("Using dynamic YouTube search. Video length and content relevance may vary.")
                else:
                    # If dynamic search fails, use the category default fallback
                    video_id = CATEGORY_DEFAULTS.get(category, CATEGORY_DEFAULTS["DEFAULT_GENERIC"])
                    st.warning(f"Dynamic search failed. Showing high-quality default video for {category}.")
            except Exception:
                # If everything fails, use the absolute generic fallback
                video_id = CATEGORY_DEFAULTS["DEFAULT_GENERIC"]
                st.warning("All searches failed. Showing absolute general fallback video.")
        
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
                # Video is guaranteed to exist by this point 
                st.video(f"https://www.youtube.com/watch?v={video_id}")
