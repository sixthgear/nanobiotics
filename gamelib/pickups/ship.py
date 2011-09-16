import base
from gamelib import obj

class Ship(base.Pickup):
    sprite = data.spritesheet[40]

    def activate(self, player):
        player.lives += 1
        self.alive = False

