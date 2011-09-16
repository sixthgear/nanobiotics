
from gamelib import bullet
from weapon import Weapon

class BasicTurret(Weapon):
    def __init__(self, *args):
        Weapon.__init__(self,*args)
        self.cooldown = 7

    def update(self, *args):
        Weapon.update(self, *args)

        if self.cooldown > 0:
            self.cooldown -= 1
            return

        self.cooldown = 7

        if self.engaged:
            bv = (self.target_pos - self.pos).normal * 1000
            bp = self.pos
            if bv.x != 0 or bv.y != 0:
                bullet.pool.fire(bp.x, bp.y, bv.x, bv.y) 
