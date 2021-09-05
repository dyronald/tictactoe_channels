from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json
from . import game

class Player(WebsocketConsumer):
    """
    Handles connection to the client UI.
    Transforms game logic data so it's consumable by the client and vice versa.
    Sends messages to the client as the game progresses.
    """
    def connect(self):
        self.player_name = self.scope['url_route']['kwargs']['player_name']
        if self.player_name == '':
            self.close()
            return

        # kwargs are valid if execution reaches here

        self.game = game.get_game(self.player_name)

        async_to_sync(self.channel_layer.group_add)(
            self.game.group_name,
            self.channel_name
        )

        self.accept()

        players = self.game.get_players()
        if len(players) == 1:
            message = players[0] + ' created new game.'
        else:
            message = players[1] + ' joined ' + players[0]

        async_to_sync(self.channel_layer.group_send)(
            self.game.group_name,
            {
                'type': 'game_message',
                'message': message,
                'board': self.game.get_board()
            }
        )

    def disconnect(self, close_code):
        print('disconnected!!!')

    def receive(self, text_data):
        data_parsed = json.loads(text_data)
        self.game.move(self.player_name, data_parsed['move'])
        board = self.game.get_board()

        payload = {}
        payload['type'] = 'game_message'
        payload['board'] = board
        if self.game.get_winner() != '':
            payload['winner'] = self.game.get_winner()

        async_to_sync(self.channel_layer.group_send)(
            self.game.group_name,
            payload
        )

    def game_message(self, event):
        payload = event.copy()
        del payload['type']
        self.send(text_data=json.dumps(payload))