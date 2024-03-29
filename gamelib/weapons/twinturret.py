import pyglet
import random

from gamelib import bullet
from weapon import Weapon

class TwinTurret(Weapon):
    
    fire_sound = pyglet.resource.media('fire.wav', streaming=False)

    def __init__(self, *args):
        Weapon.__init__(self,*args)
        self.cooldown = 1

    def update(self, *args):
        Weapon.update(self, *args)

        # if self.cooldown > 0:
        #     self.cooldown -= 1
        #     return

        self.cooldown = 1

        if self.engaged:
            bv = (self.target_pos - self.pos).normal * 2000
            bp = self.pos
            if bv.x != 0 or bv.y != 0:
                self.fire_sound.play()
                # jitter
                bv.x += random.randrange(-100,100)
                bv.y += random.randrange(-100,100)    
                bullet.pool.fire(bp.x, bp.y, bv.x, bv.y) 

                

class FireHose(Weapon):
    
    fire_sound = pyglet.resource.media('fire.wav', streaming=False)

    def __init__(self, *args):
        Weapon.__init__(self,*args)
        self.cooldown = 0

    def update(self, *args):
        Weapon.update(self, *args)

        # if self.cooldown > 0:
        #     self.cooldown -= 1
        #     return

        self.cooldown = 0

        if self.engaged:
            bv = (self.target_pos - self.pos).normal * 2000
            bp = self.pos
            if bv.x != 0 or bv.y != 0:
                
                self.fire_sound.play()
                for i in range(4):
                    # jitter
                    bv.x += random.randrange(-100,100)
                    bv.y += random.randrange(-100,100)                
                    bullet.pool.fire(bp.x, bp.y, bv.x, bv.y) 
