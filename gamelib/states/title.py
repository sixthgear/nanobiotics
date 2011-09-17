import pyglet
from gamelib import data

title = pyglet.resource.image('title.png')

class Title(object):
    
    def __init__(self, window):
        self.window = window
        self.timer = pyglet.clock.schedule_interval(self.update, 1.0/60)
        
        self.music = pyglet.media.Player()

        if pyglet.media.have_avbin:
            self.music.queue(pyglet.resource.media('Theme1_Spacelab.mp3'))
            self.music.play()
            self.music.eos_action = pyglet.media.Player.EOS_LOOP
        else:
            print "Avbin not found, you're going to be missing some awesome music :("
        
        
            
    def update(self, dt):
        pass
        
    def on_draw(self):
        self.window.viewport.begin()
        self.window.clear()        
        title.blit(0,0)
        self.window.viewport.end()
        
    def on_key_press(self, symbol, modifiers):
        pass
        # pyglet.clock.schedule_once(self.window.play, 0.0)
        
    def on_mouse_press(self, x, y, button, modifiers):
        # pyglet.app.exit()
        pyglet.clock.schedule_once(self.window.play, 0.0)