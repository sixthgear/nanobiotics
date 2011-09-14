import pyglet
import random

from gamelib import obj
from gamelib import data
from gamelib import bullet
from gamelib import fx

class BaseEnemy(obj.GameObject):
    
    speed = 1.0
    speed_diag = speed * 0.7071
    width = 64
    height = 64
    points = 100
    life = 1
    target = None
    
    def __init__(self, x=None, y=None, vx=None, vy=None):
        super(BaseEnemy, self).__init__(data.spritesheet[random.randrange(5)*8 + random.randrange(6)], x, y)
        self.alive = True        
        self.life = self.__class__.life

    def set_target(self, target):
        self.target = target
                
    def update(self, dt):
        if not self.alive: return

        self.pos += self.vel * dt
        self.sprite.xy = self.pos.x, self.pos.y
        self.x, self.y = self.pos.x, self.pos.y
        
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
        fx.exploder.explode(self.pos.x, self.pos.y)
        self.alive = False
