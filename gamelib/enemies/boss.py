from __future__ import division

import pyglet
import base
import math

from gamelib import data
from gamelib import fx
from gamelib import bullet

class Boss(base.BaseEnemy, pyglet.event.EventDispatcher):
    spritesheet = data.bosses["stomach"]
    sprite_image = spritesheet[0]
    animation = [0,1]
    color = (116,193,109)
    life = 100
    width = 512
    height = 512
    boss = True
    death_sound = pyglet.resource.media('pop.wav', streaming=False)

    def __init__(self, x=None, y=None, vx=None, vy=None):
        super(Boss, self).__init__(x, y, vx, vy)
        self.death_sound = self.__class__.death_sound
        self.animation = self.__class__.animation
        self.sprite.texture = self.__class__.sprite_image
        self.current_frame = 0
        self.bomb = 200

    def ai(self, scene):
        if not self.alive: return
        self.current_frame = (self.current_frame + 1) % len(self.animation)
        self.sprite.texture = self.spritesheet[self.current_frame]

    def update(self, dt):
        if not self.alive: return
        if self.cooldown > 0:
            self.cooldown -= 1

        if self.bomb > 0:
            self.bomb -= 1

        if self.bomb == 0:
            b = 90
            for a in range(0, 360, 360//10): 
                bullet.pool.fire(self.x, self.y, math.cos(math.radians(a)) * b, math.sin(math.radians(a)) * b, 1)
            self.bomb = 200

        super(Boss, self).update(dt)

    def die(self):
        self.death_sound.play()
        fx.gibber.explode(self.pos.x, self.pos.y, n=2000, size=3.0, color=[c/255 for c in self.color])
        self.snap_out()
        self.alive = False
        self.dispatch_event('on_boss_death')

class StomachBoss(Boss):
    spritesheet = data.bosses["stomach"]
    sprite_image = spritesheet[0]
    animation = [0,1,2,3]
    color = (0, 160, 0)
    cooldown = 30
    width = 400
    height = 400

    def __init__(self, x=None, y=None, vx=None, vy=None):
        super(StomachBoss, self).__init__(800, 470, vx, vy)
        
    def ai(self, scene):
        super(StomachBoss, self).ai(scene)

    def update(self, dt):
        if not self.alive: return 
        super(StomachBoss, self).update(dt)
         
        if self.target and self.cooldown == 0:
            self.shoot(self.target.pos)


class HeartBoss(Boss):
    spritesheet = data.bosses["heart"]
    sprite_image = spritesheet[0]
    animation = [0,1,2,3]
    color = (0, 160, 0)
    cooldown = 30
    width = 400
    height = 400

    def __init__(self, x=None, y=None, vx=None, vy=None):
        super(HeartBoss, self).__init__(800, 800, vx, vy)
        
    def ai(self, scene):
        super(HeartBoss, self).ai(scene)

    def update(self, dt):
        super(HeartBoss, self).update(dt)
     
        if self.target and self.cooldown == 0:
            self.shoot(self.target.pos)

class BrainBoss(Boss):
    spritesheet = data.bosses["brain"]
    sprite_image = spritesheet[0]
    animation = [0]
    color = (0, 160, 0)
    cooldown = 30
    width = 400
    height = 400

    def __init__(self, x=None, y=None, vx=None, vy=None):
        super(BrainBoss, self).__init__(800, 800, vx, vy)
        
    def ai(self, scene):
        super(BrainBoss, self).ai(scene)

    def update(self, dt):
        super(BrainBoss, self).update(dt)
        if self.target and self.cooldown == 0:
            self.shoot(self.target.pos)


Boss.register_event_type('on_boss_death')
