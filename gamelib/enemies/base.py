import pyglet
import rabbyt
import random

from gamelib import obj
from gamelib import data
from gamelib import bullet
from gamelib import fx
from gamelib import vector

class BaseEnemy(obj.GameObject):
    
    speed = 1.0
    speed_diag = speed * 0.7071
    width = 64
    height = 64
    points = 100
    life = 1
    cooldown = 100
    bullet_velocity = 250
    boss = False

    
    def __init__(self, x=None, y=None, vx=None, vy=None):
        super(BaseEnemy, self).__init__(self.sprite_image, x, y)
        self.alive = True
        self.is_boss = self.__class__.boss     
        self.life = self.__class__.life
        self.bullet_velocity = self.__class__.bullet_velocity
        self.cooldown = 0
        self.target = None

    def set_target(self, target):
        self.target = target
                
    def update(self, dt):
        if not self.alive: return

        # if self.cooldown > 0:
        #     self.cooldown -= 1
        # 
        # if self.cooldown == 0:
        #     self.shoot(self.target.pos)

        self.pos += self.vel * dt
        self.sprite.xy = self.pos.x, self.pos.y
        self.x, self.y = self.pos.x, self.pos.y
        
        
    def snap_in(self, start=0.01):
        self.sprite.scale_x = rabbyt.anims.chain(
            rabbyt.anims.ease_in(start, 2.5, dt=0.15),
            rabbyt.anims.ease_out(2.5, 1.0, dt=0.2)
        )
        self.sprite.scale_y = rabbyt.anims.chain(
            rabbyt.anims.ease_out(start, 1.5, dt=0.15),
            rabbyt.anims.ease_in(1.5, 1.0, dt=0.2)
        )
        
    def snap_out(self, start=0.01):
        self.sprite.scale_x = rabbyt.anims.chain(
            rabbyt.anims.ease_in(1.0, 2.5, dt=0.2),
            rabbyt.anims.ease_out(2.5, start, dt=0.15),            
        )
        self.sprite.scale_y = rabbyt.anims.chain(
            rabbyt.anims.ease_out(1.0, 1.5, dt=0.2),
            rabbyt.anims.ease_in(1.5, start, dt=0.15),

        )     
                        
    def ai(self, scene):
        if not self.alive: return
        return
        
    def hit(self, other):
        self.life -= 1
        if self.life <= 0:
            self.die()
        else:
            self.flash(0.125, (1.0,0.7,0.7,1.0))
        
    def die(self):
        fx.gibber.explode(self.pos.x, self.pos.y)
        self.alive = False

    def shoot(self, xy):
        self.cooldown = self.__class__.cooldown
        bp = self.pos
        bv = (xy - bp).normal * self.bullet_velocity
        
        if bv.x != 0 or bv.y != 0:
            bullet.pool.fire(bp.x, bp.y, bv.x, bv.y, 1)
         
