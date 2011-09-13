import pyglet
import data
import random
import obj
import vector
import constants
import gamepad
import bullet

from weapons.basicturret import BasicTurret
  
class Player(pyglet.event.EventDispatcher, obj.CompoundGameObject):
    """
    """
    speed = 640
    speed_diag = speed * 0.7071    
    vel_smooth = 0.4
    width = 64
    height = 64    
    
    def __init__(self, x, y):
        player_sprites = [(data.spritesheet[0],(0,0))] 
                
        obj.CompoundGameObject.__init__(self, player_sprites, x, y)
        
        self.alive = True        
        self.vel_target = vector.Vec2d(0, 0)
        self.target = vector.Vec2d(x,y)
        self.weapon = BasicTurret(None) # we like guns
        
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
        self.weapon.engage()

    def on_mouse_release(self, x, y, button, modifiers):
        self.weapon.disengage()
            
    def on_mouse_motion(self, x, y, dx, dy): 
        self.target.x = min(max(self.target.x + dx, 0), constants.WIDTH)
        self.target.y = min(max(self.target.y + dy, 0), constants.HEIGHT)
                 
    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers): 
        self.on_mouse_motion(x,y,dx,dy)
                                                    
    def update(self, dt):
        
        if not self.alive:
            self.weapon.disengage()
            self.weapon.update(dt)
            return
                    

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
        #self.sprite.xy = self.pos.x, self.pos.y
                
        # modify rotation
        self.sprites[0].rot = -self.vel.angle
        
        obj.CompoundGameObject.update(self, dt)

        self.weapon.update(dt, self.pos, self.target)
        
    def hit(self, other):        
        pass
        
    def die(self):
        self.alive = False        
        self.dispatch_event('on_death')    
                
Player.register_event_type('on_hit')
Player.register_event_type('on_death')
Player.register_event_type('on_respawn')
