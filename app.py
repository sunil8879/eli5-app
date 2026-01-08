# --- IMPORTS ---
from groq import Groq
import streamlit as st
from youtube_search import YoutubeSearch
from gtts import gTTS # NEW IMPORT
import os # NEW IMPORT
import io # NEW IMPORT

# --- 1. PAGE CONFIGURATION & STATE INITIALIZATION ---
st.set_page_config(
    page_title="ELI5 Pro",
    page_icon="🧠",
    layout="wide"
)

# Initialize session state variables for TTS
if 'tts_trigger' not in st.session_state:
    st.session_state['tts_trigger'] = False
if 'last_explanation' not in st.session_state:
    st.session_state['last_explanation'] = ""
if 'last_lang_code' not in st.session_state:
    st.session_state['last_lang_code'] = "English"
if 'current_audio_path' not in st.session_state:
    st.session_state['current_audio_path'] = None 



# --- LANGUAGE DEFINITIONS ---
# --- LANGUAGE DEFINITIONS (CORRECT DICTIONARY STRUCTURE) ---
LANGUAGES = {
    "English": {"name": "English"},
    "Hindi (हिंदी)": {"name": "Hindi"},
    "Gujarati (ગુજરાતી)": {"name": "Gujarati"},
    "Spanish (Español)": {"name": "Spanish"},
    "French (Français)": {"name": "French"},
    "Mandarin (普通话)": {"name": "Mandarin Chinese"},
    "German (Deutsch)": {"name": "German"},
    "Japanese (日本語)": {"name": "Japanese"}
}

# --- TEXT-TO-SPEECH IMPORTS ---
from gtts import gTTS
import os
import io

# --- TTS FUNCTION (Cached for speed) ---
# NOTE: Language code is needed for gTTS, which is slightly different than language name.
# We will create a helper dictionary for the codes.
TTS_LANG_CODES = {
    "English": "en", "Hindi": "hi", "Gujarati": "gu", "Spanish": "es", 
    "French": "fr", "Mandarin Chinese": "zh-cn", "German": "de", "Japanese": "ja"
}

# START OF NEW INSERTION:
@st.cache_resource(show_spinner=False)
def generate_audio_bytes(text, language_name):
    lang_code = TTS_LANG_CODES.get(language_name, 'en')
    
    try:
        tts = gTTS(text=text, lang=lang_code, slow=False)
        
        # Use BytesIO to save audio directly into memory
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        return fp.read() # Returns raw MP3 bytes
        
    except Exception as e:
        print(f"TTS Generation Failed for {language_name}: {e}") 
        return None
# END OF NEW INSERTION

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
        "Doctors and Hospitals", "Brushing Teeth", "The Brain", "Exercise", "Allergies", "Blood", "How do body parts work"
    ],




"Economics & Money": [
    "What is a Bank", "How ATMs Work", "Saving & Budgeting",
    "Demand & Supply (Kids)", "What Are Taxes Used For",
    "Goods vs Services", "How Businesses Work"
],

"Psychology": [
    "How the Brain Makes Decisions", "Habits & Routines", "Why We Dream",
    "Growth Mindset", "Why We Forget Things", "Understanding Motivation"
],

"Health & Safety": [
    "First Aid Basics", "Road Safety Rules", "Fire Safety",
    "Internet Safety for Kids", "Hygiene Rules", "Emergency Numbers & Help"
],

"Creativity & Arts": [
    "Drawing Techniques", "Cartooning", "Origami",
    "Clay Modelling", "Colour Theory", "Creative Writing for Kids"
],

"Food & Nutrition": [
    "What Are Vitamins", "Healthy Snacks", "How Digestion Works (Kids)",
    "Where Food Comes From", "Food Groups", "Food Safety & Cleanliness",   "Food groups", "Healthy food",
    "How Digestion Works (Kids)", "Where Food Comes From",
    "Healthy vs Unhealthy food", "Food Safety & Cleanliness", "Details of Vitamins"
],

"Transportation": [
    "How Airplanes Fly", "How Trains Work", "Bicycles & Gears",
    "Ships & Submarines", "Traffic Rules", "Future Transport (Hyperloop)"
],

"Careers & Future Jobs": [
    "What Scientists Do", "Becoming a Doctor", "Space Careers",
    "Digital Creators", "Engineers & Inventors", "Wildlife Researchers"
],

"Culture & Society": [
    "World Traditions", "Family Structures", "Manners Around the World",
    "Languages of the World", "Food Cultures", "Traditional Clothing"
],

"Logic & Critical Thinking": [
    "Puzzles & Riddles", "Logical Reasoning", "Spot the Pattern",
    "Sequencing", "Cause & Effect", "Analogies"
],

"Ethics & Values": [
    "Fairness", "Responsibility", "Respecting Privacy",
    "Environmental Responsibility", "Anti-Bullying", "Equality"
],

"Daily Life Skills": [
    "Doing Basic Household Tasks", "Packing a School Bag", "Cleaning & Tidying",
    "Shopping Basics", "How to Use Public Transport", "Understanding Labels"
],

"Weather & Natural Disasters": [
    "Floods", "Droughts", "Hurricanes & Cyclones",
    "Tsunamis", "Lightning", "Weather Forecasting"
],

"Mythology & Folk Stories": [
    "Greek Mythology", "Indian Mythology", "Norse Mythology",
    "Folk Tales Around the World", "Fairy Tales Explained", "Legends & Heroes"
],

"Family & Relationships": [
    "Roles of Family Members", "Helping at Home", "Respecting Elders",
    "Sibling Bonds", "Handling Conflicts", "Family Support"
],

"Media & Entertainment": [
    "How Movies Are Made", "Animation Basics", "Music Genres",
    "Comics & Superheroes", "Radio vs Television", "How News Works"
],

"Agriculture & Farming": [
    "How Crops Grow", "Types of Farming", "Farm Animals",
    "Organic Farming", "Irrigation", "Farm Machines"
],

"Architecture & Structures": [
    "How Bridges Work", "Skyscrapers", "Tunnels",
    "Houses Around the World", "Ancient Structures", "Building Materials"
],

"Oceans & Marine Life": [
    "Coral Reefs", "Deep Sea Creatures", "Waves & Currents",
    "Ocean Exploration", "Marine Plants", "Underwater Volcanoes"
],

"Hobbies & Recreation": [
    "Gardening", "Bird Watching", "Stamp/ Coin Collecting",
    "Camping", "Playing Instruments", "Photography Basics"
],

"Finance for Kids": [
    "What Is Salary", "Pocket Money", "Profit & Loss (Simple)",
    "Saving vs Spending", "Digital Payments", "What Is Insurance (Simple)"
],






"Economics & Money": [
    "What is a Bank", "How ATMs Work", "Financial terminologies",
    "Demand & Supply (Kids)", "What Are Taxes Used For",
    "Goods vs Services", "History of Money", "Business ideas"
],


"Psychology": [
    "How the Brain Makes Decisions", "Habits & Routines", "Why We Dream",
    "Growth Mindset", "Why We Forget Things", "Understanding Motivation"
],


"Health & Safety": [
    "First Aid Basics", "Road Safety Rules", "Fire Safety",
    "Internet Safety for Kids", "Hygiene Rules",
    "Emergency Numbers & Help"
],


"Creativity & Arts": [
    "Drawing Techniques", "Landscaping", "Origami",
    "Clay Modelling", "Colour Theory", "Creative Writing for Kids"
],





"Transportation": [
    "Inventions of aeroplanes", "How Trains Work",
    "Bicycles & Gears", "Ships & Submarines",
    "What is Hyperloop", "Future Transport"
],


