import pyglet
import random
import math

import lepton
import lepton.controller
import lepton.emitter
import lepton.renderer
import lepton.texturizer
import lepton.domain

blood_tex = pyglet.resource.texture('blood.png')

class Gibber(object):
    """A Class used to be bloody."""
        
    def __init__(self):
        
        # self.target = lepton.domain.Point((800,800,0))
        
        self.particles = lepton.ParticleGroup(
        	controllers=[
                lepton.controller.Gravity((0,-50,0)),
                lepton.controller.Growth(-1),
                # lepton.controller.Magnet(self.target, 15000.0),
                lepton.controller.Lifetime(3),
                lepton.controller.Movement(damping=0.94),
                lepton.controller.Fader(
                    fade_out_start=0.5, 
                    fade_out_end=3
                ),
        	],
        	renderer=lepton.renderer.BillboardRenderer(
        	    lepton.texturizer.SpriteTexturizer(blood_tex.id))
        )
          
        self.emitter = lepton.emitter.StaticEmitter(
            template=lepton.Particle(
                position=(0,0,0), 
                color=(1,1,1),                
            ),
            # velocity=lepton.domain.Disc((0,0,0), (0,0,1), 400, 400),
                
            deviation=lepton.Particle(
                position=(1,1,0), 
                velocity=(400,400,0), 
                age=2),
            size=[
                (12,12,0), 
                (8,8,0), 
                (4,4,0)
            ]
        )
        
    def explode(self, x, y, size=16.0, color=(1,1,1)):
        self.emitter.template.position = (x,y,0)
        self.emitter.template.color = color
        self.emitter.emit(108, self.particles)
        
    def update(self, dt):        
        self.particles.update(dt)
        
    def draw(self):        
        pyglet.gl.glPushAttrib(pyglet.gl.GL_ALL_ATTRIB_BITS)
        pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
        pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE)
        self.particles.draw()
        pyglet.gl.glPopAttrib()
        
        
