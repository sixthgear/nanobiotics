import pyglet
try:
    import pygame
    pygamefound = True
    pygame.display.init()
    pygame.joystick.init()
    pygame.event.set_allowed([
        pygame.JOYAXISMOTION, 
        pygame.JOYBALLMOTION, 
        pygame.JOYHATMOTION, 
        pygame.JOYBUTTONUP, 
        pygame.JOYBUTTONDOWN
    ])
except ImportError:
    pygamefound = False

class GamepadHandler(pyglet.event.EventDispatcher):
    
    def __init__(self, id):
        
        self.buttons = {}
        self.hats = {}
        self.axis = {}        
        self.deadzone = 0.2
                        
        self.j = pygame.joystick.Joystick(id)
        self.j.init()
        
        for a in range(self.j.get_numaxes()):
            self.axis[a] = 0.0
            
        for b in range(self.j.get_numbuttons()):
            self.buttons[b] = 0
            
        self.dispatch_event('on_gamepad_connect')
        
    def update(self):
        
        # this should go somehwhere else.
        pygame.event.pump()
        
        for a in range(self.j.get_numaxes()):
            self.axis[a] = self.j.get_axis(a)
        
        # if abs(self.axis[a]) < self.deadzone: self.axis[a] = 0.0    
        if abs(self.axis[0]) < self.deadzone and abs(self.axis[1]) < self.deadzone:
            self.axis[0] = self.axis[1] = 0.0    
            
        if abs(self.axis[2]) < self.deadzone and abs(self.axis[3]) < self.deadzone:
            self.axis[2] = self.axis[3] = 0.0
        
            
        for b in range(self.j.get_numbuttons()):
            old_b_state = self.buttons[b]
            self.buttons[b] = self.j.get_button(b)
            
            if self.buttons[b] and not old_b_state:
                self.dispatch_event('on_gamepad_button', b)
                # print 'button %d' % b
            
    @classmethod
    def connect(cls):
        
        if not pygamefound:
            print "Could not import pygame, gamepad support disabled."
            return None
                    
        count = pygame.joystick.get_count()
        if not count: 
            return None
        else:
            return cls(0)
                
GamepadHandler.register_event_type('on_gamepad_connect')
GamepadHandler.register_event_type('on_gamepad_button')