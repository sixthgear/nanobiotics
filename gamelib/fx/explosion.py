import pyglet
import random
import math

import lepton
import lepton.controller
import lepton.emitter
import lepton.renderer
import lepton.texturizer

fire_tex = pyglet.resource.texture('puff.png')
spark_tex = pyglet.resource.texture('flare1.png')

class Exploder(object):
    """A Class used to splode stuff up."""
    
    # sound = pyglet.resource.media('explode.wav', streaming=False)
    
    def __init__(self):
        
        self.fire = lepton.ParticleGroup(
        	controllers=[
        		lepton.controller.Lifetime(1.50),
        		lepton.controller.Movement(damping=0.91),
                lepton.controller.Growth(10),
        		lepton.controller.Fader(
        		    fade_in_start=0, 
        		    start_alpha=0, 
        		    fade_in_end=0.1, 
        		    max_alpha=1.0, 
        			fade_out_start=0.75, 
        			fade_out_end=1.50
        		)
        	],
        	renderer=lepton.renderer.BillboardRenderer(lepton.texturizer.SpriteTexturizer(fire_tex.id)))

        self.firer = lepton.emitter.StaticEmitter(
        	template=lepton.Particle(
        		position=(0,0,0), 
        		size=(190,190,0)),
        	deviation=lepton.Particle(
        		position=(20,20,0), 
        		velocity=(600,600,0), 
        		size=(40,40,0),
                # up=(0,0,math.pi*2), 
                # rotation=(0,0,math.pi*0.06),
                # age=2,
        		),
        	color=[
        	    (0.5,0,0), 
        	    (0.5,0.5,0.5), 
        	    (0.4,0.1,0.1), 
        	    (0.85,0.3,0)
        	],
        )
        
        self.sparks = lepton.ParticleGroup(
          controllers=[
              # lepton.controller.Gravity((0,-240,0)),
              lepton.controller.Lifetime(1.2),
              lepton.controller.Movement(damping=0.97),
              lepton.controller.Fader(fade_out_start=0.75, fade_out_end=1.2),
          ],
          renderer=lepton.renderer.BillboardRenderer(lepton.texturizer.SpriteTexturizer(spark_tex.id)))
        
        self.sparker = lepton.emitter.StaticEmitter(
            template=lepton.Particle(
                position=(0,0,0), 
                color=(1,1,1)),
            deviation=lepton.Particle(
                position=(1,1,0), 
                velocity=(600,600,0), 
            ),
            size=[(5,5,0), (7,7,0), (10,10,0)]
        )
                       
    def explode(self, x, y, size=1.0, color=(1,1,1)):
        self.firer.template.position = (x,y,0)
        self.firer.emit(120, self.fire)        
        self.sparker.template.position = (x,y,0)
        self.sparker.template.color = color
        self.sparker.emit(120, self.sparks)
        
    def update(self, dt):        
        self.fire.update(dt)
        self.sparks.update(dt)
        
    def draw(self):        
        pyglet.gl.glPushAttrib(pyglet.gl.GL_ALL_ATTRIB_BITS)
        pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
        pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE)
        self.sparks.draw()
        self.fire.draw()        
        pyglet.gl.glPopAttrib()
        

