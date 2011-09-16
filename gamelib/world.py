import random
import math
import pyglet
import vector
import data
import collision

from gamelib import fx
from gamelib.enemies import base
from gamelib.enemies import virus

class World(object):
    """
    World object contains world geometry and tells game whats up
    """

    def __init__(self, border_name, game, name="VOID"):
        self.game = game
        self.countdown = 120
        self.name = name

        self.width = 1600
        self.height = 1600
        self.center = vector.Vec2d(self.width/2, self.height/2)
        self.radius = 600
        
        self.borders = [vector.Vec2d(*v) for v in 
                            data.worlds[border_name].paths[0].path[0]]
                
        self.build_up = True
        self.max_build_up = 35
        
        fx.effects.insert(0, fx.bubbles.Bubbler())
        
        self.pickup_rate = 30
        self.pickup_accumulator = 0
            
        # pyglet.clock.schedule_once(lambda dt: game.next_wave(), 0.0)
        
    def valid_location(self):
        
        found = False
        while not found:
            angle = random.random() * math.pi * 2
            mag = random.randrange(0, self.radius - 60)
            x = self.center.x + math.cos(angle) * mag
            y = self.center.y + math.sin(angle) * mag
        
            if collision.circle_to_circle(vector.Vec2d(x,y),1, self.game.player.pos, 320):
                continue
            
            found = True
            
        return x, y

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
            self.build_up = True
        
        # self.current_wave = wave.Wave.generate(self.wave, self.diffculty)
        if self.build_up and random.random() < 0.3:        
            for i in range(random.choice([3,3,3,3,3,3,3,3,3,3,3,3,5,5,5,5,5,5,5,10,10,10,30])):
                
                x, y = self.valid_location()
                
                self.game.spawn_robot(random.choice((
                    virus.GreenVirus, 
                    virus.BlueVirus, 
                    virus.PurpleVirus, 
                    virus.SixthVirus, 
                    virus.CheezeVirus,
                    # virus.WormVirus
                    )
                ), 1, x, y)
        
    def update(self, dt):

        pass


