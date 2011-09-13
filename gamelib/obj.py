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
    # img_col = [(img, (offset_x, offset_y)), ...]
    def __init__(self, img_col, x=0.0, y=0.0, vx=0.0, vy=0.0):
        self.pos = vector.Vec2d(x, y)
        self.vel = vector.Vec2d(vx, vy)
        
        # rabbyt stuff
        self.sprites = list()
        for i in img_col:
            o_x, o_y = i[1]
            s = rabbyt.Sprite(i[0], xy=(x + o_x, y + o_y))
            s.offset_x = o_x
            s.offset_y = o_y
            self.sprites.append(s)

        #hax for now, first sprite is main sprite that we use for collision dectection
        self.bounding_radius = self.__class__.width // 2
        self.bounding_radius_squared = self.bounding_radius ** 2
        
    @property
    def x(self): return self.pos.x
        
    @property
    def y(self): return self.pos.y
                            
    def render(self):
        for s in self.sprites:
            s.render()
            
    def update(self, dt):
        #self.pos += self.vel * dt
        for s in self.sprites:
            s.xy = self.pos.x + s.offset_x, self.pos.y + s.offset_y
        