"Careers & Future Jobs": [
    "Jobs and Occupations", "Different types of Doctors",
    "Space Careers", "Best jobs ever", "High paying jobs"
],


"Culture & Society": [
    "World Traditions", "Family Structures",
    "Manners Around the World", "Languages of the World",
    "World cuisines", "Traditional Clothing"
],


"Logic & Critical Thinking": [
    "Puzzles & Riddles", "Logical Reasoning", "Spot the Pattern",
    "Sequencing", "Cause & Effect", "Foundational thinking",
    "Matching, Sorting and games", "Analogy"
],


"Ethics & Values": [
    "Honesty", "Responsibility", "Respecting Privacy",
    "Environmental Responsibility", "Anti-Bullying", "Equality"
],


"Daily Life Skills": [
    "Doing Basic Household Tasks", "Packing a School Bag",
    "Cleaning & Tidying", "Shopping Basics",
    "Talk about Public Transport", "Understanding Labels"
],


"Weather & Natural Disasters": [
    "Floods", "Droughts", "Hurricanes & Cyclones",
    "Tsunamis", "Lightning", "Cyclone",
    "Natural disasters names"
],


"Mythology & Folk Stories": [
    "Greek Mythology", "Indian Mythology", "Norse Mythology",
    "Folk Tales Around the World", "Fairy Tales Explained",
    "Myths | Legends | Folk tales | Fairy tales",
    "Mahabharat", "Ramayan"
],

"Stories": [
    "Family stories", "Adventure stories", "Moral stories",
    "Bedtime stories", "Fairy tales",
    "Alice's wonderland",
    "Aladdin and magic lamp", "Haatim tai",
    "Arabian nights", "Panchtantra"
],

"Movies": [
    "Little krishna", "Bal ganesh", "Tenali rama",
    "Akbar birbal", "Vikram betal","Little singham","Motu patlu"
],

"Causes of Diseases": [
    "Diabetes", "Malaria", "Chicken Pox",
    "Allergies", "Typhoid","TB","Asthama",
     "Diarrhoea", "Dandruff", "Heartattack",
    "Kidney stones", "Appendix","Alzheimer","Hiccups",
     "Head lice", "Dyslexia","Hand,foot & mouth disease","Depression","Pimples"
],

"Harmful effects of food": [
    "Sugar", "Junk food", "Milk",
    "Fruit juice", "Coffee","Tea","Cold drinks","Processed food","Burger"
],




"Ancient Civilisation": [
  "Mayans", "Vikings", "Indus Valley", "Harappan",
  "Mohenjo Daro", "Ancient Greece", "Aztecs", "Inca",
  "Mesopotamia", "Ming Dynasty", "Ancient Persia", "Stone Age"
],

"Coding Concepts": [
  "What Is a Bug", "What Are Loops", "What Are Variables",
  "What Are Binary Codes", "What Are IF-ELSE Statements",
  "What Are Functions", "What Are Classes", "What Is OOPS",
  "Types of Hackers", "Vocabulary", "How Do Search Engines Work"
],

"Music Theory": [
  "Music Theory", "Rhythm vs Pulse", "Melody vs Harmony",
  "Pitch (High & Low)", "Tempo (Speed)", "Chords",
  "Orchestra Sections", "Treble and Bass Clef", "Scales"
],

"Ice Age Animals": [
  "Woolly Mammoth", "Saber-Toothed Tiger vs Woolly Mammoth",
  "Megalodon", "Dodo Bird", "Giant Sloth",
  "Dire Wolf", "Woolly Rhinoceros", "Terror Birds",
  "Irish Elk", "Glyptodon"
],

"Deep Space Objects": [
  "Nebula", "Supernova", "Comets, Asteroids and Meteors",
  "Dwarf Planet Pluto", "Black Dwarf Star", "Exoplanets",
  "Space Exploration", "Space Debris", "The Kuiper Belt"
],

"Engineering Marvels": [
  "Panama Canal", "Channel Tunnel", "Burj Khalifa",
  "Golden Gate Bridge", "International Space Station",
  "Hoover Dam", "Aqueducts", "Suspension Bridges",
  "Bullet Trains", "Underwater Foundation", "Chenab Bridge"
],

"Autobiographies": [
  "Bhagat Singh",
  "A. P. J. Abdul Kalam",
  "J. Robert Oppenheimer",
  "Abraham Lincoln",
  "Adolf Hitler",
  "Swami Vivekananda",
  "Kalpana Chawla",
  "Albert Einstein",
  "Martin Luther King Jr.",
  "Nikola Tesla",
  "Nelson Mandela",
  "Elon Musk",
  "Bill Gates",
  "Cristiano Ronaldo",
  "Pelé"
],

"Inventions": [
  "Paper",
  "Steam Engine",
  "Telephone",
  "Television",
  "Electric Bulb",
  "Microwave Oven",
  "Refrigerator",
  "Washing Machine",
  "Mobile Phone",
  "Airplanes",
  "Computer",
  "Electricity",
  "Email",
  "Camera",
  "Zero"
],

"The five senses": [
  "Taste",
  "Hearing",
  "Smell",
  "Touch",
  "Sight",
  "All Five Senses"
],


"Rocks & Minerals": [
  "Rocks and Minerals",
  "Types of Rocks",
  "Rock Cycle",
  "Rock Uses",
  "Soil and Types"
],

"Dog Breeds": [
  "100 Dog Breeds",
  "Golden Retriever",
  "German Shepherd",
  "Doberman",
  "Labrador",
  "Bulldog",
  "Pomeranian",
  "Siberian Husky",
  "Dalmatian",
  "Beagle",
  "Chihuahua"
],

"Secret Codes": [
  "Morse Code",
  "Invisible Ink",
  "Fingerprints",
  "Caesar Cipher"
],

"Basic Concepts": [
  "MS Word",
  "MS Excel",
  "MS PowerPoint",
  "Server",
  "Google Drive",
  "Google Docs",
  "Google Sheets",
  "Google Maps",
  "Gmail"
],

"Natural Wonders of the World": [
  "Northern Lights",
  "Grand Canyon",
  "Great Barrier Reef",
  "Mount Everest",
  "Victoria Falls",
  "Dead Sea",
  "Amazon Rainforest",
  "Paricutin Volcano",
  "Harbor of Rio",
  "The Nile River"
],




"Benefits of various vegetables": [
  "Spinach", "Lettuce", "Cabbage", "Kale", "Swiss Chard",
  "Mustard Greens", "Collard Greens", "Arugula", "Fenugreek Leaves",
  "Coriander Leaves", "Parsley", "Basil", "Mint", "Dill", "Sorrel",
  "Bok Choy", "Napa Cabbage", "Endive", "Radicchio", "Watercress",
  "Carrot", "Beetroot", "Radish", "Turnip", "Sweet Potato", "Potato",
  "Yam", "Cassava", "Parsnip", "Rutabaga", "Salsify", "Taro Root",
  "Burdock Root", "Jerusalem Artichoke", "Onion", "Garlic", "Shallot",
  "Leek", "Spring Onion", "Fennel Bulb", "Celery", "Asparagus",
  "Bamboo Shoots", "Kohlrabi", "Lotus Stem", "Rhubarb", "Cauliflower",
  "Broccoli", "Artichoke", "Banana Flower", "Broccolini", "Romanesco",
  "Tomato", "Brinjal", "Capsicum", "Chili Pepper", "Cucumber",
  "Pumpkin", "Bottle Gourd", "Ridge Gourd", "Sponge Gourd",
  "Bitter Gourd", "Snake Gourd", "Ash Gourd", "Zucchini", "Squash",
  "Okra (Ladyfinger)", "Chayote", "Tomatillo", "Jalapeño",
  "Habanero Peppers", "Green Peas", "Chickpeas", "French Beans",
  "Cluster Beans", "Broad Beans", "Soybeans", "Lentil Pods",
  "Cowpeas", "Snow Peas", "Sugar Snap Peas", "Mushroom",
  "Shiitake Mushrooms", "Oyster Mushroom", "Enoki Mushrooms",
  "Portobello Mushrooms", "Morel Mushrooms", "Drumstick",
  "Banana Stem", "Winged Beans", "Malabar Spinach",
  "Amaranth Leaves", "Elephant Foot Yam", "Water Chestnut",
  "Seaweed", "Pointed Gourd", "Daikon Radish", "Wasabi Root",
  "Lotus Root", "Perilla Leaves", "Curry Leaves", "Lemongrass",
  "Chives", "Oregano", "Thyme", "Rosemary", "Sage",
  "Fiddlehead Fern", "Celeriac", "Jicama", "Kangkong",
  "Ivy Gourd", "Teasel Gourd"
],







