from django.test import TestCase
from tttserver import game
from tttserver import models


class GameSetupTestCase(TestCase):
    fixtures = ['test_fixture']

    def test_new_players_are_created(self):
        """
        GIVEN player name NEW_PLAYER do not yet exists in the database
        WHEN game is created using player name NEW_PLAYER
        THEN NEW_PLAYER is created in the database
        """
        player_name = 'NEW_PLAYER'
        player_q = models.Player.objects.filter(name=player_name)
        self.assertFalse(player_q.exists())

        game.get_game(player_name)

        self.assertTrue(player_q.exists())
        
    def test_new_players_are_given_zero_score(self):
        """
        GIVEN NEW_PLAYER does not exist
        WHEN NEW_PLAYER is created
        THEN NEW_PLAYER shall have a score of 0
        """
        player_name = 'NEW_PLAYER'
        score_q = models.PlayerScore.objects.filter(player__name=player_name)
        self.assertFalse(score_q.exists())

        game.get_game(player_name)

        self.assertTrue(score_q.exists())
        score = score_q[0]
        self.assertEqual(score.score, 0)
        self.assertEqual(score.player.name, player_name)

    def test_players_with_game_in_progress_retrieves_their_game(self):
        """
        GIVEN player prog_1 has a game in progress
        WHEN a game is created for prog_1
        THEN the game in progress is retrieved
        """
        player_name = 'prog_1'
        game_obj = game.get_game(player_name)

        # assert board is not all blank
        self.assertTrue(models.GameState.X in game_obj.get_board())

