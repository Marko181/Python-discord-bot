# Python bot for Discord server

## Idea:
- send menu from cantine every workday at 10:00
- send menu upon prompt 'menza'
- send menu for any restaurant that offers student meals upon prompt 'hrana [restaurant name]'
- send fun food fact upon prompt 'hrana fact'
- send fun food pun upon prompt 'hrana pun'

## Installation:
1. Clone this git repository
2. Install required Python libraries by running:
   ```bash
   pip install -r requirements.txt
4. Change the *YOUR_CHANNEL_ID* in [main.py](main.py) to your channel ID
5. Add a .txt file with your bot key in this folder
6. Enable necessary settings in your Discord server
7. Run [main.py](main.py)

## Script functions:

- **`main.py`**: Runs the Discord bot, handles events, and communicates with users.
- **`hrana.py`**: Fetches restaurant menus and provides food-related puns and facts.
- **`menza.py`**: Scrapes and formats the university cafeteria menu.
- **`whois.py`**: Placeholder for future user information features.

