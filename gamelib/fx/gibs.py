import pyglet
import random
import math

import lepton
import lepton.controller
import lepton.emitter
import lepton.renderer
import lepton.texturizer

blood_tex = pyglet.resource.texture('blood.png')

class Gibber(object):
    """A Class used to be bloody."""
        
    def __init__(self):
        
        self.particles = lepton.ParticleGroup(
        	controllers=[
                lepton.controller.Gravity((0,-400,0)),
                lepton.controller.Lifetime(0.75),
                lepton.controller.Movement(damping=0.90),
                lepton.controller.Fader(
                    fade_out_start=0.5, 
                    fade_out_end=0.75
                ),
        	],
        	renderer=lepton.renderer.BillboardRenderer(
        	    lepton.texturizer.SpriteTexturizer(blood_tex.id))
        )
          
        self.emitter = lepton.emitter.StaticEmitter(
            template=lepton.Particle(
                position=(0,0,0), 
                color=(1,1,1)),
            deviation=lepton.Particle(
                position=(1,1,0), 
                velocity=(600,600,0), 
                age=0.25),
            size=[
                (12,12,0), 
                (8,8,0), 
                (4,4,0)
            ]
        )
        
    def explode(self, x, y, size=16.0, color=(1,1,1)):
        self.emitter.template.position = (x,y,0)
        self.emitter.template.color = color
        self.emitter.emit(96, self.particles)
        
    def update(self, dt):        
        self.particles.update(dt)
        
    def draw(self):        
        self.particles.draw()
