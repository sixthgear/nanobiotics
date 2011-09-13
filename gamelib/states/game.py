import pyglet
import rabbyt
import random

from gamelib import data
from gamelib import player
from gamelib import bullet
from gamelib import collision
from gamelib.enemies import base

from gamelib.constants import *

class Game(object):
    """
    The game object is the BOSS.
    """
    def __init__(self, window):
        
        # keep a window context so we can exit back to the title screen on gameover
        self.window = window

        self.tick = 0    
        self.wave = 0
        self.score = 0
        self.diffculty = NORMAL
        self.current_wave = None
        
        # game objects
        self.player = player.Player(WIDTH//2,HEIGHT//2)
        self.robots = []
        self.pickups = []

        # sorted list of objects to render back to front
        self.render_list = []
                            
        # event handlers
        self.window.push_handlers(self.player)
        self.window.push_handlers(self.player.keys)
        self.window.push_handlers(self.player.gamepad)
        self.player.push_handlers(self)

        # timers       
        pyglet.clock.schedule_interval(self.update, 1.0/60)
        pyglet.clock.schedule_interval(self.ai, 1.0/2)
        pyglet.clock.schedule_interval_soft(self.collect_garbage, 10.0)
        
        # music
        # self.music = pyglet.media.Player()
        # self.music.queue(pyglet.resource.media('unmute.mp3'))
        # self.music.play()
        # self.music.eos_action = pyglet.media.Player.EOS_LOOP
        
        # HUD stuff        
        self.announcing = False

        self.announcement = pyglet.text.Label(
            font_name=['DYLOVASTUFF', 'DYLOVASTUFF'],
            text='READY', 
            font_size=144, x=WIDTH//2, y=HEIGHT//2,
            anchor_x='center', anchor_y='center',
            color=(255,255,255,200))
            
        self.announce('READY', 3.0)
        
        self.score_label = pyglet.text.Label(
            text='1234567890', 
            font_name=['DYLOVASTUFF', 'DYLOVASTUFF'], font_size=18, x=WIDTH-20, y=HEIGHT-20,
            anchor_x='right', anchor_y='top',
            color=(255,255,255,255)
        )
                     
       # lets do this!
        self.rebuild_render_list()
        self.next_wave()

    def collect_garbage(self, dt=0.0):
        """
        This function will remove all of the dead objects in the robots and 
        build a new list without them. We don't remove dead objects immediately
        because of how slow python list removal is. It is much better to 
        track what objects are "dead" and then rebuild our list periodically.
        This is why we constantly check if objects are "alive" in various places.
        """
        self.robots = [r for r in self.robots if r.alive]
        self.pickups = [p for p in self.pickups if p.alive]
        print "garbage collected, %d renderings" % len(self.render_list)
        self.rebuild_render_list()
        
    def rebuild_render_list(self):
        """
        This function rebuilds our render list. We need to keep a separate list
        of renderable objects so that we can sort it and draw from back to front.
        One of the goals is to remove this completely and use OpenGL for z-sorting.
        """
        self.render_list = [r for r in self.robots]
        self.render_list += [p for p in self.pickups]
        self.render_list.append(self.player)        

    def on_draw(self):
        """
        Draw the game scene. Various sprite libs are not great at cleaning up 
        their OpenGL states, so we need to set the color before bliting images.
        """
        self.window.viewport.begin()
        self.window.clear()
                        
        # render background
        # pyglet.gl.glColor4f(1, 1, 1, 1)
        data.background.blit(0,0)
                
        # render characters and pickups
        rabbyt.set_default_attribs()
        self.render_list.sort(key=lambda x: x.pos.y, reverse=True)
        for r in (r for r in self.render_list if r.alive):
            r.render()

        # render foreground
        pyglet.gl.glColor4f(1, 1, 1, 1)
            
        # render particles and bullets
        # effects.draw()
        bullet.pool.draw()
        
        # render HUD        
        
        self.score_label.draw()
        # self.lives_label.draw()
        if self.announcing: 
            self.announcement.draw()        
                
        # render cursor        
        data.cursor.blit(self.player.target.x, self.player.target.y)
        
        self.window.viewport.end()
                               
    def announce(self, text, duration):
        """
        Announce some big important message.
        """
        self.announcing = True        
        self.announcement.text = text
        pyglet.clock.schedule_once(self.clear_announcement, duration)
        
    def clear_announcement(self, dt):
        """
        Stop announcing some big important message.
        """        
        self.announcing = False
                
    def update(self, dt):
        """
        The ever-important update method is called every 1/60 seconds.
        Step through all the important game objects and update their position.
        Perform physics and collision detection.
        """
        self.tick += 1        
        self.player.update(dt)
        [r.update() for r in self.robots]
        bullet.pool.update()        
        # effects.update(dt)        
        self.collide()
                    
    def ai(self, dt):
        """
        The AI method is called only 1/2 seconds, and it the function that determines
        when to make game state changes and asks the computer controlled characters to
        make decisions on what to do next
        """                       
        # update current wave
        # self.current_wave.ai(self)
        
        # update robots
        for r in self.robots:
            r.ai(self) 
            
        # update pickups    
        for p in self.pickups:
            p.ai(self)

    def next_wave(self):      
        """
        Begin the next wave!
        """
        self.collect_garbage()
        self.wave += 1
        # self.current_wave = wave.Wave.generate(self.wave, self.diffculty)
        for i in range(100):
            self.spawn_robot(base.BaseEnemy, 1, random.randrange(WIDTH-20)+10, random.randrange(HEIGHT-20)+10)
        
        
        self.announce('WAVE %d' % self.wave, 3.0)
        
            
    def spawn_robot(self, robot, n=1, x=None, y=None):
        """
        Create a mechanical horror.
        """
        if not x or not y:
            r = [robot() for r in range(n)]
        else:
            r = [robot(x,y) for r in range(n)]        
        self.robots += r
        self.render_list += r
                                             
    def spawn_pickup(self,x=None,y=None,type=None):
        """
        Create a helpful thing.
        """        
        p = pickup.Pickup(x,y,type)
        self.pickups.append(p)
        self.render_list.append(p)            
        
    def add_score(self, score):
        """
        Add some score
        """        
        self.score += score
        self.score_label.text = '%d' % self.score
                
    def collide(self):
        """
        Heres where we detect us some collisions.
        """        
        # bullets vs screen
        for b in (b for b in bullet.pool.active if b.alive):
            if not collision.AABB_to_AABB(b.pos.x-2, b.pos.y-2, 4, 4, 0, 0, WIDTH, HEIGHT):
                b.die()
     
        # player vs screen                    
        self.player.pos.x = min(max(32, self.player.pos.x), WIDTH)
        self.player.pos.y = min(max(50, self.player.pos.y), HEIGHT)

        # robots vs player bullets
        for r, b in rabbyt.collisions.collide_groups(self.robots, bullet.pool.active):
            if not r.alive: continue
            if not b.alive or not b.group==0: continue
            b.die()
            r.hit(b)
            if not r.alive: self.on_kill(r)
                
        # if not self.player.alive: return
        # 
        # # player vs robots
        # for r in rabbyt.collisions.collide_single(self.player, self.robots):
        #     if not r.alive: continue
        #     if self.player.form == player.MONSTER:
        #         r.hit(self.player)
        #         if not r.alive: self.on_kill(r)
        #     elif not self.player.invincible:
        #         self.player.hit(r)
        #     # bail out if the player dies, since we don't need to test any further collisions
        #     # as they all pertain to the player
        #     if not self.player.alive: return
        #                 
        # # player vs robot bullets
        # for b in rabbyt.collisions.collide_single(self.player, bullet.pool.active):
        #     if not b.alive or not b.group==1: continue
        #     # if b.group == 0 or not b.alive: continue
        #     b.die()
        #     self.player.hit(b)
        #     # bail out if the player dies, since we don't need to test any further collisions
        #     # as they all pertain to the player            
        #     if not self.player.alive: return
        #             
        # # player vs pickups
        # for p in rabbyt.collisions.collide_single(self.player, self.pickups):
        #     if not p.alive: continue
        #     p.activate(self)
        #     p.die()
    
    def on_hit(self, a, b):
        """
        Player got hit.
        """
        pass

    def on_kill(self, robot):
        """
        Player killed something.
        """        
        pass
            
    def on_death(self):
        """
        Player bites the dust.
        """                
        # update lives text
        # self.lives_label.text = "%d" % self.player.lives
                                
        # check for gameover
        # if self.player.lives == 0:
        #     self.game_over()
        
    def on_respawn(self):
        """
        Player just respawned.
        """                
        pass
        
    def on_transform(self):    
        """
        Player just transformed.
        """                        
        pass
                
    def game_over(self):
        """
        Game over man! Game over! -- Sgt. Hicks
        """                        
        self.announce("GAME OVER", 4)
        pyglet.clock.schedule_once(self.shutdown, 4.0)
        
    def shutdown(self, dt=0.0):
        """
        Goodnight. Try to clean up so we dont have any issues when we start again.
        """                        
        self.robots = []
        self.render_list = []
        self.window.remove_handlers(self.player.keys)
        self.window.remove_handlers(self.player)
        self.music.pause()
        pyglet.clock.unschedule(self.update)
        pyglet.clock.unschedule(self.ai)
        pyglet.clock.unschedule(self.collect_garbage)
        bullet.pool.clear()
        effects.clear()
        pyglet.clock.schedule_once(self.window.title, 0.0)