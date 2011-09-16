import random
import math
import pyglet
import vector
import data

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
        
        # pyglet.clock.schedule_once(lambda dt: game.next_wave(), 0.0)
        
    def valid_location(self, v):
        valid = False
        return valid

    def ai(self, game):

        num = len(filter(lambda r: r.alive, self.game.robots))
        
        if num > 20: return
        
        # self.current_wave = wave.Wave.generate(self.wave, self.diffculty)
        if random.random() < 0.3:        
            for i in range(random.choice([1,1,1,1,1,1,1,5,5,5,10])):
                angle = random.random() * math.pi * 2
                mag = random.randrange(game.world.radius-160, game.world.radius - 60)
                x = game.world.center.x + math.cos(angle)*mag
                y = game.world.center.y + math.sin(angle)*mag
                game.spawn_robot(random.choice((
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


