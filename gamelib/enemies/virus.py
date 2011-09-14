import random

from gamelib import data
from gamelib.enemies import base

class Virus(base.BaseEnemy):
    sprite_image = data.spritesheet[random.range(5)*8 + random.randrange(6)]
    
    def ai(self, scene):
        if not self.alive: return

        if self.target and self.target.alive:
            self.vel = (self.target - self.pos).normal * self.speed

        else:
            # player dead, do something cool, like dance!
            pass
