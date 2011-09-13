import pyglet
import rabbyt
import vector

class GameObject(object):
    
    width = 0.0
    height = 0.0
    
    def __init__(self, img, x=0.0, y=0.0, vx=0.0, vy=0.0):
                
        self.pos = vector.Vec2d(x, y)
        self.vel = vector.Vec2d(vx, vy)
        self.bounding_radius = self.__class__.width // 2
        self.bounding_radius_squared = self.bounding_radius ** 2
                
        # rabbyt stuff
        self.sprite = rabbyt.Sprite(img, xy=(x,y))
        self.x = self.sprite.attrgetter('x')
        self.y = self.sprite.attrgetter('y')
        self.render = self.sprite.render

    def update(self, dt):
        self.pos += self.vel * dt
        self.sprite.xy = self.pos.x, self.pos.y
        
class CompoundGameObject(GameObject):
    
    def __init__(self, imgs, x=0.0, y=0.0, vx=0.0, vy=0.0):
        self.pos = vector.Vec2d(x, y)
        self.vel = vector.Vec2d(vx, vy)
        self.bounding_radius = self.__class__.width // 2
        self.bounding_radius_squared = self.sprite.bounding_radius ** 2
        
        # rabbyt stuff
        for i in imgs:
            self.sprites = rabbyt.Sprite(i, xy=(x,y))
            s.offset_x = 0
            s.offset_y = 0
        
    @property
    def x(self): return self.pos.x
        
    @property
    def y(self): return self.pos.y
                            
    def render(self):
        for s in self.sprites:
            s.render()
            
    def update(self):
        self.pos += self.vel
        for s in self.sprites:
            s.xy = self.pos.x + s.offset_x, self.pos.y + s.offset_y
        
