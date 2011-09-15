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
        self.x = max(0, min(self.bounds_x * player_norm.x, self.bounds_x))
        self.y = max(0, min(self.bounds_y * player_norm.y, self.bounds_y))
