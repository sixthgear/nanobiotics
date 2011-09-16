import pyglet
import random

from gamelib import data
from gamelib import obj


class Pickup(obj.GameObject):
    
    life = 20
    sprite = data.spritesheet[40]
    # sound = pyglet.resource.media('powerup.wav', streaming=False)
    
    def __init__(self, x=None, y=None, type=None):
        if x == None or y == None:
            x = random.randrange(768) + 32
            y = random.randrange(540) + 50            
        if type == None:
            type = random.randrange(4)
            
        x = min(max(32, x), 768)
        y = min(max(50, y), 540)
        
        self.life = self.__class__.life    
        self.type = type    
        super(Pickup,self).__init__(self.__class__.sprite, x, y)
        self.alive = True
    
    def ai(self, scene):
        self.life -= 1
        if self.life == 6: self.flash(3.0)
        if self.life <= 0: self.die()
        
    def activate(self, player):
        #self.__class__.sound.play()
        pass
        
    def die(self):
        self.alive = False
