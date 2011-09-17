import pyglet
import rabbyt
from pyglet.gl import *
from pyglet.window import key
import states.title
import states.game
import fixed_resolution
import constants

if not pyglet.media.have_avbin:
    print 'You need to install AVbin http://code.google.com/p/avbin/ to play this game.'

class Controller(pyglet.window.Window):
    
    def __init__(self):
        super(Controller, self).__init__(width=constants.WIDTH, height=constants.HEIGHT, caption="Nanobiotics")#, fullscreen=True)        
        self.viewport = fixed_resolution.FixedResolutionViewport(self, constants.WIDTH, constants.HEIGHT, filtered=False)        
        rabbyt.set_viewport((constants.WIDTH, constants.HEIGHT))
        rabbyt.set_default_attribs()        
        
        self.set_exclusive_mouse(True)
        self.set_mouse_visible(False)
        self.state = None
        self.fps_display = pyglet.clock.ClockDisplay()

                
    def switch(self, state):
        if self.state:
            self.remove_handlers(self.state)        
        self.state = state(self)
        self.push_handlers(self.state)
        
    def title(self, dt):
        self.state.music.pause()
        self.switch(states.title.Title)

    def play(self, dt):
        self.state.music.pause()
        self.switch(states.game.Game)
        
    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            pyglet.app.exit()
        elif symbol == key.F and (modifiers & key.MOD_CTRL or modifiers & key.MOD_COMMAND):
            self.set_fullscreen(not self.fullscreen)
            if not self.fullscreen:
                self.width, self.height = constants.WIDTH, constants.HEIGHT            
            self.set_exclusive_mouse(True)
            
    def on_resize(self, width, height):        
        # Based on the default with more useful clipping planes
        gl.glViewport(0, 0, width, height)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gl.glOrtho(0, width, 0, height, -1.0, 1000)
        gl.glMatrixMode(gl.GL_MODELVIEW)        
    
    def on_draw(self):
        self.fps_display.draw()
        
    def setup_gl(self):
        """
        Asumming the window has already been created, configure the OpenGL 
        context.
        """        
        # glEnable(GL_DEPTH_TEST)
        glClearDepth(1.0)
        glClearColor(0.1, 0.1, 0.1, 1.0)
        glEnable(GL_BLEND)        
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_LINE_SMOOTH)
                
    def run(self):
        """
        Setup the environment and run with it.
        """
        pyglet.options['debug_gl'] = False
        self.setup_gl()
        self.switch(states.title.Title)
        pyglet.app.run()