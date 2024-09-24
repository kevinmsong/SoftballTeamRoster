import streamlit as st
import json
import os

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

def main():
    st.title("Shady Sluggers Team Roster Management")

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
        new_player = st.text_input("Enter player name")
        new_position = st.selectbox("Select position", POSITIONS, key="new_position")
        submit_button = st.form_submit_button(label='Add Player')
        if submit_button and new_player and new_position:if submit_button and new_player and new_position:
            if new_player not in roster_data["roster"]:
                roster_data["roster"].append(new_player)
                roster_data["positions"][new_player] = new_position
                roster_data["alternates"][new_player] = ""
                save_roster(roster_data)
                st.rerun()
            else:
                st.error(f"Player '{new_player}' already exists in the roster.")

    # Display and manage roster
    st.subheader("Roster Management")
    updated = False
    for i, player in enumerate(roster_data["roster"]):
        col1, col2, col3 = st.columns([3, 2, 2])
        
        with col1:
            st.write(f"{i+1}. {player}")
        
        with col2:
            position = st.selectbox(
                "Position",
                POSITIONS,
                index=POSITIONS.index(roster_data["positions"][player]),
                key=f"pos_{i}"
            )
            if position != roster_data["positions"][player]:
                roster_data["positions"][player] = position
                updated = True
        
        with col3:
            alternate = st.text_input(
                "Alternate",
                value=roster_data["alternates"][player],
                key=f"alt_{i}"
            )
            if alternate != roster_data["alternates"][player]:
                roster_data["alternates"][player] = alternate
                updated = True

        col4, col5, col6 = st.columns([1, 1, 1])
        
        with col4:
            if st.button("Remove", key=f"remove_{i}", use_container_width=True):
                roster_data["roster"].remove(player)
                del roster_data["positions"][player]
                del roster_data["alternates"][player]
                updated = True
        
        with col5:
            if st.button("⬆️", key=f"up_{i}", use_container_width=True, disabled=(i == 0)):
                roster_data["roster"][i], roster_data["roster"][i-1] = roster_data["roster"][i-1], roster_data["roster"][i]
                updated = True
        
        with col6:
            if st.button("⬇️", key=f"down_{i}", use_container_width=True, disabled=(i == len(roster_data["roster"]) - 1)):
                roster_data["roster"][i], roster_data["roster"][i+1] = roster_data["roster"][i+1], roster_data["roster"][i]
                updated = True

        st.write("---")  # Add a horizontal line for separation

    # Save changes if any updates were made
    if updated:
        save_roster(roster_data)
        st.rerun()

    # Display final roster with positions and alternates
    st.markdown("## Batting Order with Positions and Alternates")
    for i, player in enumerate(roster_data["roster"]):
        position = roster_data["positions"][player]
        alternate = roster_data["alternates"][player]
        if alternate:
            st.markdown(f"### {i+1}. {player}")
            st.write(f"Position: {position} | Alternate: {alternate}")
        else:
            st.markdown(f"### {i+1}. {player}")
            st.write(f"Position: {position}")
        st.write("---")  # Add a horizontal line for separation

if __name__ == "__main__":
    main()