"Benefits of various fruits": [
    "Apple", "Banana", "Orange", "Mango", "Grapes",
    "Papaya", "Pineapple", "Watermelon", "Muskmelon", "Pear",

    "Lemon", "Lime", "Mandarin", "Tangerine", "Clementine",
    "Grapefruit", "Pomelo", "Sweet orange", "Bergamot",

    "Strawberry", "Blueberry", "Raspberry", "Blackberry",
    "Cranberry", "Gooseberry", "Mulberry", "Elderberry", "Boysenberry",

    "Coconut", "Jackfruit", "Lychee", "Longan", "Rambutan",
    "Durian", "Passion fruit", "Guava", "Star fruit", "Dragon fruit",
    "Breadfruit", "Soursop", "Custard apple", "Sugar apple",
    "Sapodilla", "Mangosteen",

    "Peach", "Plum", "Cherry", "Apricot", "Nectarine",
    "Olive", "Dates",

    "Quince", "Medlar",

    "Jamun", "Bael", "Wood apple", "Kokum", "Karonda",
    "Phalsa", "Langsat", "Salak",

    "Almond", "Cashew", "Walnut", "Pistachio", "Hazelnut",
    "Brazilnut", "Macadamia", "Pecan", "Arecanut", "Raisins",

    "Miracle fruit", "Jabuticaba",
    "Feijoa", "Horned melon", "Lucuma", "Santol",
    "Surinam cherry", "Ice apple",

    "Kiwi", "Fig", "Pomegranate", "Avocado",
    "Persimmon", "Tamarind", "Loquat"
],



