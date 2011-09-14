import pyglet
import rabbyt
import vector
import math

class GameObject(object):
    
    width = 0.0
    height = 0.0
    
    def __init__(self, img, x=0.0, y=0.0, vx=0.0, vy=0.0):
                
        self.pos = vector.Vec2d(x, y)
        self.vel = vector.Vec2d(vx, vy)
        self.bounding_radius = self.__class__.width // 2
        self.bounding_radius_squared = self.bounding_radius ** 2
        self.x, self.y = x,y
                
        # rabbyt stuff
        self.sprite = rabbyt.Sprite(img, xy=(x,y))
        # self.x = self.sprite.attrgetter('x')
        # self.y = self.sprite.attrgetter('y')
        self.render = self.sprite.render

    def update(self, dt):
        self.pos += self.vel * dt
        self.sprite.xy = self.pos.x, self.pos.y
        self.x, self.y = self.sprite.xy
        
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
            s.offset_x, s.offset_y = o_x, o_y
            self.sprites.append(s)

        #hax for now, first sprite is main sprite that we use for collision dectection
        self.bounding_radius = self.__class__.width // 2
        self.bounding_radius_squared = self.bounding_radius ** 2
    
    def add_sprite(self, img, offset):
        s = rabbyt.Sprite(img, xy=(self.pos.x + offset[0], 
                                   self.pos.y + offset[1]))
        s.offset_x, s.offset_y = offset
        self.sprites.append(s)

    @property
    def rot(self):
        return self.sprites[0].rot

    @rot.setter
    def rot(self, r):
        self.sprites[0].rot = r
        # for s in self.sprites:
        #     s.rot = v
        
    
    @property
    def x(self): return self.pos.x
        
    @property
    def y(self): return self.pos.y
                            
    def render(self):
        for s in self.sprites:
            s.render()
            
    def update(self, dt):
        #self.pos += self.vel * dt
        if len(self.sprites) > 1:
            angle = math.radians(self.rot)
            sin_a = math.sin(angle)
            cos_a = math.cos(angle)
        
        for i, s in enumerate(self.sprites):
            if i == 0:
                s.xy = self.pos.x + s.offset_x, self.pos.y + s.offset_y
            else:
                s.x = self.pos.x + (s.offset_x * cos_a) - (s.offset_y * sin_a)
                s.y = self.pos.y + (s.offset_y * cos_a) + (s.offset_x * sin_a)
