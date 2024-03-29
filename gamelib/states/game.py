import pyglet
import rabbyt
import random
import math

from gamelib import bullet
from gamelib import camera
from gamelib import collision
from gamelib import data
from gamelib import fixedsteploop
from gamelib import fx
from gamelib import player
from gamelib import vector
from gamelib import world

from gamelib.pickups import base, ship, bomb

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
        self.world = None
        self.worlds = [ 
            world.Stomach, 
            world.Heart, 
            world.Brain 
        ]
          
        self.player = player.Player(0,0)
        self.robots = []
        self.pickups = []
        self.boss = None
        
        self.camera = vector.Vec2d()
        self.cursor = vector.Vec2d(WIDTH//2,HEIGHT//2)
        
        # sorted list of objects to render back to front
        self.render_list = []
                            
        # event handlers
        self.window.push_handlers(self.player)
        self.window.push_handlers(self.player.keys)
        # self.player.gamepad.push_handlers(self)
        if self.player.gamepad:
            self.player.gamepad.push_handlers(self.player)        
        self.player.push_handlers(self)

        # timers
        # self.timer = fixedsteploop.FixedStepLoop(self.update, TIME_STEP, MAX_CYCLES_PER_FRAME)
        # self.timer.play()
        pyglet.clock.schedule_interval(self.update, 1.0/60)
        pyglet.clock.schedule_interval(self.ai, 1.0/2)
        pyglet.clock.schedule_interval_soft(self.collect_garbage, 10.0)
                
        # HUD stuff        
        self.announcing = False

        self.announcement = pyglet.text.Label(
            font_name=['DYLOVASTUFF', 'DYLOVASTUFF'],
            text='READY', 
            font_size=144, x=WIDTH//2, y=HEIGHT//2,
            anchor_x='center', anchor_y='center',
            color=(255,255,255,255))
            
        # self.announce('READY', 3.0)
 
        self.player_inventory = pyglet.text.Label(
            text='Lives: 00   Bombs: 00', 
            font_name=['DYLOVASTUFF', 'DYLOVASTUFF'], font_size=18, x=WIDTH-20, y=10,
            anchor_x='right', anchor_y='bottom',
            color=(255,255,255,255)
        )
        
        self.score_label = pyglet.text.Label(
            text='1234567890', 
            font_name=['DYLOVASTUFF', 'DYLOVASTUFF'], font_size=18, x=WIDTH-20, y=HEIGHT-20,
            anchor_x='right', anchor_y='top',
            color=(255,255,255,255)
        )

        # lets do this!
        self.rebuild_render_list()
        self.next_world()
        # self.switch_world(self.worlds[0])
        self.player.pos = self.world.center.copy()
        self.camera = camera.Camera(self.world, 0, 0)
        self.camera.update(self.player.pos)
        
        # rabbyt.set_time(0)
        
    def on_key_press(self, symbol, modifiers):
        """
        Perform oneoff key press actions.
        """
        pass
        # if symbol == pyglet.window.key.Z:            
        #     self.next_world()
        # if symbol == pyglet.window.key.B:
        #     boss = self.world.world_boss
        #     if boss:
        #         self.spawn_boss(boss)
        #         self.player.invuln = 3
        #     else:
        #         pass
        #         # print "no boss"
                    
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
        # print "garbage collected, %d renderings" % len(self.render_list)
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
        
    def on_mouse_motion(self, x, y, dx, dy): 
        self.cursor.x = min(max(self.cursor.x + dx, 0), WIDTH)
        self.cursor.y = min(max(self.cursor.y + dy, 0), HEIGHT)
                 
    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers): 
        self.on_mouse_motion(x,y,dx,dy)        

    def on_draw(self):
        """
        Draw the game scene. Various sprite libs are not great at cleaning up 
        their OpenGL states, so we need to set the color before bliting images.
        """
        self.window.viewport.begin()
        self.window.clear()
        
        pyglet.gl.glPushMatrix()
        # render background        
        pyglet.gl.glTranslatef(-self.camera.x, -self.camera.y, 0)
        
        # pyglet.gl.glColor4f(1, 1, 1, 1)
        self.world.draw()
                
        # render characters and pickups

        self.render_list.sort(key=lambda x: x.pos.y, reverse=True)
        for r in (r for r in self.render_list if r.alive):
            r.render()

        # render foreground
        pyglet.gl.glColor4f(1, 1, 1, 1)
            
        # render particles and bullets
        fx.draw()
        bullet.pool.draw()
        
        # render HUD        
        pyglet.gl.glPopMatrix()
        self.player_inventory.draw()
        self.score_label.draw()
        if self.announcing: 
            self.announcement.draw()
        
        if self.boss:
            hw = WIDTH // 2
            bh = min(500, int(500.0 * (self.boss.life /
                                       float(self.boss.__class__.life))))
            hp = hw - data.boss_hud[1].width // 2
            data.boss_hud[0].blit(hw, HEIGHT - 60)
            data.boss_hud[1].get_region(0,0,bh,10).blit(hp, HEIGHT - 65)
                
        # render cursor        
        data.cursor.blit(self.cursor.x, self.cursor.y)
        
        self.window.viewport.end()
                               
    def announce(self, text, duration):
        """
        Announce some big important message.
        """
        self.announcing = True        
        self.announcement.text = text
        if len(text) < 10:
            self.announcement.font_size = 144
        else:
            self.announcement.font_size = 108
            
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
        
        rabbyt.add_time(dt)
        
        self.tick += 1        
        self.player.update(dt)
        self.world.update(dt)
        self.camera.update(self.player.pos, 0)
        
        self.player.target = self.camera + self.cursor
        
        [r.update(dt) for r in self.robots]
        bullet.pool.update(dt)        
        # fx.gibber.target.x, fx.gibber.target.y = self.player.pos.x, self.player.pos.y
        fx.update(dt)        
        self.collide()
        
        
                    
    def ai(self, dt):
        """
        The AI method is called only 1/2 seconds, and it the function that determines
        when to make game state changes and asks the computer controlled characters to
        make decisions on what to do next
        """                       
        # update current wave
        self.world.ai()
        
        # update robots
        for r in self.robots:
            r.ai(self) 
            
        # update pickups    
        for p in self.pickups:
            p.ai(self)


    def switch_world(self, world):
        self.collect_garbage()
        if self.world:
            self.world.music_player.pause()
            self.world.music_player = None
        # self.world = None
        self.world = world(self)
        self.announce('The %s' % self.world.name, 3.0)
        
    def next_world(self):
        """
        Being the next world!
        """
        self.add_score(0)
                
        if self.worlds:
            self.switch_world(self.worlds.pop(0))

        else:
            pass # player wins

    def next_wave(self):      
        """
        Begin the next wave!
        """
        self.collect_garbage()
        self.wave += 1
                
        self.announce('WAVE %d' % self.wave, 3.0)
        
            
    def spawn_robot(self, robot, n=1, x=None, y=None):
        """
        Create a mechanical (biological?) horror.
        """
        if not x or not y:
            r = [robot() for r in range(n)]
        else:
            r = [robot(x,y) for r in range(n)]

        for roebit in r:
            roebit.set_target(self.player)

        self.robots += r
        self.render_list += r
        
    def spawn_boss(self, boss):
        self.boss = boss()
        self.boss.set_target(self.player)
        self.robots.append(self.boss)
        self.render_list.append(self.boss)        
        self.boss.push_handlers(self)
                                            
    def on_boss_death(self):

        for r in self.robots:
            if r.alive: r.die()
        
        if not self.worlds:
            pyglet.clock.schedule_once(lambda dt: self.win(), 3.0)
        else:    
            pyglet.clock.schedule_once(lambda dt: self.next_world(), 3.0)
                    
    def spawn_pickup(self,x=None,y=None,type=None):
        """
        Create a helpful thing.
        """        
        p_class = random.choice((
            base.MachineGunPickup,
            base.SpreadGunPickup,
            base.FireHosePickup,
            ship.Ship,
            bomb.Bomb))
        p = p_class(x,y,type)                
        self.pickups.append(p)
        self.render_list.append(p)            
        
    def add_score(self, score):
        """
        Add some score
        """        
        self.score += score

        if self.score < 9999999999:
            self.score_label.text = '%010d' % self.score
        else:
            self.score_label.text = '%d' % self.score

        self.player_inventory.text = 'Lives: %02d   Bombs: %02d' % (self.player.lives, 
                                                                    self.player.bombs) 
                
    def collide(self):
        """
        Heres where we detect us some collisions.
        """
                
        # bullets vs world
        for b in (b for b in bullet.pool.active if b.alive):
            if not self.world.within_bounds(b.pos, 12):
                b.die()                

        # robots vs player bullets
        for r, b in rabbyt.collisions.collide_groups(self.robots, bullet.pool.active):
            if not r.alive: continue
            if not b.alive or not b.group==0: continue
            b.die()
            r.hit(b)
            if not r.alive: self.on_kill(r)
                
        if not self.player.alive: return
        
        # player vs world                    
        if not self.world.within_bounds(self.player.pos, 18): 
               
            nb = None
            npd = 10000
            
            for b in self.world.bounds:
                p_distance = (self.player.pos - b.center).magnitude - abs(b.radius - 18)
                if p_distance < npd:
                    npd = p_distance
                    nb = b
                    
            p_distance = npd
            p_normal = (self.player.pos - nb.center).normal
            p_vector = p_distance * p_normal
            self.player.pos -= p_vector
            self.player.sprites[0].xy = self.player.pos.x, self.player.pos.y
                    
         
        # player vs robots
        for r in rabbyt.collisions.collide_single(self.player, self.robots):
            if not r.alive: continue
            self.player.hit(r)
            # bail out if the player dies, since we don't need to test any further collisions
            # as they all pertain to the player
            if not self.player.alive: return
                         
        # player vs robot bullets
        for b in rabbyt.collisions.collide_single(self.player, bullet.pool.active):
            if not b.alive or not b.group==1: continue
            b.die()
            self.player.hit(b)
            # bail out if the player dies, since we don't need to test any further collisions
            # as they all pertain to the player            
            if not self.player.alive: return
                    
        # player vs pickups
        for p in rabbyt.collisions.collide_single(self.player, self.pickups):
            if not p.alive: continue
            p.activate(self, self.player)
            p.die()
            self.add_score(0) # update hud
    
    def on_bomb(self):
        """
        Player killed all the things
        """
        p = 0

        for r in self.robots:
            if r.alive:
                if r.is_boss:
                    r.life -= 15
                else:
                    r.die()
                    p += r.points
            

        bullet.pool.kill_group(1) # kill off enemy bullets 

        self.add_score(p)

    def on_hit(self, a, b):
        """
        Player got hit.
        """
        pass
        
    def on_kill(self, robot):
        """
        Player killed something.
        """
        if robot.is_boss:
            self.boss = None
      
        self.add_score(robot.points)
            
    def on_death(self):
        """
        Player bites the dust.
        """
        # update lives text
        # self.lives_label.text = "%d" % self.player.lives
        for r in self.robots:
            if r.alive and not r.is_boss: r.die()

        self.add_score(0) # update hud
                                
        # check for gameover
        if self.player.lives == 0:
            self.game_over()
            return
        
        pyglet.clock.schedule_once(self.player.respawn, 3.0, self.world.center)
        
    def on_respawn(self):
        """
        Player just respawned.
        """                        
        pass
        
    def win(self):
        self.announce("YOU WIN!", 10)
        pyglet.clock.schedule_once(self.shutdown, 10.0)
                
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
        self.world.music_player.pause()
        del self.world.music_player
        pyglet.clock.unschedule(self.update)
        pyglet.clock.unschedule(self.ai)
        pyglet.clock.unschedule(self.collect_garbage)
        bullet.pool.clear()
        fx.clear()
        pyglet.clock.schedule_once(self.window.title, 0.0)
