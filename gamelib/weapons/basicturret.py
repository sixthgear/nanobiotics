import pyglet

from gamelib import bullet
from weapon import Weapon

class BasicTurret(Weapon):
    
    fire_sound = pyglet.resource.media('fire.wav', streaming=False)

    def __init__(self, *args):
        Weapon.__init__(self,*args)
        self.cooldown = 5

    def update(self, *args):
        Weapon.update(self, *args)

        if self.cooldown > 0:
            self.cooldown -= 1
            return

        self.cooldown = 5

        if self.engaged:
            bp = self.pos
            bv = (self.target_pos - bp).normal * 1400
            if bv.x != 0 or bv.y != 0:
                self.fire_sound.play()
                bullet.pool.fire(bp.x, bp.y, bv.x, bv.y) 
