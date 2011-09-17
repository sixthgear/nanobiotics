import pyglet
import random

from gamelib import data
from gamelib import obj


class Pickup(obj.GameObject):
    
    life = 20
    sprite = data.spritesheet[40]
    sound = pyglet.resource.media('powerup.wav', streaming=False)
    
    def __init__(self, x, y, type=None):
            
        # x = min(max(32, x), 768)
        # y = min(max(50, y), 540)
        
        self.life = self.__class__.life    
        self.type = type    
        super(Pickup,self).__init__(self.__class__.sprite, x, y)
        self.alive = True
    
    def ai(self, scene):
        self.life -= 1
        if self.life == 6: self.flash(3.0)
        if self.life <= 0: self.die()
        
    def activate(self, game, player):
        self.__class__.sound.play()
            
    def die(self):
        self.alive = False


class MachineGunPickup(Pickup):    
    sprite = data.spritesheet[9]
    def activate(self, game, player):        
        player.swap_weapon(1)
        self.alive = False
        self.__class__.sound.play()
    
class SpreadGunPickup(Pickup):    
    sprite = data.spritesheet[10]
    def activate(self, game, player):        
        player.swap_weapon(2)
        self.alive = False
        self.__class__.sound.play()

class FireHosePickup(Pickup):    
    sprite = data.spritesheet[11]
    def activate(self, game, player):        
        player.swap_weapon(3)
        self.alive = False
        self.__class__.sound.play()
    
    
    