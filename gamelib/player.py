import pyglet
import data
import random
import obj
import vector
import constants
import gamepad
import bullet
  
class Player(pyglet.event.EventDispatcher, obj.GameObject):
    """
    """
    speed = 640
    speed_diag = speed * 0.7071    
    vel_smooth = 0.4
    width = 64
    height = 64    
    
    def __init__(self, x, y):    
                
        obj.GameObject.__init__(self, data.spritesheet[0], x, y)
        
        self.alive = True        
        self.vel_target = vector.Vec2d(0, 0)
        self.target = vector.Vec2d(x,y)
        self.cooldown = 2
        self.firing = False
        
        # pyglet events
        self.keys = pyglet.window.key.KeyStateHandler()
        self.gamepad = gamepad.GamepadHandler.connect()
        self.dispatch_event('on_respawn')

    def on_gamepad_connect(self):
        print 'Gamepad Connect!'
        
    def on_gamepad_button(self):
        print 'Gamepad Button!'    
        
    def on_key_press(self, symbol, modifiers):
        """
        Perform oneoff key press actions.
        """
        pass
        
    def on_mouse_press(self, x, y, button, modifiers):
        self.firing = True        

    def on_mouse_release(self, x, y, button, modifiers):
        self.firing = False
            
    def on_mouse_motion(self, x, y, dx, dy): 
        self.target.x = min(max(self.target.x + dx, 0), constants.WIDTH)
        self.target.y = min(max(self.target.y + dy, 0), constants.HEIGHT)
                 
    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers): 
        self.on_mouse_motion(x,y,dx,dy)
                                                    
    def update(self, dt):
        
        if not self.alive: return
                    
        self.vel_target.zero()
        
        if self.gamepad:
            # we might want to move this into the pyglet event loop
            self.gamepad.update()
            self.vel_target.x = self.gamepad.axis[0]
            self.vel_target.y = -self.gamepad.axis[1]

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

        self.vel_target *= self.__class__.speed
            
        # smooth velocity changes
        self.vel += (self.vel_target - self.vel ) * self.__class__.vel_smooth
    
        # do regular euler updates
        self.pos += self.vel * dt
        self.sprite.xy = self.pos.x, self.pos.y
                
        # modify rotation
        self.sprite.rot = -self.vel.angle
        
        if self.firing:
            self.fire(self.pos, self.target)
        
    def fire(self, source, dest):
        
        if self.cooldown > 0:
            self.cooldown -= 1
            return
            
        self.cooldown = 2
                
        bv = (dest - source).normal * 40
        bp = source # + bv
        if bv.x != 0 or bv.y != 0:            
            bullet.pool.fire(bp.x, bp.y, bv.x, bv.y)
                        
    def hit(self, other):        
        pass
        
    def die(self):
        self.alive = False        
        self.dispatch_event('on_death')    
                
Player.register_event_type('on_hit')
Player.register_event_type('on_death')
Player.register_event_type('on_respawn')
