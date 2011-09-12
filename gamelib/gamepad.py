import pyglet
try:
    import pygame
    pygamefound = True
except ImportError:
    pygamefound = False

class GamepadHandler(pyglet.event.EventDispatcher):
    
    def __init__(self, id):
        
        self.buttons = {}
        self.hats = {}
        self.axis = {}        

        self.j = pygame.joystick.Joystick(id)
        self.j.init()
        self.dispatch_event('on_gamepad_connect')
        
    def update(self):
        pygame.event.pump()
        for a in range(self.j.get_numaxes()):
            self.axis[a] = self.j.get_axis(a)
        for b in range(self.j.get_numbuttons()):
            self.buttons[b] = self.j.get_button(b)
            if self.buttons[b]: 
                self.dispatch_event('on_gamepad_button')
                print 'button %d' % b
            
    @classmethod
    def connect(cls):
        if not pygamefound:
            print "Could not import pygame, gamepad support disabled."
            return None
            
        pygame.init()
        count = pygame.joystick.get_count()
        if not count: 
            return None
        else:
            return cls(0)
                
GamepadHandler.register_event_type('on_gamepad_connect')