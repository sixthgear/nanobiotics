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
    
    def __init__(self, game, music=None):        
        
        self.game = game
        self.boss = self.__class__.world_boss
        self.countdown = 120

        self.bounds = []
        self.center = vector.Vec2d(self.width/2, self.height/2)
        
        self.boss_mode = False
        self.build_up = True
        self.crescendos = [4, 8, 16, 16, 8, 32, 32, 16, 48]
        
        self.pickup_rate = 35
        self.pickup_accumulator = 0
        self.effects = []
  
        if music and pyglet.media.have_avbin:
            self.music_player = pyglet.media.Player()
            self.music_player.eos_action = pyglet.media.Player.EOS_LOOP
            self.music_player.queue(music)
            self.music_player.seek(self.music_start)    
            self.music_player.play()
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
        
        if self.build_up and num >= self.crescendos[0]: 
            self.build_up = False
            return
            
        if not self.boss_mode and not self.build_up and num < 1:             
            # self.game.next_world()            
            self.crescendos.pop(0)
            if self.crescendos:
                self.build_up = True
            else:
                self.boss_mode = True
                self.game.spawn_boss(self.world_boss)
                        
        # self.current_wave = wave.Wave.generate(self.wave, self.diffculty)
        if self.build_up and random.random() < 0.5:
            for i in range(random.randrange(self.crescendos[0]/2)+1):                
                x, y = self.valid_location()
                v = random.choice(self.virus_types)
                self.game.spawn_robot(v, 1, x, y)
        
        
    

class Stomach(BaseWorld):
    """
    ACID BURN
    """

    background = pyglet.resource.image('stage_1_background.png')
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
        super(Stomach, self).__init__(game, music=pyglet.resource.media('Stomach.mp3'))
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
    music_start = 0.0
    width = 1600
    height = 1600
    name = 'Heart'
    world_boss = boss.HeartBoss
    virus_types = ( 
        virus.SixthVirus, 
        virus.CheezeVirus,
        virus.WormVirus,
        virus.RedVirus
    )
    
        
    def __init__(self, game):
        super(Heart, self).__init__(game, music=pyglet.resource.media('ThemeA.mp3'))
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
    width = 1600
    height = 1600
    name = 'Brain'
    world_boss = boss.BrainBoss
    virus_types = (
        virus.BlueVirus, 
        virus.PurpleVirus, 
        virus.SixthVirus, 
        virus.RedVirus
    )
    
    
    def __init__(self, game):
        super(Brain, self).__init__(game, music=pyglet.resource.media('Brain.mp3'))
        # fx.effects.insert(0, fx.bubbles.Bubbler())            
        # pyglet.clock.schedule_once(lambda dt: game.next_wave(), 0.0)
        self.bounds = [
            Bound(vector.Vec2d(806,941), 609),
            Bound(vector.Vec2d(812,708), 570),
            Bound(vector.Vec2d(625,325), 262),
            Bound(vector.Vec2d(995,325), 262),
        ]
        
