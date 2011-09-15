import random
import math

import pyglet
from pyglet.gl import *

from gamelib import data

from lepton import Particle, ParticleGroup, default_system
from lepton.renderer import BillboardRenderer
from lepton.texturizer import SpriteTexturizer
from lepton.emitter import StaticEmitter
from lepton.controller import Gravity, Lifetime, Movement, Fader, ColorBlender, Growth

from gamelib.constants import *


blood_tex  = pyglet.resource.texture('blood.png')

class Gibber(object):
    """A Class used to bloody up the place."""
    
    # sound = pyglet.resource.media('explode.wav', streaming=False)
    
    def __init__(self):
                
        self.blood = ParticleGroup(
          controllers=[
              # Gravity((0,-240,0)),
              Lifetime(0.3),
              Movement(damping=0.8),
              Fader(fade_out_start=0.2, fade_out_end=0.3),
          ],
          renderer=BillboardRenderer(SpriteTexturizer(blood_tex.id)))
        
        self.blooder = StaticEmitter(
          template=Particle(
              position=(0,0,0), 
              color=(1,1,1)),
          deviation=Particle(
              position=(1,1,0), 
              velocity=(400,400,0), 
              age=1.5),
          size=[(12,12,0), (8,8,0), (4,4,0)])
                       
    def explode(self, x, y, size=16.0, color=(1,1,1)):
        self.blooder.template.position = (x,y,0)
        self.blooder.template.color = color
        self.blooder.emit(100, self.blood)
        # self.__class__.sound.play()
        
    def update(self, dt):
        # default_system.update(dt)        
        self.blood.update(dt)
        
    def draw(self):        
        glPushAttrib(GL_ALL_ATTRIB_BITS)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE)
        self.blood.draw()
        # self.fire.draw()        
        glPopAttrib()
        

