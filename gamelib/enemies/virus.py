import pyglet
import random

from gamelib import data
from gamelib import fx
from gamelib.enemies import base

class Virus(base.BaseEnemy):
    
    sprite_image = data.spritesheet[5]
    frames = [data.spritesheet[5], data.spritesheet[13]]
    color = (162.0/255,142.0/255,249.0/255)
    speed = 100.0
    speed_diag = speed * 0.7071
    
    def __init__(self, x=None, y=None, vx=None, vy=None):
        super(Virus, self).__init__(x, y, vx, vy)
        self.current_frame = 0
        self.current_animation = self.animation_small
        
    def ai(self, scene):
        if not self.alive: return
        self.current_frame = (self.current_frame + 1) % len(self.current_animation)
        self.sprite.texture = self.spritesheet[self.current_animation[self.current_frame]]

        if self.target and self.target.alive:
            self.vel = (self.target.pos - self.pos).normal * self.speed        
        else:
            # player dead, do something cool, like dance!
            pass
            
    def die(self):
        fx.gibber.explode(self.pos.x, self.pos.y, color=self.color)
        self.alive = False
        
        
class PurpleVirus(Virus):
    
    spritesheet = data.load_virus('purple')
    sprite_image = spritesheet[3]
    animation_small = [3,2]
    color = (162.0/255,142.0/255,249.0/255)
    speed = 100.0
    speed_diag = speed * 0.7071
    
class BlueVirus(Virus):    
    spritesheet = data.load_virus('blue')
    sprite_image = spritesheet[3]    
    animation_small = [3,2]
    color = (35.0/255,35.0/255,224.0/255)
    speed = 100.0
    speed_diag = speed * 0.7071
    
class GreenVirus(Virus):
    spritesheet = data.load_virus('green')
    sprite_image = spritesheet[3]
    animation_small = [3,2]
    color = (116.0/255,193.0/255,109.0/255)
    speed = 175.0
    speed_diag = speed * 0.7071
    
class SixthVirus(Virus):
    spritesheet = data.load_virus('sixth')
    sprite_image = spritesheet[3]
    animation_small = [3,2]
    color = (131.0/255,131.0/255,131.0/255)
    speed = 175.0
    speed_diag = speed * 0.7071
    
    def update(self, dt):
        super(SixthVirus, self).update(dt)
        self.sprite.rot = (self.sprite.rot + 5) % 360
        
class CheezeVirus(Virus):
    spritesheet = data.load_virus('cheeze')
    sprite_image = spritesheet[3]
    animation_small = [3,2]
    color = (237.0/255,238.0/255,74.0/255)
    speed = 175.0
    speed_diag = speed * 0.7071
        
class WormVirus(Virus):
    spritesheet = data.load_virus('worm')
    sprite_image = spritesheet[3]
    animation_small = [3,2,1,2]
    color = (104.0/255,217.0/255,198.0/255)
    speed = 175.0
    speed_diag = speed * 0.7071
        