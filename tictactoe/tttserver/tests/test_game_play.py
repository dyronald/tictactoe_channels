from django.test import TestCase
from tttserver import game


class GamePlayTestCase(TestCase):
    fixtures = ['test_fixture']

    def test_player_1_win(self):
        """
        GIVEN a player Winner1 is playing as first player
        WHEN Winner1 marks cells 1,2,3
        THEN Winner1 wins
        """
        p1 = 'Winner1'
        p2 = 'Player2'
        p1_game = game.get_game(p1)
        p2_game = game.get_game(p2)

        p1_game.move(p1, '1')
        p2_game.move(p2, '4')
        
        p1_game.move(p1, '2')
        p2_game.move(p2, '5')

        p1_game.move(p1, '3')

        self.assertEqual(p1_game.get_winner(), p1)
    
    def test_player_2_win(self):
        """
        GIVEN a player Winner2 is playing as second player
        WHEN Winner2 marks cells 3,6,9
        THEN Winner2 wins
        """
        p1 = 'Player1'
        p2 = 'Winner2'
        p1_game = game.get_game(p1)
        p2_game = game.get_game(p2)

        p1_game.move(p1, '1')
        p2_game.move(p2, '3')
        
        p1_game.move(p1, '2')
        p2_game.move(p2, '6')

        p1_game.move(p1, '5')
        p2_game.move(p2, '9')

        self.assertEqual(p2_game.get_winner(), p2)

    def test_draw(self):
        """
        GIVEN all cells are occupied
            AND neither player formed 3 in a row
        THEN game is a draw
        """
        p1 = 'Draw1'
        p2 = 'Draw2'
        p1_game = game.get_game(p1)
        p2_game = game.get_game(p2)

        p1_game.move(p1, '1')
        p2_game.move(p2, '2')
        
        p1_game.move(p1, '4')
        p2_game.move(p2, '6')

        p1_game.move(p1, '5')
        p2_game.move(p2, '7')

        p1_game.move(p1, '8')
        p2_game.move(p2, '9')

        p1_game.move(p1, '3')

        self.assertEqual(p1_game.get_winner(), 'DRAW')