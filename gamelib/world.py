import pyglet
import vector
import data

from gamelib.enemies import base

class World(object):
    """
    World object contains world geometry and tells game whats up
    """

    def __init__(self, border_name, game, name="VOID"):
        self.game = game
        self.countdown = 120
        self.name = name

        self.width = 1600
        self.height = 1600
        self.center = vector.Vec2d(self.width/2, self.height/2)
        self.radius = 600
        
        self.borders = [vector.Vec2d(*v) for v in 
                            data.worlds[border_name].paths[0].path[0]]

    def valid_location(self, v):
        valid = False
        return valid

    def ai(self, game):

        if len(filter(lambda r: r.alive, self.game.robots)) == 0:
            pyglet.clock.schedule_once(lambda dt: game.next_wave(), 0.0)
        
        
    def update(self, dt):

        pass


