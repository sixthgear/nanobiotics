import random
import math
import pyglet
import vector
import data
import collision

from gamelib import fx
from gamelib.enemies import base
from gamelib.enemies import virus

class BaseWorld(object):
    
    background = pyglet.resource.image('stage_1_background.png')
    width = 1600
    height = 1600
    name = "Void"
        
    def __init__(self, game):        
        self.game = game
        self.countdown = 120

        self.center = vector.Vec2d(self.width/2, self.height/2)
        self.radius = 600
                        
        self.build_up = True
        self.max_build_up = 15
        self.pickup_rate = 30
        self.pickup_accumulator = 0
        
        self.effects = []
        
    def valid_location(self):
        abstract
        
    def update(self, dt):
        for e in self.effects:
            e.update(dt)
            
    def draw(self):
        self.background.blit(0,0)
        for e in self.effects:
            e.draw()

        
    def ai(self):
        
        if not self.game.player.alive:
            return
            
        self.pickup_accumulator -= 0.5
        if self.pickup_accumulator <= 0:
            self.pickup_accumulator = self.pickup_rate
            x, y = self.valid_location()
            self.game.spawn_pickup(x, y, 1)        
            
        num = len(filter(lambda r: r.alive, self.game.robots))
        
        if num >= self.max_build_up: 
            self.build_up = False
            return
            
        if not self.build_up and num < 2: 
            self.game.next_world()
            self.build_up = True
        
        # self.current_wave = wave.Wave.generate(self.wave, self.diffculty)
        if self.build_up and random.random() < 0.2:        
            for i in range(random.choice([3,3,3,3,3,3,3,3,3,3,3,3,5,5,5,5,5,5,5,10,10,10,30])):                
                x, y = self.valid_location()
                v = random.choice((
                    virus.GreenVirus, 
                    virus.BlueVirus, 
                    virus.PurpleVirus, 
                    virus.SixthVirus, 
                    virus.CheezeVirus,
                    virus.WormVirus,
                    virus.RedVirus
                ))
                self.game.spawn_robot(v, 1, x, y)
        
        
    

class Stomach(BaseWorld):
    """
    ACID BURN
    """

    background = pyglet.resource.image('stage_1_background.png')
    width = 1600
    height = 1600
    name = 'Stomach'
    
    def __init__(self, game):
        super(Stomach, self).__init__(game)
        self.effects.append(fx.bubbles.Bubbler())
        # pyglet.clock.schedule_once(lambda dt: game.next_wave(), 0.0)
        
    def valid_location(self):
        
        while True:
            angle = random.random() * math.pi * 2
            mag = random.randrange(0, self.radius - 60)
            x = self.center.x + math.cos(angle) * mag
            y = self.center.y + math.sin(angle) * mag
        
            if collision.circle_to_circle(vector.Vec2d(x,y),1, self.game.player.pos, 320):
                continue
            
            return x, y
            
class Heart(BaseWorld):
    """
    ACID BURN
    """

    background = pyglet.resource.image('stage_2_background.png')
    width = 1600
    height = 1600
    name = 'Heart'
        
    def __init__(self, game):
        super(Heart, self).__init__(game)
        # fx.effects.insert(0, fx.bubbles.Bubbler())            
        # pyglet.clock.schedule_once(lambda dt: game.next_wave(), 0.0)
        
    def valid_location(self):
        
        while True:
            angle = random.random() * math.pi * 2
            mag = random.randrange(0, self.radius - 60)
            x = self.center.x + math.cos(angle) * mag
            y = self.center.y + math.sin(angle) * mag
        
            if collision.circle_to_circle(vector.Vec2d(x,y),1, self.game.player.pos, 320):
                continue
            
            return x, y
            
class Brain(BaseWorld):
    """
    BRAAAAIIIIIN
    """

    background = pyglet.resource.image('stage_2_background.png')
    width = 1600
    height = 1600
    name = 'Brain'
    
    def __init__(self, game):
        super(Brain, self).__init__(game)
        # fx.effects.insert(0, fx.bubbles.Bubbler())            
        # pyglet.clock.schedule_once(lambda dt: game.next_wave(), 0.0)
        
    def valid_location(self):
        
        while True:
            angle = random.random() * math.pi * 2
            mag = random.randrange(0, self.radius - 60)
            x = self.center.x + math.cos(angle) * mag
            y = self.center.y + math.sin(angle) * mag
        
            if collision.circle_to_circle(vector.Vec2d(x,y),1, self.game.player.pos, 320):
                continue
            
            return x, y
            
