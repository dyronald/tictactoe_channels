Running the app:
- Create virtualenv
- Install pip packages listed in requirements.txt
- MySQL host running on localhost. See settings.py for the full settings.
- Redis host running localhost. See settings.py for the full settings.
- Execute python ./manage.py migrate if starting from an empty database.
- Execute python ./manage.py runserver to start; Debug mode was left enabled.

To play the game:
http://localhost:8000/play/[player_name]

To show high scores:
http://localhost:8000/hiscore/

Characteristics:
- Player name is specified in the address bar
- Only 1 game can be in progress per player
- Though multiple games can simultaneously be in progress spread among different players
- Players automatically join a waiting game if one is found; or otherwise creates a new game
- Opponent's display is automatically refreshed using websocket events
- Uses database for game state persistence
- Player cell (game move) input is error checked
- Game rejects illegal moves; out-of-turn, occupied cell, etc.

Limitations:
- Only basic testing done (game logic) due to time constraints
- Player name input not fully sanitized
- No mitigation against faulty or flaky network connection

Tech stack:
- Django
- Channels for websockets
- MySQL for database
- HTML and JS for frontend