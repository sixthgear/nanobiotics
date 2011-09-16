import base
from gamelib import obj
from gamelib import data

class Bomb(base.Pickup):
    sprite = data.spritesheet[8]

    def activate(self, game, player):        
        player.bombs += 1
        self.alive = False
        self.__class__.sound.play()