"Miscellaneous": [
 "Advantages of drinking water",
     "How do plants help us",
     "Categories of animals",
     "Animals and their sounds",
     "Vertebrates & Invertebrates",
     "Types of water bodies",
     "Names of animals,birds & flowers",
     "Musical instruments",
     "Names and sounds of birds",
     "Vehicle names",
     "Carnivores,herbivores,omnivores",
     "Human body",
     "Toddler learning",
     "Finger abacus",
     "Scientific instruments"
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
    "Allergies": "sM3FDsMAMdc", "Blood": "Dw0WO2XZ5fM", "How do body parts work": "GYtJKrbqhiQ",
     #Stories
     "Family stories": "9G18UA311QA", "Adventure stories": "rHzHphVfnAo", 
    "Moral stories": "eDTCua9fgMU", "Bedtime stories": "gQAyIXGHgnc", 
    "Alice's wonderland": "IDujfwZqpgA", "Fairy tales": "_dR1grQ2hvU", 
    "Aladdin and magic lamp": "viijvOzGRLI", "Haatim tai": "6O98ckc62Jk", 
    "Arabian nights ": "sLEAfY3bAiI", "Panchtantra": "jutaxap6Ye0",
     #Movies
     "Little krishna": "3V-dmbxWcz4", "Bal ganesh": "hO1JNpwnkTs", 
    "Tenali rama": "IhDiWLALlP4", "Akbar birbal": "9I5mtAgqKM8", 
    "Vikram betal": "oQjurAE6PXI", "Little singham": "isg9KS28_qk", 
     "Motu Patlu": "mYGB7ic99lU", 
     #Causes of Diseases     
    "Diabetes": "d86DofYpkrY",
    "Malaria": "PGiqxnAr2fQ",
    "Chicken pox": "xNc4kEt4pN0",
    "Allergies": "sM3FDsMAMdc",
    "Typhoid": "dae6VhLjT70",
    "TB": "qlKwAH-8cmI",
    "Asthma": "s1R0dL1VB0I",
    "Diarrhoea": "tiz8zeGgp7U",
    "Heart attack": "jP0qT6GpBVY",
    "Kidney stones": "xmbpPWIV0VU",
    "Dandruff": "Ut9WP9jL4s4",
    "Appendix": "2IFjlIkHApo",
    "Alzheimer": "5dmqaH-MlA0",
    "Hiccups": "UZy2Wlh97SU",
    "Head lice": "Ect-ty6ka0M",
    "Dyslexia": "65psPXWzNic",
    "Hand, foot and mouth disease": "stxuE51jI3s",
    "Depression": "0hxFR6tezAc",
    "Pimples": "SPQt5v5Xsg8",






# ANCIENT CIVILISATION

"Mayans": "YW0rLAX3y-c",
"Vikings": "ul75T-6MvWA",
"Indus Valley": "S83f3hT1BiQ",
"Harappan": "XWjoBcj25SY",
"Mohenjo Daro": "VECJJIEYTXw",
"Ancient Greece": "RchSJSJAbc0",
"Aztecs": "urFpctOmJZY",
"Inca": "k__GbOiOYz4",
"Mesopotamia": "EHkAGKgoyGo",
"Ming Dynasty": "0G5EKB0omVw",
"Ancient Persia": "yN4F25Of3E4",
"Stone Age": "yN4F25Of3E4",



# CODING CONCEPTS

"What Is a Bug": "EhTr8udTdV0",
"What Are Loops": "r3Ti5Xp9W8A",
"What Are Variables": "xjZDZ1TJe4o",
"What Are Binary Codes": "XwBPeiK61Ec",
"What Are IF-ELSE Statements": "wt_oQssEF0k",
"What Are Functions": "3JIZ40yuZL0",
"What Are Classes": "IHyxevOMosw",
"What Is OOPS": "X3cFiJnxUBY",
"Types of Hackers": "9K8Xn0y5CU4",
"Vocabulary": "NNQWZf1FQyE",
"How Do Search Engines Work": "9n4l491nuOI",



# MUSIC THEORY

"Music Theory": "VxF7ebeXjfU",
"Rhythm vs Pulse": "HU_M4z7qnTc",
"Melody vs Harmony": "jILmtgbFPxo",
"Pitch (High & Low)": "jcAa9G64HdA",
"Tempo (Speed)": "3e_ciHxPswk",
"Chords": "u92UhIvxd1M",
"Orchestra Sections": "Tde91GvEHV8",
"Treble and Bass Clef": "OcRdtEGVENo",
"Scales": "w5GgDAKAzos",



# ICE AGE ANIMALS

"Woolly Mammoth": "TlX4sGPd6SA",
"Saber-Toothed Tiger vs Woolly Mammoth": "Wkbdy2RZI_w",
"Megalodon": "P4Rdb3qgvPA",
"Dodo Bird": "R-I-9SKLkoc",
"Giant Sloth": "MaTQewJIznQ",
"Dire Wolf": "eO7xZwclnlI",
"Woolly Rhinoceros": "9QtQ1CK3XAQ",
"Terror Birds": "fjVrfgoXNKA",
"Irish Elk": "motD8jAbFVU",
"Glyptodon": "nPP84w1ENa8",



# DEEP SPACE OBJECTS

"Nebula": "JmK2UNg34Z8",
"Supernova": "JnFbG1cbLB0",
"Comets, Asteroids and Meteors": "UHK-fbdbwF8",
"Dwarf Planet Pluto": "G3Oguc-jpoI",
"Black Dwarf Star": "7qnSTxxxa-I",
"Exoplanets": "dsBI-bBdnDw",
"Space Exploration": "F7JQk225fgA",
"Space Debris": "425q4Iva4zM",
"The Kuiper Belt": "2cQai-ec3J0",



# ENGINEERING MARVELS

"Panama Canal": "zRiTz3VDwvA",
"Channel Tunnel": "ZVaoEPhI_Lw",
"Burj Khalifa": "SqFx0cBR0oo",
"Golden Gate Bridge": "C8ZwEbhrco0",
"International Space Station": "oLrOnEmy_GA",
"Hoover Dam": "hopBzK6BOwo",
"Aqueducts": "Qc9FRYOuxBE",
"Suspension Bridges": "Rg9a9-IvAyE",
"Bullet Trains": "XjwF-STGtfE",
"Underwater Foundation": "8u2snChJ1x8",
"Chenab Bridge": "3hJreF5QVc0",

#AUTOBIOGRAPHIES
"Bhagat Singh": "Hq4gX59w8ms",
"A. P. J. Abdul Kalam": "sRd04r7mDjA",
"J. Robert Oppenheimer": "4b4B6qrDPdI",
"Abraham Lincoln": "za8ihVU-vx8",
"Adolf Hitler": "wDVDC81eiv4",
"Swami Vivekananda": "Dl9akckdaYk",
"Kalpana Chawla": "ixgAX31s4RM",
"Albert Einstein": "GjoYbsvUoO4",
"Martin Luther King Jr.": "iGuKmYXgm6s",
"Nikola Tesla": "58x6ID5-wqY",
"Nelson Mandela": "F0lKZqHwNXE",
"Elon Musk": "CxbMk4bREZk",
"Bill Gates": "q2fQOo9_lIw",
"Cristiano Ronaldo": "64VTm3QWshQ",
"Pelé": "mS9zDEUsO3Q",

#INVENTIONS
"Paper": "COxB_GvdzWI",
"Steam Engine": "hU22evActPU",
"Telephone": "VNbFLCZ9KEY",
"Television": "LV6r-RYVq7g",
"Electric Bulb": "XWWgDn0C6DA",
"Microwave Oven": "qCRm503O0po",
"Refrigerator": "mBFa7H1ieAQ",
"Washing Machine": "KSN6t4tc0ao",
"Mobile Phone": "75aECeykhv0",
"Airplanes": "NpqU3eSeS1c",
"Computer": "zzMm2PaVUpQ",
"Electricity": "qxWI2MGT6Co",
"Email": "EZFmZPikKjQ",
"Camera": "diNLTZNntuk",
"Zero": "tALP1YGoF3I",

#THE FIVE SENSES
"Taste": "imkwAY2PtLw",
"Hearing": "mptjEoHF2aI",
"Smell": "v7Or809TTRU",
"Touch": "mWeTqNdSQlE",
"Sight": "xi2Xb56FpR4",
"All Five Senses": "xHwNIw6nHPg",












# Economics & Money

"What is a Bank": "fU4VBa-0ImU", "How ATMs Work": "iP_-3FrC1Sg", "Financial terminologies": "A9Xq3FGjpZA",
"Demand & Supply (Kids)": "j2BGJdCN8Cw", "What Are Taxes Used For": "rAhobLacBrs",
"Goods vs Services": "laKl9VRjaw0", "History of Money": "fcrQHC3jRsA", "Business ideas": "Je24erSNapw",



# Psychology

"How the Brain Makes Decisions": "ndDpjT0_IM0", "Habits & Routines": "MylSqdceXlU",
"Why We Dream": "09TRoxgVPjs", "Growth Mindset": "w6LLxTcVN9k",
"Why We Forget Things": "7GI4eTUyGSM", "Understanding Motivation": "XLPqy2oO-Eg",


# Health & Safety

"First Aid Basics": "2cMe3tBLaf4", "Road Safety Rules": "aT61nwd5U-s", "Fire Safety": "AWHGdWOI4kw",
"Internet Safety for Kids": "s-Iy3_5lC5g", "Hygiene Rules": "l6XGE-Xuq3M",
"Emergency Numbers & Help": "X3HTl-H69Dg",



# Creativity & Arts

"Drawing Techniques": "7SWvlUd2at8", "Landscaping": "eGGwB93IGwo", "Origami": "E10EtsY080c",
"Clay Modelling": "NDzbyqOCSOg", "Colour Theory": "YeI6Wqn4I78",
"Creative Writing for Kids": "KxVeE8Bik98", 


# Food & Nutrition

"Food groups": "pmgkj01uUTw", "Healthy food": "EhfOZMOF9W4",
"How Digestion Works (Kids)": "SD8kLAD1jnA", "Where Food Comes From": "v7HNTGXwQd0",
"Healthy vs Unhealthy food": "kvlWTI672sk", "Food Safety & Cleanliness": "e7zOSDg6x8c", "Details of Vitamins": "6gZzPE4Ln3s",

#Harmful effects of food

"Sugar": "vj1PB_NU__A",
"Junk food": "9U0XFhE_t50",
"Milk": "F5axBKDwM78",
"Fruit juice": "FZzi6HcWJqE",
"Coffee": "pGLuy5YuNhw",
"Tea": "9jW0ZOS6uHA",
"Cold drinks": "Cf16CSlxbdE",
"Processed food": "Zn-b93v0X00",
"Burger": "IQkLRMpN19w",

#Benefits of various vegetables

"Spinach": "Ks8eEnjB0ec",
"Lettuce": "dirs0a43DiY",
"Cabbage": "WPba1m0Z0tw",
"Kale": "OTPKrQMFfUU",
"Swiss Chard": "H94HsUm1vfM",
"Mustard Greens": "c9yW-TZXKGc",
"Collard Greens": "bS98Zv15XXo",
"Arugula": "zZP10V58cX4",
"Fenugreek Leaves": "719Y_gjFKG0",
"Coriander Leaves": "GRFzJwtZNWM",
"Parsley": "Cp5LIVk8k0s",
"Basil": "1J21ZW41tsc",
"Mint": "5W5t_UjKbTk",
"Dill": "eETQPc9qThY",
"Sorrel": "v6rzxL54Gb0",
"Bok Choy": "kpAWG2FD-dk",
"Napa Cabbage": "IMCgcldweuQ",
"Endive": "80bSsNlgAL0",
"Radicchio": "5JU8IQxXvzg",
"Watercress": "fd23_njWH9E",
"Carrot": "BbblxOSv7M4",
"Beetroot": "vHaHrDiBdmg",
"Radish": "vkZf24QC-9M",
"Turnip": "VkNMy5b2zYU",
"Sweet Potato": "oY7bayEHRXk",
"Potato": "ljsdtX27HpY",
"Yam": "EJ2mKoZT2RQ",
"Cassava": "gQZu9BMrv18",
"Parsnip": "KUJ_HJPTUto",
"Rutabaga": "RD4B06-horw",
"Salsify": "xpBRNkXh_8k",
"Taro Root": "-E-rIoRf3EY",
"Burdock Root": "lPU3DC25Tts",
"Jerusalem Artichoke": "N0oPDPm96bw",
"Onion": "ii7hJPmivyY",
"Garlic": "Y0RIsGOW-S4",
"Shallot": "SIHj6-2JQjk",
"Leek": "a1scRSQ1u0w",
"Spring Onion": "E7Esr0OHiLQ",
"Fennel Bulb": "Hd1Vj7Pepgk",
"Celery": "0nGJ6sd2rxk",
"Asparagus": "QtryEBOyZ9o",
"Bamboo Shoots": "0jY--H0h0Xs",
"Kohlrabi": "PiHIWeo3Fzo",
"Lotus Stem": "Ty8dSn4IhV4",
"Rhubarb": "OEoh9SR4ITI",
"Cauliflower": "cmVpCBWDw9A",
"Broccoli": "YDZZCW3m9nk",
"Artichoke": "30nuRm_t3rA",
"Banana Flower": "v9rgqz7QinU",
"Broccolini": "XEx7rT_wHkw",
"Romanesco": "D8r8HGJmwc4",
"Tomato": "kVR8mBaqAwk",
"Brinjal": "gHNtDNqaRFU",
"Capsicum": "7eXlJLTt6CY",
"Chili Pepper": "CK1nG5_sOVs",
"Cucumber": "2dgBi5bEPmY",
"Pumpkin": "JwzXNBv_Pxs",
"Bottle Gourd": "bnx_kKgZCDc",
"Ridge Gourd": "YWxX779QgSo",
"Sponge Gourd": "7kbMwjK9ZX4",
"Bitter Gourd": "Y0HUC7vtSj0",
"Snake Gourd": "MQYDnfTiLCM",
"Ash Gourd": "ZVOC0u4GbHk",
"Zucchini": "8p5ErDYloys",
"Squash": "Nx5FQDBrGOQ",
"Okra (Ladyfinger)": "KP4Zc3FuH7s",
"Chayote": "fVuL_2d-JHM",
"Tomatillo": "-b5qscKgo4A",
"Jalapeño": "6zBlIqlSEaI",
"Habanero Peppers": "SXrWGjaSzJI",
"Green Peas": "yFohZOPCwaI",
"Chickpeas": "s3O7MGk0Dro",
"French Beans": "TtMLHFfj0Gg",
"Cluster Beans": "iUKLsXfSWk4",
"Broad Beans": "rlYcJkKuTHU",
"Soybeans": "0gqLJcK52sc",
"Lentil Pods": "Y-XnjsbQxcA",
"Cowpeas": "ueULsY7qAf4",
"Snow Peas": "CKO6rAynDSM",
"Sugar Snap Peas": "nYAQGV_DZFE",
"Mushroom": "2fooP2ienR0",
"Shiitake Mushrooms": "IWwTK55uVks",
"Oyster Mushroom": "9yNGBghVX4s",
"Enoki Mushrooms": "PYO0NV7k2bM",
"Portobello Mushrooms": "6VtgIkQ511s",
"Morel Mushrooms": "U5Bty_5nEkA",
"Drumstick": "aPB1dRZBE_c",
"Banana Stem": "H3VSxGwQcwo",
"Winged Beans": "Fv4GzJcbF1k",
"Malabar Spinach": "Xmbfs8T20_o",
"Amaranth Leaves": "R8s5cKQnU7c",
"Elephant Foot Yam": "Lkl5PC3b1z8",
"Water Chestnut": "s6gwLIwpWc8",
"Seaweed": "7jxmmrSnZJI",
"Pointed Gourd": "0hWK1D2p51I",
"Wasabi Root": "w429YJPPAKA",
"Lotus Root": "T55qdrgFMhA",
"Perilla Leaves": "14W6Smj51yg",
"Curry Leaves": "_4gWnjdRXTY",
"Lemongrass": "yTkorSnzLL0",
"Chives": "kAdXaDDIJQI",
"Oregano": "Xvd0pE4dcdc",
"Thyme": "mTgZHsXRwa8",
"Rosemary": "IBvUJluIBu0",
"Sage": "PUM0aGnus4Y",
"Fiddlehead Fern": "sO_d2t0Dg9I",
"Celeriac": "FCrAlF4T6GE",
"Jicama": "n6YeZWo_A9I",
"Kangkong": "--XuGhJ88Wo",
"Ivy Gourd": "N9rmWaoFTZ0",
"Teasel Gourd": "dwMzpaZ_CYU",



#Benefits of various fruits

"Apple": "-o_HaNo7LWw",
"Banana": "NEzc5rmpF4k",
"Orange": "2dPO6Rfx7-8",
"Mango": "4-cR3N_NJT4",
"Grapes": "5BmWiai1RzM",
"Papaya": "VBNNCs2FmQ8",
"Pineapple": "WU5X3iL3Pso",
"Watermelon": "A_XHpn3UI8",
"Muskmelon": "bCRer2fm-f8",
"Pear": "VkdoQ5X5_Ig",
"Lemon": "jOUXGQ3TZrU",
"Lime": "kSFlGTYoHXo",
"Tangerine": "q9-9fIFFdW4",
"Clementine": "X-GWrrpBhLk",
"Grapefruit": "kghdn2p0wIg",
"Pomelo": "4frc8FpN8T0",
"Bergamot": "t4sc-3TTUGo",

"Strawberry": "u3oLQcx6FtE",
"Blueberry": "vdJIHC0TvJQ",
"Raspberry": "uaA9sbpdpok",
"Blackberry": "8RVUBlWIVWw",
"Cranberry": "QqGFk2jUwrQ",
"Gooseberry": "O21VWukqDSc",
"Mulberry": "fbg7yYRssqM",
"Elderberry": "vfY5O2ztboU",

"Coconut": "3zn5V0DeJ-I",
"Jackfruit": "5QDC6h6PADk",
"Lychee": "rDNb2Nze__E",
"Longan": "_zMFihxA0xY",
"Rambutan": "4uafgJRM2PU",
"Durian": "8hq6tPkxYZo",
"Passion fruit": "OY0x0re7hLY",
"Guava": "YWj5aX2PENA",
"Star fruit": "nEnlDc6c2gg",
"Dragon fruit": "MNo4ddAfPxU",
"Bread fruit": "cpQyi5ywpYs",
"Soursop": "JLsNu7gCJu4",
"Custard apple": "0QgdQYKGIpM",
"Sugar apple": "0QgdQYKGIpM",
"Chikoo": "gTPpIP7pYHg",
"Mangosteen": "n8Gg2Ye7DXk",

"Peach": "JUe7X0ZEXUM",
"Plum": "ISkLcLLsjAs",
"Cherry": "xVnsM-N1_Xs",
"Apricot": "OAxdcmZBftI",
"Nectarine": "-IgcL4EthAg",
"Olive": "Y2yBruKH6FY",
"Dates": "xsCqbQ-318A",
"Quince": "nB_OiisPSuk",

"Jamun (Java plum)": "T1E8SOvbq8Y",
"Bael": "YBz804oo6Ls",
"Wood apple": "EouaiIEVH4g",
"Kokum": "DAVm-nTaTZY",
"Phalsa": "yuuPlxfMbsM",
"Snake fruit": "kmhUpFGYLlQ",
"Langsat": "E6t3csIJ9o4",
"Ice apple": "2sEcV1evXzM",

"Kiwi": "mKVdtqbgxM4",
"Fig": "r_Sk6Rq2y7g",
"Pomegranate": "5l6tcQncnnk",
"Tamarind": "ZSOor5w6K6A",
"Avocado": "79DDXFpK4Ts",
"Persimmon": "ZUDv7LN3ilw",
"Loquat": "FHdTlmHdCi0",

"Miracle fruit": "_S_yqe7BLyI",
"Lucuma": "0hpZ1dCvh7Q",
"Santol": "nOWkAYomDCU",
"Surinam cherry": "KOGKfd8VPdc",
"Horned melon": "c86AOSLIROI",
"Jabuticaba": "4FgSRhmXH80",
"Feijoa": "VJiZOA6XYxs",
"Cantaloupe": "NCXHwNM46Iw",

"Almond": "_Gd5lkiB0y0",
"Cashew": "DD2ajId1Jj8",
"Walnut": "TfA-xOKckSs",
"Pistachio": "6AkhNgFSXBM",
"Hazelnut": "NvfjLp02QVQ",
"Brazilnut": "I8Un2dstqQk",
"Macadamia": "LsPJeQLOkXk",
"Pecan": "6zGpZCGROuA",
"Arecanut": "OOiXltpCn_4",
"Raisins": "Qu1Kkuis9ew",





# Transportation

"Inventions of aeroplanes": "NpqU3eSeS1c", "How Trains Work": "L9Rt_5T5cGU",
"Bicycles & Gears": "oifV7-zYLhg", "Ships & Submarines": "LTUFm7P15cE",
"What is Hyperloop": "S5fOWB6SNqs", "Future Transport ": "qb3SMLxz4JY",



# Careers & Future Jobs

"Jobs and Ocuupations": "ugsRzHMIF2o", "Different types of Doctors": "BHfmsZnu7GQ",
"Space Careers": "IagxIpCvMl4", "Best jobs ever": "Nej8PkTgbhI",
"High paying jobs": "P-Nn5B2U-CM", 



# Culture & Society

"World Traditions": "2Seg3t7PQQI", "Family Structures": "GnelN7Y70xs",
"Manners Around the World": "WxjHzlQVtZs", "Languages of the World": "C_-8SUXLY6I",
"World cuisines": "Lb0m0MF1924", "Traditional Clothing": "OyctNZgiMJk",



# Logic & Critical Thinking

"Puzzles & Riddles": "VHK-by9y8sA", "Logical Reasoning": "Aq5ms0s_GuQ",
"Spot the Pattern": "CzFLDtvN_Xk", "Sequencing": "7aL78cZLUKc",
"Cause & Effect": "T17uXLNMi6E", "Foundational thinking": "GBI6vCHeooM",
"Matching,Sorting and games": "WBGcTq3aiY4", "Analogy": "71iIhK2eLLQ",


# Ethics & Values

"Honesty": "0VWK4plxkjk", "Responsibility": "UB4TKI7G8s0", "Respecting Privacy": "G7MIi-SogAc",
"Environmental Responsibility": "KY4mlk5CKrk", "Anti-Bullying": "XkTqM-72w5k",
"Equality": "Yt_2Hqel0Iw",



# Daily Life Skills

"Doing Basic Household Tasks": "p1WG8VdZuKo", "Packing a School Bag": "jFzxr9MrRXA",
"Cleaning & Tidying": "-oWT9m7iNv0", "Shopping Basics": "QNGxlv5X-Oo",
"Talk about Public Transport": "AF2gr6r89wc", "Understanding Labels": "R-o-83k8dP0",



# Weather & Natural Disasters

"Floods": "j4yuzWuMLGQ", "Droughts": "O5a6yHSI0L0", "Hurricanes & Cyclones": "J2__Bk4dVS0",
"Tsunamis": "MfsugkikLJI", "Lightning": "ZR0O1wodxyE", "Cyclone": "oXNOyvs4xZU",
"Natural disasters names": "E0_EkX5AlNg",



# Mythology & Folk Stories

"Greek Mythology": "wTxW7sa2rtg", "Indian Mythology": "Ygfwi1wjP9M",
"Norse Mythology": "GDzmuV8D-88", "Folk Tales Around the World": "NncRwyOFA4E",
"Fairy Tales Explained": "zDBvqNcbGI", "Myths|Legends|Folk tales|Failry tales": "kpLqEKLrxnc",
"Mahabharat": "pHwgLLFyGMc", "Ramayan": "6Dp0iJNYKqk",


# Rocks & Minerals

"Rocks and Minerals": "hxN0JatEZi4", "Types of Rocks": "qFEBPD3JEOM",
"Rock Cycle": "uRaVu52eCBQ", "Rock Uses": "Vwcm-KFtLLM",
"Soil and Types": "uFgfeS_VmBg",


# Dog Breeds

"100 Dog Breeds": "8MlqcBAyq1g", "Golden Retriever": "TXFLZ20mv3g",
"German Shepherd": "rQ83mpQLBOY", "Doberman": "PaCWHpmvbCc",
"Labrador": "fAYTqXbZR9U", "Bulldog": "dT_Ai3jt2kk",
"Pomeranian": "d8_BEKwbwBk", "Siberian Husky": "tbn8IF0D9Yg",
"Dalmatian": "BRrnz3F6Ucg", "Beagle": "eNGRyoVA4pg",
"Chihuahua": "X4TVV5_cLGo",


# Secret Codes

"Morse Code": "0CYpik24pRU", "Invisible Ink": "AOVD7WgFP2s",
"Fingerprints": "sMnTbG0-YUk", "Caesar Cipher": "QuXhWlekrNU",


# Basic Concepts

"MS Word": "KCfwX98EWIc", "MS Excel": "wbJcJCkBcMg",
"MS PowerPoint": "KqgyvGxISxk", "Server": "UjCDWCeHCzY",
"Google Drive": "luH4t1kZ5CA", "Google Docs": "OBITNezSmLY",
"Google Sheets": "UvCANQhqsSw", "Google Maps": "CU4dBJk97AI",
"Gmail": "CtRgwJaW2N4",


# Natural Wonders of the World

"Northern Lights": "4W0RcxZ6bGc", "Grand Canyon": "_RMZSgwjJeY",
"Great Barrier Reef": "qmCtYtC_0fs", "Mount Everest": "g6eseuiBoz8",
"Victoria Falls": "3T-z-715NPA", "Dead Sea": "MJl6wY1G8Ls",
"Amazon Rainforest": "_OKdzTGRa4o", "Paricutin Volcano": "0XHDZYhVeQ4",
"Harbor of Rio": "fdI-9rUZu6A", "The Nile River": "ERbQ3GsbFxM",



#Miscellaneous
     "Advantages of drinking water": "31F0laJjyy8",
     "How do plants help us": "Z9mOrNcX4j0",
     "Categories of animals": "5hFoZq0qgrM",
     "Animals and their sounds": "GsoPwyStpJg",
     "Vertebrates & Invertebrates": "LGxmZqQBOdU",
     "Types of water bodies": "U-rUl_OFBq0",
     "Names of animals,birds & flowers": "MssglYt2aLk",
     "Musical instruments": "1hWb6Qu6A1w",
     "Names and sounds of birds": "WhRpW0cVmds",
     "Vehicle names": "_cn0pod5KRc",
     "Carnivores,herbivores,omnivores": "VVjqDzTYfyw",
     "Human body": "AHQGNb0zBgg",
     "Toddler learning": "WOn8gdKrZzY",
     "Finger abacus": "5u55IhRGRAk",
     "Scientific instruments": "GNP51BjotVc",



    
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
     "Economics & Money": "-dQ6ak7dHhk",
     "Social skills": "Myf2CUx9E60",
     "Healthy Habits": "jBEVDM0BEdI",
     "Safety": "2-cRbXbkgYI",
     "Creativity & Arts": "bsbpfdyQtGw",
     "Food & Nutrition": "fagLa_46HkY",
     "Transportation": "PcjIyMTuU0o",
     "Careers & Future Jobs": "Iaxjhm21yhc",
     "Communities": "04lO0ISBT40",
     "Logic & Critical Thinking": "C-dvWa-IIG4",
     "Ethics & Values": "eDTCua9fgMU",
     "Daily routine": "MCQoWGAmj7w",
     "Weather & Natural Disasters": "FCxCkXI4fc8",
     "Mythology & Folk Stories": "2ccD-VkcDpA",
     "Advantages of drinking water": "31F0laJjyy8",
     "How do plants help us": "Z9mOrNcX4j0",
     "Categories of animals": "5hFoZq0qgrM",
     "Animals and their sounds": "GsoPwyStpJg",
     "Vertebrates & Invertebrates": "LGxmZqQBOdU",
     "Types of water bodies": "U-rUl_OFBq0",
     "Names of animals,birds & flowers": "MssglYt2aLk",
     "Musical instruments": "1hWb6Qu6A1w",
     "Names and sounds of birds": "WhRpW0cVmds",
     "Vehicle names": "_cn0pod5KRc",
     "Carnivores,herbivores,omnivores": "VVjqDzTYfyw",
     "Human body": "AHQGNb0zBgg",
     "Toddler learning": "WOn8gdKrZzY",


    
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

# --- 3. API SETUP (USING GROQ) ---
from groq import Groq 

try:
    # Use the name you set in your secrets store: 'eli5'
    GROQ_API_KEY = st.secrets["eli5"] 
    
    client = Groq(api_key=GROQ_API_KEY) 
except KeyError:
    # Update the error message to reflect the expected key name
    st.error("⚠️ GROQ API Key not found in Streamlit Secrets. Please ensure the key 'eli5' is set correctly.")
    st.stop() 
except Exception as e:
    st.error(f"⚠️ GROQ API configuration failed: {e}")
    st.stop()

# --- MULTILINGUAL QUERY GENERATION FUNCTION (CACHED) ---
# NOTE: This function must be defined BEFORE it is called in Section 6.

@st.cache_data(ttl=3600)
def generate_youtube_query(topic, category, language_name, _client):
    if language_name == "English":
        return f"{topic} {category} educational video for kids safe mode child lock 10 minute"
    
    # Use a highly stable model for search term generation
    search_model = "llama-3.1-8b-instant"
    
    prompt = (
        f"You are a YouTube search expert. Generate the best possible, strictest search query "
        f"to find a relevant, long educational video (10+ minutes) about the topic '{topic}' "
        f"in the category '{category}'. "
        f"The query must be strictly in **{language_name}** and targeted "
        f"at children's education. Output ONLY the search query string, nothing else. "
        f"Example for French: 'Les volcans geographie video éducative pour enfants 10 minutes'"
    )
    try:
        response = _client.chat.completions.create(
            model=search_model,
            messages=[{"role": "user", "content": prompt}]
        )
        # Clean up output rigorously
        search_query = response.choices[0].message.content.strip().replace('"', '').replace("'", '').split('\n')[0].strip()
        return search_query
    except Exception:
        # Fallback to a complex English query if AI generation fails
        return f"{topic} {category} educational video for kids safe mode child lock 10 minute"






# --- QUIZ GENERATION FUNCTION (Cached and Fast - 5 QUESTIONS) ---
@st.cache_data(ttl=600) # Cache quiz for 10 minutes
def generate_quiz(_client, topic, category, lang):
    # Use the 8B model for speed and low cost
    quiz_model = "llama-3.1-8b-instant"
    
    prompt = (
        f"Generate **5 separate multiple-choice quiz questions** based on the topic '{topic}' "
        f"from the '{category}' area. The questions and options must be in **{lang}**."
        f"Format your response strictly as a single JSON object with the following structure: "
        f"{{'quizzes': [{{'question': '...', 'options': ['a', 'b', 'c', 'd'], 'correct_index': 0}}, ...]}}"
    )
    
    try:
        response = _client.chat.completions.create(
            model=quiz_model,
            messages=[
                {"role": "system", "content": "You are a quiz master generating strict, clean JSON output containing a list of 5 quizzes."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )
        import json
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        print(f"Quiz Generation Error: {e}")
        return None






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


# --- 5. SEARCH INPUT & CATEGORY LOGIC (Curated Flow Only) ---

# Initialize variables to avoid NameError if user doesn't interact
query = None
category = "General Knowledge"
is_curated_search = True # ALWAYS TRUE now

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    
    # EXPLANATION MODE SELECTOR (Kept for Story Mode feature)
    explanation_mode = st.radio(
        "Select Explanation Style:",
        ["Informative Mode (Facts & Analogies)", "Story Mode (Narrative)"],
        horizontal=True,
        index=0,
        key='explanation_mode'
    )
    
    # LANGUAGE SELECTOR
    selected_language = st.selectbox(
        "Select Language for Explanation:",
        options=list(LANGUAGES.keys()),
        index=0,
        key="language_select"
    )
    st.write("---") 
    
    # Initial choice: The UI will only show the curated option now.
    mode = st.radio(
        "How do you want to find your topic?", 
        [
            # "Search Any Topic",  <-- REMOVED FROM UI
            "Choose Specific Category"
        ], 
        horizontal=True, 
        index=0 # Index 0 now defaults to the remaining option
    )

    st.write("---")
    
    # --- CURATED CONTENT PATH (The ONLY active path) ---
    
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
        is_curated_search = True # Ensure this flag is set
        
        # Visual check for the user
        st.info(f"You selected: **{query}** (in the {category} category)")

# NOTE: The logic for "if mode == 'Search Any Topic':" is completely eliminated,
# ensuring the script only executes the curated path.
# --- 6. LOGIC (CRASH PROOF) ---
if query:
    st.write("---") 
    
    # Get the language data
    lang_data = LANGUAGES[selected_language]
    language_keyword = lang_data["name"]
    
    # --- QUIZ STATE INITIALIZATION ---
    quiz_key = f"quiz_{query}_{language_keyword}_{st.session_state.get('explanation_mode', 'Informative')}"
    if quiz_key not in st.session_state:
        st.session_state[quiz_key] = None
    
    # --- AUDIO STATE INITIALIZATION AND CHECK ---
    # Initialize local variable to store audio data (bytes)
    audio_bytes_to_display = None
    
    if st.session_state.get('tts_trigger'):
        st.session_state['tts_trigger'] = False # Reset trigger immediately
        
        if st.session_state.get('last_explanation'):
            with st.spinner("Generating audio, please wait..."):
                # Call the memory-based function (CORRECT NAME)
                audio_bytes_to_display = generate_audio_bytes( 
                    st.session_state['last_explanation'], 
                    st.session_state['last_lang_code']
                )
    
    
    with st.spinner(f'⚡ Brainstorming in {language_keyword}...'):
        
        # --- CRITICAL: Generate Localized Video Search Query (Uses AI) ---
        video_search_query = generate_youtube_query(query, category, language_keyword, client)

      # 1. GENERATE TEXT (With Safety Net using GROQ)
        text_response = ""
        try:
            # --- DYNAMIC PROMPT ADJUSTMENT ---
            if st.session_state.get('explanation_mode') == "Story Mode (Narrative)":
                mode_instruction = "Explain this concept as a simple, fun narrative story, using characters and a plot."
            else:
                mode_instruction = "Explain this concept using simple facts and analogies."

            prompt_content = (
                f"{mode_instruction} The topic is '{query}' (Category: {category}). "
                f"Generate the entire explanation in **{language_keyword}**. "
                f"Keep the explanation concise, around 500 words."
            )
            
            # --- TOKEN LIMIT FIX ---
            if language_keyword == "English":
                token_limit = 1000 
            else:
                token_limit = 1800 

            # GROQ API Call 
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant", 
                messages=[
                    {"role": "system", "content": "You are an excellent teacher simplifying complex topics for children."},
                    {"role": "user", "content": prompt_content}
                ],
                max_tokens=token_limit # <-- DYNAMIC LIMIT USED HERE
            )
            text_response = response.choices[0].message.content
            
            # --- PERSIST TEXT AND LANGUAGE FOR FUTURE TTS/QUIZ CALL ---
            st.session_state['last_explanation'] = text_response
            st.session_state['last_lang_code'] = language_keyword
            
        except Exception as e: # <--- THIS LINE MUST BE ALIGNED WITH 'try'
            # Fallback text simplified
            error_message = str(e)
            
            if 'authentication' in error_message.lower() or 'invalid api key' in error_message.lower():
                detail = "API Key error. Check the GROQ key in Streamlit Secrets."
            elif 'rate limit' in error_message.lower():
                detail = "We've hit a temporary rate limit. Try again in 30 seconds."
            else:
                detail = "The AI brain is temporarily busy or resting."
                
            text_response = f"""
            ### 🚦 AI Service Failure!
            
            **Reason:** {detail}
            
            Don't worry! Your **Images** and **Videos** below are still working perfectly. 👇
            
            *(Please try searching again in a moment!)*
            """
        # 2. CACHE/GENERATE QUIZ (Runs once per session/topic)
        if st.session_state[quiz_key] is None:
            with st.spinner("Generating fun quiz (This may take a moment)..."):
                st.session_state[quiz_key] = generate_quiz(client, query, category, language_keyword)


        # 3. GENERATE IMAGE (Pollinations API)
        clean_query = query.replace(" ", "-")
        image_url = f"https://image.pollinations.ai/prompt/3d-render-of-{clean_query}-bright-colors-pixar-style-white-background-4k"
        
        # 4. VIDEO SEARCH: HYBRID (Curated or Dynamic)
        video_id = None
        
        if is_curated_search:
            # --- PATH A: CURATED SEARCH (Category Mode - Guaranteed 10+ Min) ---
            video_id = VIDEO_DB.get(query, VIDEO_DB["DEFAULT_VIDEO_ID"])
            
            if video_id in VIDEO_DB.values(): 
                st.info("Video selected from the highly-curated educational database (10+ minutes guaranteed).")
            else:
                category_fallback_id = CATEGORY_DEFAULTS.get(category, CATEGORY_DEFAULTS["DEFAULT_GENERIC"])
                video_id = category_fallback_id
                st.warning(f"Curated video not found for '{query}'. Showing high-quality default video for {category}.")

        else:
            # --- PATH B: DYNAMIC SEARCH (Search Bar Mode - Localized) ---
            try:
                # We use the AI-generated video_search_query from the top of this block
                results = YoutubeSearch(video_search_query, max_results=1).to_dict()
                
                if results and results[0].get('id'):
                    video_id = results[0]['id']
                    st.warning(f"Using dynamic YouTube search localized for {language_keyword}. Video length and content relevance may vary.")
                else:
                    video_id = CATEGORY_DEFAULTS.get(category, CATEGORY_DEFAULTS["DEFAULT_GENERIC"])
                    st.warning(f"Dynamic search failed. Showing high-quality default video for {category}.")
            except Exception:
                video_id = CATEGORY_DEFAULTS["DEFAULT_GENERIC"]
                st.warning("All searches failed. Showing absolute general fallback video.")


        # --- DISPLAY RESULTS ---
        tab1, tab2 = st.tabs(["📖 THE STORY", "📺 VISUALS"])

        # TAB 1: TEXT AND QUIZ
        with tab1:
            st.markdown("## 📖 Explanation & Quiz")

            # --- AUDIO PLAYER CONTROLS ---
            st.button(
                f"🔊 Read Explanation Aloud ({language_keyword})", 
                key='tts_button', 
                on_click=lambda: st.session_state.update(tts_trigger=True)
            )
            st.markdown("---")
            
            # Display generated audio if the bytes were successfully generated
            if audio_bytes_to_display:
                # Play the raw bytes (shows full controls: progress bar, play/pause)
                st.audio(audio_bytes_to_display, format='audio/mp3') 
                st.markdown("---")
            elif st.session_state.get('tts_trigger'):
                 st.warning("Please wait a moment for the audio to be generated and try clicking the button again.")
            
            st.markdown(text_response)
            
            st.markdown("---")
            
            # ====== QUIZ DISPLAY SECTION (5 QUESTIONS) ======
            quiz_container = st.session_state[quiz_key]
            
            if quiz_container and 'quizzes' in quiz_container and isinstance(quiz_container['quizzes'], list):
                st.markdown("### 🤔 Test Your Knowledge! (5 Questions)")
                
                if 'quiz_results_history' not in st.session_state:
                    st.session_state['quiz_results_history'] = {}

                # Iterate through all 5 quizzes
                for i, quiz_data in enumerate(quiz_container['quizzes']):
                    st.markdown(f"**Question {i+1}:** {quiz_data['question']}")
                    
                    result_key = f'result_q_{i}_{quiz_key}'

                    with st.form(key=f'quiz_form_{i}'):
                        selected_option = st.radio(
                            "Select Answer:",
                            options=quiz_data['options'],
                            index=None,
                            key=f'user_selection_{i}'
                        )
                        
                        check_button = st.form_submit_button(f"Check Answer {i+1}")

                    # Handle feedback after submission
                    if check_button and selected_option is not None:
                        user_index = quiz_data['options'].index(selected_option)
                        correct_index = quiz_data['correct_index']
                        
                        if user_index == correct_index:
                            st.session_state['quiz_results_history'][result_key] = True
                        else:
                            st.session_state['quiz_results_history'][result_key] = False
                            
                    # Display persistent feedback
                    if result_key in st.session_state['quiz_results_history']:
                        if st.session_state['quiz_results_history'][result_key]:
                            st.success(f"🎉 Question {i+1}: Correct! Excellent.")
                        else:
                            st.error(f"❌ Question {i+1}: Incorrect. The correct answer was: {quiz_data['options'][correct_index]}")

        # TAB 2: VISUALS
        with tab2:
            col_a, col_b = st.columns(2)
            
            with col_a:
                st.markdown("### 🎨 3D Drawing")
                st.image(image_url, use_container_width=True, caption=f"A 3D image of '{query}'")
                
            with col_b:
                st.markdown("### 🎥 Explanation Video")
                st.video(f"https://www.youtube.com/watch?v={video_id}")
                
                # LANGUAGE TIP
                st.markdown("""
                    <div style="
                        background-color: #1877F2; padding: 10px; border-radius: 8px; margin-top: 15px; text-align: center; box-shadow: 2px 2px 5px rgba(0,0,0,0.2);
                    ">
                        <p style="color: #FFFFFF !important; font-weight: 800; font-size: 1rem; margin: 0;">
                            LANGUAGE TIP: Video audio may be in English for stability.
                            <br>
                            TO TRANSLATE SUBTITLES IN YOUR FAVOURITE LANGUAGE : CLICK  SETTINGS ⚙️ > SUBTITLES/CC > AUTO-TRANSLATE ON THE PLAYER ABOVE!
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
