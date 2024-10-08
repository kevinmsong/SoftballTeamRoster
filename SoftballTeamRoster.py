import streamlit as st
import json
import os

st.set_page_config(page_title="Shady Sluggers", page_icon="🥎", layout="wide")

# Custom CSS for mobile optimization and layout
st.markdown("""
<style>
    .stButton > button {
        width: 100%;
        padding: 0.1rem 0.5rem;
        font-size: 0.8rem;
    }
    .stSelectbox, .stTextInput {
        padding: 0.1rem;
        font-size: 0.8rem;
    }
    .row-widget.stButton {
        margin-bottom: 0.25rem;
    }
    .inline-buttons {
        display: flex;
        justify-content: space-between;
        gap: 5px;
    }
    .inline-buttons .stButton {
        flex: 1;
    }
    .inline-buttons .stButton button {
        width: 100%;
        padding: 0.1rem;
        font-size: 0.8rem;
    }
    .version {
        font-size: 0.8rem;
        color: #888;
        margin-top: -1rem;
        margin-bottom: 1rem;
    }
    .nav-buttons {
        display: flex;
        justify-content: center;
        margin-bottom: 1rem;
    }
    .nav-buttons .stButton {
        margin: 0 0.5rem;
    }
    .player-row {
        margin-bottom: 0.5rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid #f0f0f0;
    }
    .batting-order .player-row {
        margin: 0;
        padding: 0.1rem 0;
        border-bottom: none;
        line-height: 1.2;
    }
    .batting-order .player-info {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .batting-order .player-name {
        font-weight: bold;
    }
    .batting-order .player-position {
        color: #666;
        font-size: 0.9em;
    }
    .batting-order .player-alternate {
        font-size: 0.8em;
        color: #888;
        margin-left: 1em;
    }
    .st-ae {
        gap: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Define softball positions
POSITIONS = [
    "Pitcher", "Catcher", "First Base", "Second Base", "Third Base",
    "Shortstop", "Left Fielder", "Center Fielder", "Right Fielder"
]

# File to store roster data
ROSTER_FILE = "roster_data.json"

def load_roster():
    if os.path.exists(ROSTER_FILE):
        with open(ROSTER_FILE, "r") as f:
            return json.load(f)
    return {"roster": [], "positions": {}, "alternates": {}}

def save_roster(data):
    with open(ROSTER_FILE, "w") as f:
        json.dump(data, f)

def roster_management_page():
    st.subheader("Roster Management")
    
    # Load roster data
    roster_data = load_roster()

    # Ensure all players have positions and alternates
    for player in roster_data["roster"]:
        if player not in roster_data["positions"]:
            roster_data["positions"][player] = POSITIONS[0]
        if player not in roster_data["alternates"]:
            roster_data["alternates"][player] = ""

    # Add player form
    with st.form(key='add_player_form'):
        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            new_player = st.text_input("Player name", key="new_player_input")
        with col2:
            new_position = st.selectbox("Position", POSITIONS, key="new_position")
        with col3:
            submit_button = st.form_submit_button(label='Add')
        if submit_button and new_player and new_position:
            if new_player not in roster_data["roster"]:
                roster_data["roster"].append(new_player)
                roster_data["positions"][new_player] = new_position
                roster_data["alternates"][new_player] = ""
                save_roster(roster_data)
                st.rerun()
            else:
                st.error(f"'{new_player}' already exists.")

    # Display and manage roster
    updated = False
    for i, player in enumerate(roster_data["roster"]):
        with st.container():
            st.markdown(f"<div class='player-row'>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns([1, 1, 1])
            
            with col1:
                st.write(f"{i+1}. {player}")
            
            with col2:
                position = st.selectbox(
                    "Position",
                    POSITIONS,
                    index=POSITIONS.index(roster_data["positions"][player]),
                    key=f"pos_{i}",
                    label_visibility="collapsed"
                )
                if position != roster_data["positions"][player]:
                    roster_data["positions"][player] = position
                    updated = True
            
            with col3:
                alternate = st.text_input(
                    "Alternate",
                    value=roster_data["alternates"][player],
                    key=f"alt_{i}",
                    label_visibility="collapsed"
                )
                if alternate != roster_data["alternates"][player]:
                    roster_data["alternates"][player] = alternate
                    updated = True

            # Inline buttons
            st.markdown("<div class='inline-buttons'>", unsafe_allow_html=True)
            col4, col5, col6 = st.columns(3)
            with col4:
                if st.button("❌", key=f"remove_{i}", help="Remove player"):
                    roster_data["roster"].remove(player)
                    del roster_data["positions"][player]
                    del roster_data["alternates"][player]
                    updated = True
            
            with col5:
                if st.button("⬆️", key=f"up_{i}", help="Move up", disabled=(i == 0)):
                    roster_data["roster"][i], roster_data["roster"][i-1] = roster_data["roster"][i-1], roster_data["roster"][i]
                    updated = True
            
            with col6:
                if st.button("⬇️", key=f"down_{i}", help="Move down", disabled=(i == len(roster_data["roster"]) - 1)):
                    roster_data["roster"][i], roster_data["roster"][i+1] = roster_data["roster"][i+1], roster_data["roster"][i]
                    updated = True
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)

    # Save changes if any updates were made# Save changes if any updates were made
    if updated:
        save_roster(roster_data)
        st.rerun()

def batting_order_page():
    st.subheader("Batting Order")
    roster_data = load_roster()
    
    st.markdown("<div class='batting-order'>", unsafe_allow_html=True)
    for i, player in enumerate(roster_data["roster"]):
        position = roster_data["positions"][player]
        alternate = roster_data["alternates"][player]
        st.markdown(f"""
        <div class='player-row'>
            <div class='player-info'>
                <span class='player-name'>{i+1}. {player}</span>
                <span class='player-position'>{position}</span>
            </div>
            {f"<div class='player-alternate'>Alternate: {alternate}</div>" if alternate else ""}
        </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

def main():
    st.title("🥎 Shady Sluggers Team Roster 🙏")
    st.markdown("<p class='version'>Version 1.2</p>", unsafe_allow_html=True)

    # Navigation
    st.markdown("<div class='nav-buttons'>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        roster_button = st.button("Roster Management")
    with col2:
        order_button = st.button("Batting Order")
    st.markdown("</div>", unsafe_allow_html=True)

    # Page state
    if 'page' not in st.session_state:
        st.session_state.page = 'roster'

    # Navigation logic
    if roster_button:
        st.session_state.page = 'roster'
    elif order_button:
        st.session_state.page = 'order'

    # Display the appropriate page
    if st.session_state.page == 'roster':
        roster_management_page()
    else:
        batting_order_page()

if __name__ == "__main__":
    main()
