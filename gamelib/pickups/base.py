import pyglet
import random

from gamelib import data
from gamelib import obj
#import weapon

sprites_idx = [15,23,22,14,31,30]
SPREAD, MACHINE, SUPERMACHINE, SUPERSPREAD, RAGE, ONEUP = range(6)

class Pickup(obj.GameObject):
    
    life = 20
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
        super(Pickup,self).__init__(data.spritesheet[40], x, y)
        self.alive = True
    
    def ai(self, scene):
        self.life -= 1
        if self.life == 6: self.flash(3.0)
        if self.life <= 0: self.die()
        
    def activate(self, scene):
        """
        self.__class__.sound.play()
        if self.type == SPREAD:
            scene.player.set_weapon(weapon.Spread)
        elif self.type == MACHINE:
            scene.player.set_weapon(weapon.Machine)
        elif self.type == SUPERMACHINE:
            scene.player.set_weapon(weapon.Machine, 3, 5.0)
        elif self.type == SUPERSPREAD:
            scene.player.set_weapon(weapon.Spread, 3, 2.5)            
        elif self.type == RAGE:
            scene.rage.multiply(1)
        elif self.type == ONEUP:
            scene.player.lives += 1
            scene.lives_label.text = "%d" % scene.player.lives
        """
        
    def die(self):
        self.alive = False
