import random

from gamelib import data
from gamelib.enemies import base

class Virus(base.BaseEnemy):
    sprite_image = data.spritesheet[random.randrange(5)*8 + random.randrange(6)]
    speed = 100.0
    speed_diag = speed * 0.7071
    
    def ai(self, scene):
        if not self.alive: return

        if self.target and self.target.alive:
            self.vel = (self.target.pos - self.pos).normal * self.speed

        else:
            # player dead, do something cool, like dance!
            pass
