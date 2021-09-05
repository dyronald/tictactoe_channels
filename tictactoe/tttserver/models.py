from django.db import models

class Player(models.Model):
    name = models.CharField(max_length=50, unique=True)

class PlayerScore(models.Model):
    player = models.ForeignKey('Player', on_delete=models.PROTECT)
    score = models.IntegerField(default=0)

class GameState(models.Model):
    BLANK = 'b'
    X = 'x'
    O = 'o'
    DRAW = 'DRAW'
    IN_PROGRESS = 'IN_PROGRESS'
    WON = 'WON'

    player_x = models.ForeignKey('Player', related_name='player_x_fk', null=True, on_delete=models.PROTECT)
    player_o = models.ForeignKey('Player', related_name='player_o_fk', null=True, on_delete=models.PROTECT)
    turn = models.ForeignKey('Player', related_name='turn_fk', null=True, on_delete=models.PROTECT)
    winner = models.ForeignKey('Player', related_name='winner_fk', null=True, on_delete=models.PROTECT)
    progress = models.CharField(max_length=20, default=IN_PROGRESS) 

    cell_1 = models.CharField(max_length=1, default=BLANK)
    cell_2 = models.CharField(max_length=1, default=BLANK)
    cell_3 = models.CharField(max_length=1, default=BLANK)
    cell_4 = models.CharField(max_length=1, default=BLANK)
    cell_5 = models.CharField(max_length=1, default=BLANK)
    cell_6 = models.CharField(max_length=1, default=BLANK)
    cell_7 = models.CharField(max_length=1, default=BLANK)
    cell_8 = models.CharField(max_length=1, default=BLANK)
    cell_9 = models.CharField(max_length=1, default=BLANK)
