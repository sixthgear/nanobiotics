import pyglet
import vector

class GameObject(pyglet.sprite.Sprite):
    
    width = 0.0
    height = 0.0    
    
    def __init__(self, sprite, x=0.0, y=0.0, vx=0.0, vy=0.0):
        super(GameObject, self).__init__(sprite, x, y)
        self.x, self.y = x,y
        self.pos = vector.Vec2d(x, y)
        self.velocity = vector.Vec2d(vx, vy)
        self.width = self.__class__.width
        self.height = self.__class__.height
        self.bounding_radius = self.__class__.width
        self.bounding_radius_sq = self.__class__.width ** 2
        self.render = self.draw
                    
    def update(self):
        self.pos += self.velocity
        self.x, self.y = self.pos.x, self.pos.y

    def flash(self, duration, rgba=(0,0,0,0), time=None, on=True):
        if time == None: time = duration
        if on:
            self.color = 255,255,255
            self.opacity = 255
        else:
            self.color = rgba[:3]
            self.opacity = rgba[3]
        if time >= 0:
            pyglet.clock.schedule_once(self.flash, 0.125, rgba, time-0.125, not on)
        else:
            self.color = 255,255,255
            self.opacity = 255
