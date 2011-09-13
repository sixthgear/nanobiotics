import pyglet
import rabbyt
import vector
import obj
import data

class BulletPool(object):
    """
    Holds and reuses a list of bullets
    """
    initial_size = 120
    
    def __init__(self):
        self.n = self.__class__.initial_size
        self.bullets = [Bullet(0,0,0,0) for b in range(self.n)]
        self.active = []
                
    def fire(self, x, y, vx, vy, group=0):
        if self.n == 0: self.recycle()        
        b = self.bullets.pop()
        self.n -= 1
        b.activate(x, y, vx, vy, group)
        self.active.append(b)
                
    def recycle(self):
        print 'bullets recycled!'
        self.active = [b for b in self.active if b.alive]
        self.n = self.__class__.initial_size
        self.bullets = [Bullet(0,0,0,0) for b in range(self.n)]
                
    def update(self):
        for b in self.active:
            if not b.alive: continue
            b.pos.x += b.vel.x
            b.pos.y += b.vel.y
            b.sprite.xy = b.pos.x, b.pos.y
            
    def clear(self):
        self.active = []
        self.bullets = []
        self.__init__()
        
    def draw(self):
        # BulletPool.batch.draw()
        pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
        pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE)
        rabbyt.render_unsorted([b.sprite for b in self.active if b.alive])
        # for b in (b for b in self.active if b.alive):
        #     b.render()
            
class Bullet(obj.GameObject):
    
    width = 4
    height = 4
    
    def __init__(self, x, y, vx, vy, group=0):
        super(Bullet,self).__init__(data.bullet, x, y, vx, vy)
        self.alive = False
            
    def activate(self, x, y, vx, vy, group=0):
        if group == 0:
            self.sprite.texture = data.bullet
        else:
            self.sprite.texture = data.bullet
        
        self.pos.x, self.pos.y = x, y
        self.vel.x, self.vel.y = vx, vy
        self.sprite.rot = -self.vel.angle
        self.group = group
        self.alive = True
            
    def die(self):
        self.alive = False


pool = BulletPool()