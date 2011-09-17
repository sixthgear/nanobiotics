import base
from gamelib import obj
from gamelib import data

class Ship(base.Pickup):
    sprite = data.spritesheet[12]

    def activate(self, game, player):
        player.lives += 1
        self.alive = False

