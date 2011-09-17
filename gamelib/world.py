import random
import math
import collections
import pyglet
import vector
import data
import collision

from gamelib import fx
from gamelib.enemies import base
from gamelib.enemies import virus
from gamelib.enemies import boss

Bound = collections.namedtuple('Bound', 'center radius')

class BaseWorld(object):
    
    background = pyglet.resource.image('stage_1_background.png')
    music = pyglet.resource.media('Stomach.mp3')
    music_start = 0.0
    width = 1600
    height = 1600
    name = "Void"
    world_boss = None
    virus_types = None
    
    def __init__(self, game):        
        
        self.game = game
        self.boss = self.__class__.world_boss
        self.countdown = 120

        self.bounds = []
        self.center = vector.Vec2d(self.width/2, self.height/2)
        self.build_up = True
        self.max_build_up = 15
        self.pickup_rate = 30
        self.pickup_accumulator = 0
        self.effects = []
  
        if pyglet.media.have_avbin:
            self.music_player = pyglet.media.Player()
            self.music_player.queue(self.music)
            self.music_player.seek(self.music_start)    
            self.music_player.play()
            self.music_player.eos_action = pyglet.media.Player.EOS_LOOP
        else:
            print "Avbin not found, you're going to be missing some awesome music :("
            
       
    def within_bounds(self, pos, radius):
        """
        Checks if a given circle defined by point pos and radius is within the bounds
        of the world.
        """
        for b in self.bounds:
            if not collision.inv_circle_to_circle(pos, radius, b.center, b.radius):
                return True
        return False
        
    def valid_location(self):
        """
        Trys to locate a valid spawn location that is: 
        A. within the level bounds
        B. not on within 320 of the player
        TODO C. not on a boss.
        """
        while True:
            b = random.choice(self.bounds)
            angle = random.random() * math.pi * 2
            mag = random.randrange(0, b.radius - 60)
            x = b.center.x + math.cos(angle) * mag
            y = b.center.y + math.sin(angle) * mag
    
            if collision.circle_to_circle(vector.Vec2d(x,y),1, self.game.player.pos, 320):
                continue
        
            return x, y        
            
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
            # self.game.next_world()
            self.build_up = True
        
        # self.current_wave = wave.Wave.generate(self.wave, self.diffculty)
        if self.build_up and random.random() < 0.2:
            for i in range(random.choice([1,1,1,1,1,1,3,5])):                
                x, y = self.valid_location()
                v = random.choice(self.virus_types)
                self.game.spawn_robot(v, 1, x, y)

    def spawn_boss(self):
        if self.boss:
            x, y = self.valid_location()
            return self.boss(800,470)
        
        
    

class Stomach(BaseWorld):
    """
    ACID BURN
    """

    background = pyglet.resource.image('stage_1_background.png')
    music = pyglet.resource.media('Stomach.mp3')
    music_start = 107.5
    width = 1600
    height = 1600
    name = 'Stomach'
    world_boss = boss.StomachBoss
    virus_types = (
        virus.GreenVirus, 
        virus.BlueVirus, 
        virus.PurpleVirus, 
        virus.SixthVirus, 
    )
    
    def __init__(self, game):
        super(Stomach, self).__init__(game)
        self.effects.append(fx.bubbles.Bubbler())
        # pyglet.clock.schedule_once(lambda dt: game.next_wave(), 0.0)
        self.bounds = [
            Bound(vector.Vec2d(800,800), 632)
        ]
                  
class Heart(BaseWorld):
    """
    ACID BURN
    """

    background = pyglet.resource.image('stage_2_background.png')
    music = pyglet.resource.media('ThemeA.mp3')
    music_start = 0.0
    width = 1600
    height = 1600
    name = 'Heart'
    virus_types = ( 
        virus.SixthVirus, 
        virus.CheezeVirus,
        virus.WormVirus,
        virus.RedVirus
    )
    
        
    def __init__(self, game):
        super(Heart, self).__init__(game)
        self.bounds = [
            Bound(vector.Vec2d(744,796), 532),
            Bound(vector.Vec2d(864,664), 532),
            Bound(vector.Vec2d(1106,426), 356),            
        ]
        # fx.effects.insert(0, fx.bubbles.Bubbler())            
        # pyglet.clock.schedule_once(lambda dt: game.next_wave(), 0.0)
        
            
class Brain(BaseWorld):
    """
    BRAAAAIIIIIN
    """

    background = pyglet.resource.image('stage_3_background.png')
    music = pyglet.resource.media('Brain.mp3')
    width = 1600
    height = 1600
    name = 'Brain'
    virus_types = (
        virus.BlueVirus, 
        virus.PurpleVirus, 
        virus.SixthVirus, 
        virus.RedVirus
    )
    
    
    def __init__(self, game):
        super(Brain, self).__init__(game)
        # fx.effects.insert(0, fx.bubbles.Bubbler())            
        # pyglet.clock.schedule_once(lambda dt: game.next_wave(), 0.0)
        self.bounds = [
            Bound(vector.Vec2d(806,941), 609),
            Bound(vector.Vec2d(812,708), 570),
            Bound(vector.Vec2d(625,325), 262),
            Bound(vector.Vec2d(995,325), 262),
        ]
        
