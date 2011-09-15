import pyglet
import random

from gamelib import data
from gamelib import fx
from gamelib.enemies import base

class Virus(base.BaseEnemy):
    
    sprite_image = data.spritesheet[5]
    frames = [data.spritesheet[5], data.spritesheet[13]]
    color = color=(162.0/255,142.0/255,249.0/255)
    speed = 100.0
    speed_diag = speed * 0.7071
    
    def __init__(self, x=None, y=None, vx=None, vy=None):
        super(Virus, self).__init__(x, y, vx, vy)
        self.current_frame = 0
        
    def ai(self, scene):
        if not self.alive: return
        self.current_frame = (self.current_frame + 1) % len(self.frames)
        self.sprite.texture = self.frames[self.current_frame]

        if self.target and self.target.alive:
            self.vel = (self.target.pos - self.pos).normal * self.speed        
        else:
            # player dead, do something cool, like dance!
            pass
            
    def die(self):
        fx.gibber.explode(self.pos.x, self.pos.y, color=self.color)
        self.alive = False
        
        
class Virus_A(Virus):
    
    sprite_image = data.spritesheet[3]
    frames = [data.spritesheet[3], data.spritesheet[11]]
    color = color=(35.0/255,35.0/255,224.0/255)
    speed = 100.0
    speed_diag = speed * 0.7071
    
class Virus_B(Virus):
    
    sprite_image = data.spritesheet[5]
    frames = [data.spritesheet[5], data.spritesheet[13]]
    color = color=(162.0/255,142.0/255,249.0/255)
    speed = 100.0
    speed_diag = speed * 0.7071
    
    
