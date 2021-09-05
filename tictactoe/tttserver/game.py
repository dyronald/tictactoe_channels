from . import models

class Game():
    """
    Drives the game logic.
    This class is intended to hide database from the player classes.
    """

    def __init__(self, state):
        self.state = state
        self.group_name = 'game' + str(self.state.id)
        self._read_board()

    def move(self, player_name, cell):
        """
        Make a game move
        
        Args:
            player_name: name of player
            cell: cell number that the player wishes to mark; the variable 
                valid_cells below illustrates the positions
        """
        valid_cells = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        if cell not in valid_cells:
            return 

        player = models.Player.objects.get(name=player_name) 
        self.state.refresh_from_db()
        if models.GameState.IN_PROGRESS != self.state.progress or \
            self.state.player_x == None or \
            self.state.player_o == None: 
            return

        if player != self.state.turn:
            return

        cell_attr = 'cell_' + str(cell)
        if getattr(self.state, cell_attr) != models.GameState.BLANK:
            return

        # move is valid if execution reaches here

        if self.state.turn == self.state.player_x:
            symbol = models.GameState.X
            self.state.turn = self.state.player_o
        else:
            symbol = models.GameState.O
            self.state.turn = self.state.player_x

        setattr(self.state, cell_attr, symbol)
        self._read_board()
        self._assess_result()

        self.state.save()
        return 

    def get_players(self):
        players = []
        
        if self.state.player_x != None:
            players.append(self.state.player_x.name)
            
        if self.state.player_o != None:
            players.append(self.state.player_o.name)

        return players

    def get_board(self):
        return self.board

    def get_winner(self):
        """
        Get the winner of the game.

        Returns:
            String; Name of the winner.
            String has a value of "DRAW" if game was a draw.
            String is empty if game is still in progress.
        """
        if self.state.progress == models.GameState.IN_PROGRESS:
            return ''
        elif self.state.progress == models.GameState.DRAW:
            return models.GameState.DRAW

        return self.state.winner.name

    def _read_board(self):
        self.board = [getattr(self.state, 'cell_' + str(x)) for x in range(1, 10)]

    def _assess_result(self):
        if self._has_win(models.GameState.X):
            self._save_win(self.state.player_x)
        elif self._has_win(models.GameState.O):
            self._save_win(self.state.player_o)
        elif self._board_full():
            self.state.progress = models.GameState.DRAW

    def _has_win(self, symbol):
        # horizontal
        if self.board[0] == symbol and self.board[1] == symbol and self.board[2] == symbol: return True
        if self.board[3] == symbol and self.board[4] == symbol and self.board[5] == symbol: return True
        if self.board[6] == symbol and self.board[7] == symbol and self.board[8] == symbol: return True
        
        # vertical
        if self.board[0] == symbol and self.board[3] == symbol and self.board[6] == symbol: return True
        if self.board[1] == symbol and self.board[4] == symbol and self.board[7] == symbol: return True
        if self.board[2] == symbol and self.board[5] == symbol and self.board[8] == symbol: return True

        # diagonal
        if self.board[0] == symbol and self.board[4] == symbol and self.board[8] == symbol: return True
        if self.board[6] == symbol and self.board[4] == symbol and self.board[2] == symbol: return True

        return False

    def _board_full(self):
        return models.GameState.BLANK not in self.board

    def _save_win(self, player):
        self.state.winner = player
        self.state.progress = models.GameState.WON

        player_score = models.PlayerScore.objects.get(player=player)
        player_score.score += 1
        player_score.save()

def get_game(player_name):
    """
    Factory method for a Game object
    """
    player_q = models.Player.objects.filter(name=player_name)
    if not player_q.exists():
        # Auto create the player if it doesn't exist
        player = models.Player(name=player_name)
        player.save()
        player.refresh_from_db()

        player_score = models.PlayerScore(player=player)
        player_score.save()
    else:
        player = player_q[0]

    state = _get_game_state(player)
    return Game(state)


def _get_game_state(player):
    """
    Retrieves a player's unfinished game;
    Or joins a game that's missing a player if none is found;
    Or creates a new game if none is found;
    """
    state_q = models.GameState.objects.filter(player_x=player).filter(progress=models.GameState.IN_PROGRESS)
    if state_q.exists():
        return state_q[0] 

    state_q = models.GameState.objects.filter(player_o=player).filter(progress=models.GameState.IN_PROGRESS)
    if state_q.exists():
        return state_q[0]

    # See if anyone is waiting for someone to play with
    state_q = models.GameState.objects.filter(player_o=None)
    if state_q.exists():
        state = state_q[0]
        state.player_o = player
        state.save()
        return state

    # Create a new game
    state = models.GameState(player_x=player, turn=player)
    state.save()
    return state