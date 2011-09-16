import pyglet
import rabbyt
import random
import math

from gamelib import data
from gamelib import fx
from gamelib import vector
from gamelib.enemies import base

class Virus(base.BaseEnemy):
    
    spritesheet = data.load_virus('purple')
    sprite_image = spritesheet[3]
    animation_small = [3,2]
    animation_large = [5,4]
    color = (162.0/255,142.0/255,249.0/255)
    speed = 100.0
    speed_diag = speed * 0.7071
    vel_smooth = 0.04
    
    def __init__(self, x=None, y=None, vx=None, vy=None):
        super(Virus, self).__init__(x, y, vx, vy)
        self.current_frame = 0
        self.current_animation = self.animation_small
        self.form = 0
        self.speed = self.__class__.speed
        self.vel_target = vector.Vec2d(0,0)
        self.snap_in()

    
    def snap_in(self, start=0.01):
        self.sprite.scale_x = rabbyt.anims.chain(
            rabbyt.anims.ease_in(start, 2.0, dt=0.15),
            rabbyt.anims.ease_out(2.0, 1.0, dt=0.2)
        )
        self.sprite.scale_y = rabbyt.anims.chain(
            rabbyt.anims.ease_out(start, 1.5, dt=0.15),
            rabbyt.anims.ease_in(1.5, 1.0, dt=0.2)
        )
        
        
    def ai(self, scene):
        if not self.alive: return
        self.current_frame = (self.current_frame + 1) % len(self.current_animation)
        self.sprite.texture = self.spritesheet[self.current_animation[self.current_frame]]

        if self.target and self.target.alive:
            self.vel_target = (self.target.pos - self.pos).normal * self.speed            
        # else:
        #     # player dead, do something cool, like dance!
        #     pass
            
    def update(self, dt):        
        self.vel += (self.vel_target - self.vel ) * self.__class__.vel_smooth
        super(Virus, self).update(dt)
        
    def die(self):
        fx.gibber.explode(self.pos.x, self.pos.y, color=self.color)
        self.alive = False
        
        
class MutatingVirus(Virus):
    
    
    def update(self, dt):        
        self.vel += (self.vel_target - self.vel ) * self.__class__.vel_smooth
        super(MutatingVirus, self).update(dt)
    
    def hit(self, other):
        self.life -= 1
        if self.life <= 0:
            if self.form != 0 or random.random() < .5:
                self.die()
            else:
                self.form += 1
                self.life = 5
                self.speed *= 1.5
                self.current_animation = self.animation_large
                self.sprite.texture = self.spritesheet[self.current_animation[self.current_frame]]
                self.snap_in(0.67)
                
        else:
            self.flash(0.125, (1.0,0.4,0.4,1.0))
        

        
class PurpleVirus(Virus):    
    spritesheet = data.load_virus('purple')
    sprite_image = spritesheet[3]
    color = (162.0/255,142.0/255,249.0/255)
    speed = 100.0
    
class BlueVirus(MutatingVirus):    
    spritesheet = data.load_virus('blue')
    sprite_image = spritesheet[3]
    color = (35.0/255,35.0/255,224.0/255)
    speed = 100.0
    
class GreenVirus(MutatingVirus):
    spritesheet = data.load_virus('green')
    sprite_image = spritesheet[3]
    color = (116.0/255,193.0/255,109.0/255)
    speed = 175.0
    
class SixthVirus(MutatingVirus):
    spritesheet = data.load_virus('sixth')
    sprite_image = spritesheet[3]
    animation_small = [3]
    animation_large = [5]
    color = (131.0/255,131.0/255,131.0/255)
    speed = 250.0
    vel_smooth = 0.2
    
    def update(self, dt):
        super(SixthVirus, self).update(dt)
        self.sprite.rot = (self.sprite.rot + 5) % 360
        
class CheezeVirus(MutatingVirus):
    spritesheet = data.load_virus('cheeze')
    sprite_image = spritesheet[3]
    color = (237.0/255,238.0/255,74.0/255)
    speed = 30.0
    
    def ai(self, scene):
        if not self.alive: return
        self.current_frame = (self.current_frame + 1) % len(self.current_animation)
        self.sprite.texture = self.spritesheet[self.current_animation[self.current_frame]]

        target = vector.Vec2d()
        target.x += random.randrange(-10,10)
        target.y += random.randrange(-10,10)
        self.vel = (target).normal * self.speed
        
class WormVirus(Virus):
    spritesheet = data.load_virus('worm')
    sprite_image = spritesheet[3]
    animation_small = [3,2,1,2]
    color = (104.0/255,217.0/255,198.0/255)
    speed = 50.0
    
    # def update(self, dt):
    #     super(WormVirus, self).update(dt)
    #     d = self.target.pos - self.pos
    #     self.sprite.rot = -math.degrees(math.atan2(d.x,d.y)) - 45
    #     #     