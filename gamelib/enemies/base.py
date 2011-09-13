import pyglet
import random

from gamelib import obj
from gamelib import data
from gamelib import bullet
from gamelib import fx

class BaseEnemy(obj.GameObject):
    
    speed = 1.0
    speed_diag = speed * 0.7071
    width = 32
    height = 64
    points = 100
    life = 1
    
    def __init__(self, sprite, x=None, y=None, vx=None, vy=None):
        super(BaseEnemy, self).__init__(sprite, x, y)
        self.alive = True        
        self.life = self.__class__.life
                
    def update(self):
        if not self.alive: return
        self.pos += self.vel
        self.sprite.xy = self.pos.x, self.pos.y
        
    def ai(self, scene):
        if not self.alive: return
        return
        
    def hit(self, other):
        self.life -= 1
        if self.life <= 0:
            self.die()
        else:
            # self.flash(0.125, (1.0,0.7,0.7,1.0))
            pass
        
    def die(self):
        # fx.exploder.explode(self.pos.x, self.pos.y)
        self.alive = False