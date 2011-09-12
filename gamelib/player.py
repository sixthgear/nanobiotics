import pyglet
import data
import random
import obj
import vector
import constants
  
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
        self.sprite = pyglet.sprite.Sprite(data.spritesheet[0], self.pos.x, self.pos.y)
        self.velocity = vector.Vec2d(0, 0)
        self.target = vector.Vec2d(x,y)
        self.keys = pyglet.window.key.KeyStateHandler()
        self.dispatch_event('on_respawn')

    def on_key_press(self, symbol, modifiers):
        pass

    def on_mouse_press(self, x, y, button, modifiers):
        pass
        
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
        
        self.velocity.zero()

        if self.keys[pyglet.window.key.A]:                        
            if self.keys[pyglet.window.key.W]:
                self.velocity.y += self.__class__.speed_diag
                self.velocity.x -= self.__class__.speed_diag
            elif self.keys[pyglet.window.key.S]:
                self.velocity.y -= self.__class__.speed_diag
                self.velocity.x -= self.__class__.speed_diag
            else:
                self.velocity.x -= self.__class__.speed            
        elif self.keys[pyglet.window.key.D]:            
            if self.keys[pyglet.window.key.W]:
                self.velocity.y += self.__class__.speed_diag
                self.velocity.x += self.__class__.speed_diag
            elif self.keys[pyglet.window.key.S]:
                self.velocity.y -= self.__class__.speed_diag
                self.velocity.x += self.__class__.speed_diag
            else:
                self.velocity.x += self.__class__.speed
        else:                        
            if self.keys[pyglet.window.key.W]:
                self.velocity.y += self.__class__.speed
            elif self.keys[pyglet.window.key.S]:
                self.velocity.y -= self.__class__.speed
            else:
                pass
        
        self.pos += self.velocity        
        self.sprite.position = self.pos.x, self.pos.y
    
    def hit(self, other):        
        pass
        
    def die(self):
        self.alive = False        
        self.dispatch_event('on_death')    
                
Player.register_event_type('on_hit')
Player.register_event_type('on_death')
Player.register_event_type('on_respawn')
