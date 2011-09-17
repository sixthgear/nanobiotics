import pyglet
import rabbyt
import data
import random
import obj
import vector
import constants
import gamepad
import bullet
import collision
import fx

from weapons.basicturret import BasicTurret
from weapons.twinturret import TwinTurret, FireHose
from weapons.tripleturret import TripleTurret
  
class Player(pyglet.event.EventDispatcher, obj.CompoundGameObject):
    """
    """
    speed = 540
    speed_diag = speed * 0.7071    
    vel_smooth = 0.25
    width = 64
    height = 64 
    invuln = 3
    lives = 3
    bombs = 1
    trail_tex = data.spritesheet[1]

    def __init__(self, x, y):
        player_sprites = [
            (data.spritesheet[0],(0,0)), 
        ] 
                
        obj.CompoundGameObject.__init__(self, player_sprites, x, y)
        
        self.alive = True        
        self.vel_target = vector.Vec2d(0, 0)
        self.target = vector.Vec2d(x,y)
        self.weapon = [BasicTurret(None)] # we like guns
        
        # pyglet events
        self.keys = pyglet.window.key.KeyStateHandler()
        self.gamepad = gamepad.GamepadHandler.connect()
        self.dispatch_event('on_respawn')
        
        self.trail = []
        for t in range(20):
            self.trail.append(rabbyt.Sprite(self.trail_tex, x=x, y=y))
        self.trail_counter = 0
        self.trail_acc = 0.0

    def on_gamepad_connect(self):
        print 'Gamepad Connect!'
        
    def on_gamepad_button(self):
        print 'Gamepad Button!'    
        
    def on_key_press(self, symbol, modifiers):
        """
        Perform oneoff key press actions.
        """
        if symbol == pyglet.window.key.SPACE:
            # I came to drop bombs
            if self.bombs > 0:
                # TODO SOUNDS
                self.bombs -= 1
                self.dispatch_event('on_bomb')
            else:
                pass # CLICK CLICK, EMPTY!
                
        elif symbol == pyglet.window.key._1:
            w = BasicTurret(None)
            w.engaged = self.weapon[-1].engaged
            self.weapon[-1] = w
        elif symbol == pyglet.window.key._2:
            w = TwinTurret(None)
            w.engaged = self.weapon[-1].engaged
            self.weapon[-1] = w
        elif symbol == pyglet.window.key._3:
            w = TripleTurret(None)
            w.engaged = self.weapon[-1].engaged
            self.weapon[-1] = w
        elif symbol == pyglet.window.key._4:
            w = FireHose(None)
            w.engaged = self.weapon[-1].engaged
            self.weapon[-1] = w
            
    def render(self):
        pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
        pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE)        
        rabbyt.render_unsorted(self.trail)
        
        super(Player, self).render()
            
    def on_mouse_press(self, x, y, button, modifiers):
        self.weapon[-1].engage()

    def on_mouse_release(self, x, y, button, modifiers):
        self.weapon[-1].disengage()
                                                                
    def update(self, dt):
        
        if not self.alive:
            self.weapon[-1].disengage()
            self.weapon[-1].update(dt)
            return

        if self.invuln > 0:
            self.invuln -= dt
                    
        self.vel_target.zero()
        
        if self.gamepad:
            # we might want to move this into the pyglet event loop
            self.gamepad.update()
            self.vel_target.x = self.gamepad.axis[0]
            self.vel_target.y = -self.gamepad.axis[1]
            
            if self.gamepad.axis[2] or self.gamepad.axis[3]:
                if not self.weapon[-1].engaged:
                    self.weapon[-1].engage()
                rel_target = vector.Vec2d(self.gamepad.axis[2], -self.gamepad.axis[3]).normal * 200
                self.target = self.pos + rel_target
            else:
                self.weapon[-1].disengage()
                        
        if self.keys[pyglet.window.key.A]:                        
            if self.keys[pyglet.window.key.W]:
                self.vel_target.y += 0.7071
                self.vel_target.x -= 0.7071
            elif self.keys[pyglet.window.key.S]:
                self.vel_target.y -= 0.7071
                self.vel_target.x -= 0.7071
            else:
                self.vel_target.x -= 1.0          
        elif self.keys[pyglet.window.key.D]:            
            if self.keys[pyglet.window.key.W]:
                self.vel_target.y += 0.7071
                self.vel_target.x += 0.7071
            elif self.keys[pyglet.window.key.S]:
                self.vel_target.y -= 0.7071
                self.vel_target.x += 0.7071
            else:
                self.vel_target.x += 1.0
        else:                        
            if self.keys[pyglet.window.key.W]:
                self.vel_target.y += 1.0
            elif self.keys[pyglet.window.key.S]:
                self.vel_target.y -= 1.0
            else:
                pass
        
        # normalize target velocity to length 1
        if self.vel_target.magnitude_sq > 1:
            self.vel_target.normalize()

        self.vel_target *= self.speed
            
        # smooth velocity changes
        self.vel += (self.vel_target - self.vel ) * self.__class__.vel_smooth
    
        if self.weapon[-1].__class__ == FireHose and self.weapon[-1].engaged:
            norm = (self.target-self.pos).normal
            self.vel -= norm * 100
            self.rot = -norm.angle
        else:
            # modify rotation
            self.rot = -self.vel.angle
            
            
        # do regular euler updates
        self.pos += self.vel * dt
        #self.sprite.xy = self.pos.x, self.pos.y
                

        # # update turrets
        # rot = -(self.target - self.pos).angle
        # for s in self.sprites[1:]:
        #     s.rot = rot
        
        obj.CompoundGameObject.update(self, dt)
        self.weapon[-1].update(dt, self.pos, self.target)
        
        self.trail_acc -= dt
        if self.trail_acc <= 0:
            self.trail_acc = 0.05
            self.trail_counter = (self.trail_counter + 1) % len(self.trail) 
            self.trail[self.trail_counter].xy = self.sprites[0].xy        
            self.trail[self.trail_counter].alpha = rabbyt.lerp(0.3,0, dt=0.8)
            
        
        
    def hit(self, other):        
        if self.invuln > 0:
            pass
            # imagine shields sounds
        else:
            self.die() # bummer 
        
    def die(self):
        fx.exploder.explode(self.pos.x, self.pos.y)
        self.alive = False
        self.lives -= 1
        self.weapon = [BasicTurret(None)]
        self.dispatch_event('on_death')

    def respawn(self, dt, loc):
        self.pos = loc
        self.vel_target = vector.Vec2d(0, 0)
        self.invuln = 3
        self.alive = True

        self.dispatch_event("on_respawn")    
                
Player.register_event_type('on_bomb')
Player.register_event_type('on_hit')
Player.register_event_type('on_death')
Player.register_event_type('on_respawn')
