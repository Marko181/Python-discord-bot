# Python bot for Discord server


 /$$$$$$$$        /$$$$$$$              /$$    
| $$_____/       | $$__  $$            | $$    
| $$     /$$$$$$ | $$  \ $$  /$$$$$$  /$$$$$$  
| $$$$$ /$$__  $$| $$$$$$$  /$$__  $$|_  $$_/  
| $$__/| $$$$$$$$| $$__  $$| $$  \ $$  | $$    
| $$   | $$_____/| $$  \ $$| $$  | $$  | $$ /$$
| $$   |  $$$$$$$| $$$$$$$/|  $$$$$$/  |  $$$$/
|__/    \_______/|_______/  \______/    \___/  
                                               
                                               
                                               
## Bot auto update:
- clone this git
- add files like images in folder [files](files/)
- add or edit code files
- commit and push changes back to this git
- change the version in [main.py](main.py)
- run in discord server command "BotUpdateNow"

## Idea:
- send menu from cantine every workday at 10:00
- send menu upon prompt 'menza'
- send menu for any restaurant that offers student meals upon prompt 'hrana [restaurant name]'
- send fun food fact upon prompt 'hrana fact'
- send fun food pun upon prompt 'hrana pun'
- send random local meme
- send specific local meme
- send local meme list

## Installation:
1. Clone this git repository
2. Install required Python libraries by running:
   ```bash
   pip install -r requirements.txt
4. Add a .txt files with your channel ID, bot key and user IDs
6. Enable necessary settings in your Discord server
7. Run [main.py](main.py)

## Script functions:
- **`main.py`**: Runs the Discord bot, handles events, and communicates with users.
- **`hrana.py`**: Fetches restaurant menus and provides food-related puns and facts.
- **`menza.py`**: Scrapes and formats the university cafeteria menu.
- **`whois.py`**: Placeholder for future user information features.

