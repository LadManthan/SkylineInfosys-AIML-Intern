import streamlit as st

st.set_page_config(
    page_title="Cricket",
    page_icon=":cricket:",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "About": "This is a page about cricket using Streamlit.",
    }
)

st.markdown(f"""
    <style>
    /* Main background */
    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(0deg,rgba(42, 123, 155, 1) 0%, rgba(87, 199, 133, 1) 50%, rgba(237, 221, 83, 1) 100%);
        background-size : cover;
    }}
    
    [data-testid="stHeader"], [data-testid="stStatusWidget"] {{
        background-color : rgba(0,0,0,0);
    }}
    
    [data-testid="stSidebar"] {{
        background: rgba(255, 255, 255, 0.61);
        backdrop-filter: blur(6.4px);
    }}

    /* CENTER SIDEBAR BUTTONS */
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {{
        align-items: center;
        text-align: center;
    }}
    
    /* Make buttons look like uniform menu items */
    [data-testid="stSidebar"] .stButton button {{
        width: 200px;
    }}

    [data-testid="stTabs"] {{
        display: flex;
        justify-content: center;
        gap: 50px;
    }}

    [data-testid="stVerticalBlock"] > div {{
        text-align: center;
    }}
    </style>
    """, 
    unsafe_allow_html=True
)
    
st.sidebar.title("Select Team")
if st.sidebar.button("India"):
    st.session_state.selected_team = "India"
if st.sidebar.button("Australia"):
    st.session_state.selected_team = "Australia"
if st.sidebar.button("South Africa"):
    st.session_state.selected_team = "South Africa"
if st.sidebar.button("New Zealand"):
    st.session_state.selected_team = "New Zealand"
    
team_player = {
    "India": {
        "Batsman": ["Rohit Sharma (c)", "Shubman Gill", "Virat Kohli", "Shreyas Iyer", "KL Rahul (wk)", "Ishan Kishan", "Suryakumar Yadav"],
        "Bowler": ["Jasprit Bumrah", "Mohammed Shami", "Mohammed Siraj", "Kuldeep Yadav", "Shardul Thakur"],
        "All-rounder": ["Hardik Pandya", "Ravindra Jadeja", "Ravichandran Ashwin"]
    },
    "Australia": {
        "Batsman": ["Pat Cummins (c)", "Steve Smith", "David Warner", "Travis Head", "Marnus Labuschagne", "Josh Inglis (wk)", "Alex Carey"],
        "Bowler": ["Mitchell Starc", "Josh Hazlewood", "Adam Zampa"],
        "All-rounder": ["Glenn Maxwell", "Mitchell Marsh", "Marcus Stoinis", "Cameron Green", "Sean Abbott"]
    },
    "South Africa": {
        "Batsman": ["Temba Bavuma (c)", "Quinton de Kock (wk)", "Reeza Hendricks", "Rassie van der Dussen", "Aiden Markram", "Heinrich Klaasen", "David Miller"],
        "Bowler": ["Kagiso Rabada", "Lungi Ngidi", "Anrich Nortje", "Tabraiz Shamsi", "Keshav Maharaj", "Gerald Coetzee"],
        "All-rounder": ["Marco Jansen", "Andile Phehlukwayo"]
    },
    "New Zealand": {
        "Batsman": ["Kane Williamson (c)", "Will Young", "Mark Chapman", "Tom Latham (wk)", "Glenn Phillips", "Devon Conway"],
        "Bowler": ["Trent Boult", "Tim Southee", "Ish Sodhi", "Matt Henry", "Lockie Ferguson"],
        "All-rounder": ["Daryl Mitchell", "Mitchell Santner", "James Neesham", "Rachin Ravindra"]
    }
}

if 'selected_team' not in st.session_state:
    st.markdown("<h1>Select team from the sidebar to view the squad.</h1>", unsafe_allow_html=True)
    
else:
    current_team = st.session_state.selected_team
    st.title(f"{current_team} Squad")

    tab1, tab2, tab3= st.tabs(["Batsman", "Bowler", "All-rounder"])
    team_info = team_player.get(current_team, {"Batsman":[], "Bowler":[], "All-rounder":[]})

    with tab1:
        for player in team_info["Batsman"]:
            st.write(player)
        
    with tab2:
        for player in team_info["Bowler"]:
            st.write(player)

    with tab3:
        for player in team_info["All-rounder"]:
            st.write(player)