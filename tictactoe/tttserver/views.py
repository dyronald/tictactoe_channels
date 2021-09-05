from django.shortcuts import render
from django.utils.safestring import mark_safe
from . import models
import json

def index(request, player_name):
    return render(request, 'tttserver/index.html', {
        'player_name': mark_safe(json.dumps(player_name))
    })

def hiscore(request):
    return render(request, 'tttserver/hiscore.html', {
        'player_scores': models.PlayerScore.objects.order_by('-score').all()
    })