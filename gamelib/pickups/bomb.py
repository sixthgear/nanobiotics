import base
from gamelib import obj

class Bomb(base.Pickup):
    sprite = data.spritesheet[40]

    def activate(self, player):
        player.bombs += 1
        self.alive = False

