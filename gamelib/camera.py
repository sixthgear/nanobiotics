from gamelib import constants
from gamelib import vector

class Camera(vector.Vec2d):
    
    def __init__(self, world, x, y):
        super(Camera, self).__init__(x, y)
        self.world = world
        self.bounds_x = world.width - constants.WIDTH
        self.bounds_y = world.height - constants.HEIGHT
        
    def update(self, target, dt=0):
        player_norm = vector.Vec2d(target.x / self.world.width, target.y / self.world.height)
        target_x = max(0, min(self.bounds_x * player_norm.x, self.bounds_x))
        target_y = max(0, min(self.bounds_y * player_norm.y, self.bounds_y))
        
        if (target_x - self.x) ** 2 + (target_y - self.y) ** 2 > 144:
            self.x += (target_x - self.x) * 0.1
            self.y += (target_y - self.y) * 0.1
        else:
            self.x = target_x
            self.y = target_y
