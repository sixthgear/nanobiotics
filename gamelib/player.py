import pyglet
import data
import random
import obj
import vector
import constants
import gamepad
  
class Player(pyglet.event.EventDispatcher):
    """
    """
    speed = 10.0
    speed_diag = speed * 0.7071    
    width = 32
    height = 32    
    
    def __init__(self, x, y):    
        self.alive = True
        self.pos = vector.Vec2d(x,y)
        self.sprite = pyglet.sprite.Sprite(data.spritesheet[random.randrange(5)*8 + random.randrange(6)], self.pos.x, self.pos.y)
        self.target_velocity = vector.Vec2d(0, 0)
        self.velocity = vector.Vec2d(0, 0)
        self.target = vector.Vec2d(x,y)
        self.keys = pyglet.window.key.KeyStateHandler()
        self.gamepad = gamepad.GamepadHandler.connect()
        self.dispatch_event('on_respawn')

    def on_gamepad_connect(self):
        print 'Gamepad Connect!'
        
    def on_gamepad_button(self):
        print 'Gamepad Button!'    
        
    def on_key_press(self, symbol, modifiers):
        pass

    def on_mouse_press(self, x, y, button, modifiers):
        self.sprite.image = data.spritesheet[random.randrange(5)*8 + random.randrange(6)]
        
    def on_mouse_release(self, x, y, button, modifiers):
        pass
            
    def on_mouse_motion(self, x, y, dx, dy): 
        self.target.x = min(max(self.target.x + dx, 0), constants.WIDTH)
        self.target.y = min(max(self.target.y + dy, 0), constants.HEIGHT)
                 
    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers): 
        self.on_mouse_motion(x,y,dx,dy)
                                        
    def render(self):        
        self.sprite.draw()
                
    def update(self):
        if not self.alive: return
        
            
        self.target_velocity.zero()
        
        if self.gamepad:

            self.gamepad.update()
                
            if abs(self.gamepad.axis[0]) > 0.1 or abs(self.gamepad.axis[1]) > 0.1:
                self.target_velocity.x = self.gamepad.axis[0]
                self.target_velocity.y = -self.gamepad.axis[1]
                if self.target_velocity.magnitude_sq > 1:
                    self.target_velocity.normalize()            
                self.target_velocity *= self.__class__.speed

        if self.keys[pyglet.window.key.A]:                        
            if self.keys[pyglet.window.key.W]:
                self.target_velocity.y += self.__class__.speed_diag
                self.target_velocity.x -= self.__class__.speed_diag
            elif self.keys[pyglet.window.key.S]:
                self.target_velocity.y -= self.__class__.speed_diag
                self.target_velocity.x -= self.__class__.speed_diag
            else:
                self.target_velocity.x -= self.__class__.speed            
        elif self.keys[pyglet.window.key.D]:            
            if self.keys[pyglet.window.key.W]:
                self.target_velocity.y += self.__class__.speed_diag
                self.target_velocity.x += self.__class__.speed_diag
            elif self.keys[pyglet.window.key.S]:
                self.target_velocity.y -= self.__class__.speed_diag
                self.target_velocity.x += self.__class__.speed_diag
            else:
                self.target_velocity.x += self.__class__.speed
        else:                        
            if self.keys[pyglet.window.key.W]:
                self.target_velocity.y += self.__class__.speed
            elif self.keys[pyglet.window.key.S]:
                self.target_velocity.y -= self.__class__.speed
            else:
                pass
        
        self.velocity += (self.target_velocity - self.velocity ) * 0.4
        self.pos += self.velocity        
        self.sprite.position = self.pos.x, self.pos.y
        self.sprite.rotation = self.velocity.angle
    
    def hit(self, other):        
        pass
        
    def die(self):
        self.alive = False        
        self.dispatch_event('on_death')    
                
Player.register_event_type('on_hit')
Player.register_event_type('on_death')
Player.register_event_type('on_respawn')
