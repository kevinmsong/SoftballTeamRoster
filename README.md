# SoftballTeamRoster

Streamlit roster manager for the “Shady Sluggers” softball team: edit players, positions, and alternates, and view a batting-order page. Data is stored locally in `roster_data.json`.

## Features

- Roster Management page: add players with a default position, edit position and alternate, reorder (up/down), remove
- Positions: Pitcher, Catcher, First Base, Second Base, Third Base, Shortstop, Left Fielder, Center Fielder, Right Fielder
- Batting Order page: read-only list of current roster order with position and optional alternate
- Mobile-friendly layout (custom CSS); in-app version label 1.2
- Persistence via `roster_data.json` (`roster`, `positions`, `alternates`); empty starter file ships with the repo

## Requirements

See `requirements.txt`:

- streamlit

## Setup

```bash
pip install -r requirements.txt
```

No API keys required.

## Usage

```bash
streamlit run SoftballTeamRoster.py
```

Use **Roster Management** to edit the team and **Batting Order** to view the current order.

## Notes

- Changes save immediately to `roster_data.json` in the working directory.
- The checked-in `roster_data.json` starts empty (`{"roster": [], "positions": {}, "alternates": {}}`).
