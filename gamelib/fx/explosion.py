import random
import math

import pyglet
from pyglet.gl import *

from lepton import Particle, ParticleGroup, default_system
from lepton.renderer import BillboardRenderer
from lepton.texturizer import SpriteTexturizer
from lepton.emitter import StaticEmitter
from lepton.controller import Gravity, Lifetime, Movement, Fader, ColorBlender, Growth

from gamelib.constants import *

fire_tex = pyglet.resource.texture('puff.png')
spark_tex = pyglet.resource.texture('flare1.png')

class Exploder(object):
    """A Class used to splode stuff up."""
    
    # sound = pyglet.resource.media('explode.wav', streaming=False)
    
    def __init__(self):
        
        self.fire = ParticleGroup(
        	controllers=[
        		Lifetime(0.5),
        		Movement(damping=0.96),
        		Growth(20),
        		Fader(fade_in_start=0, start_alpha=0, fade_in_end=0.1, max_alpha=1.0, 
        			fade_out_start=0.25, fade_out_end=0.5)
        	],
        	renderer=BillboardRenderer(SpriteTexturizer(fire_tex.id)))

        self.firer = StaticEmitter(
        	template=Particle(
        		position=(0,0,0), 
        		size=(80,80,0)),
        	deviation=Particle(
        		position=(10,10,0), 
        		velocity=(60,60,0), 
        		size=(15,15,0),
                # up=(0,0,math.pi*2), 
                # rotation=(0,0,math.pi*0.06),
                # age=2,
        		),
        	color=[(0.5,0,0), (0.5,0.5,0.5), (0.4,0.1,0.1), (0.85,0.3,0)],
        )
        
        self.sparks = ParticleGroup(
          controllers=[
              # Gravity((0,-240,0)),
              Lifetime(2),
              Movement(damping=0.97),
              Fader(fade_out_start=1.5, fade_out_end=2.0),
          ],
          renderer=BillboardRenderer(SpriteTexturizer(spark_tex.id)))
        
        self.sparker = StaticEmitter(
          template=Particle(
              position=(0,0,0), 
              color=(1,1,1)),
          deviation=Particle(
              position=(1,1,0), 
              velocity=(400,400,0), 
              age=1.5),
          size=[(5,5,0), (6,6,0), (7,7,0)])
                       
    def explode(self, x, y, size=1.0, color=(1,1,1)):
        self.firer.template.position = (x,y,0)
        self.firer.emit(16, self.fire)        
        # self.sparker.template.position = (x,y,0)
        # self.sparker.template.color = color
        # self.sparker.emit(4, self.sparks)
        # self.__class__.sound.play()
        
    def update(self, dt):
        # default_system.update(dt)        
        self.fire.update(dt)
        self.sparks.update(dt)
        
    def draw(self):        
        glPushAttrib(GL_ALL_ATTRIB_BITS)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE)
        self.sparks.draw()
        self.fire.draw()        
        glPopAttrib()
        

