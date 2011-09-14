
from gamelib import bullet
from weapon import Weapon

class BasicTurret(Weapon):
    def __init__(self, *args):
        Weapon.__init__(self,*args)
        self.cooldown = 0

    def update(self, *args):
        Weapon.update(self, *args)

        if self.cooldown > 0:
            self.cooldown -= 1
            return

        self.cooldown = 0

        if self.engaged:
            bv = (self.target_pos - self.pos).normal * 1800
            bp = self.pos
            if bv.x != 0 or bv.y != 0:
                bullet.pool.fire(bp.x, bp.y, bv.x, bv.y) 
