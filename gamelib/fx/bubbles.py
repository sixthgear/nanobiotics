import pyglet
import random
import math

import lepton
import lepton.controller
import lepton.emitter
import lepton.renderer
import lepton.texturizer
import lepton.domain

bubble_tex = pyglet.resource.texture('blood.png')

class Bubbler(object):
    """A Class used to bubbly."""
        
    def __init__(self):
        
        self.rate = 0.5
        self.accumulator = 0.0
        
        self.particles = lepton.ParticleGroup(
        	controllers=[
        		lepton.controller.Lifetime(5),
        		lepton.controller.Movement(damping=0.91),
        		lepton.controller.Gravity((0, 200,0)),
                lepton.controller.Growth(3),
        		lepton.controller.Fader(
        			fade_out_start=0, 
        			fade_out_end=5
        		)
        	],
        	renderer=lepton.renderer.BillboardRenderer(
        	    lepton.texturizer.SpriteTexturizer(bubble_tex.id))
        )

        self.emitter = lepton.emitter.StaticEmitter(
            position=lepton.domain.Line((400, 320, 0), (1200, 320, 0)),
        	template=lepton.Particle(
                velocity=(0,10,0),
        		size=(8,8,0),
        		color=(0.11, 0.584,0.258, 0.5)        		
        	),        		
        	deviation=lepton.Particle(
        	    size=(2,2),
        		velocity=(2,1,2), 
                age=2,
        	),
        )
                
    def update(self, dt):
        self.accumulator -= dt
        if self.accumulator < 0:            
            self.emitter.emit(1, self.particles)
            self.accumulator = self.rate
            
        self.particles.update(dt)
        
    def draw(self):        
        self.particles.draw()
