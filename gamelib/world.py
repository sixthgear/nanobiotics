import pyglet
import vector

from gamelib.enemies import base

class World(object):
    """
    World object contains world geometry and tells game whats up
    """

    def __init__(self, svg, game, name="VOID"):
        self.game = game
        self.countdown = 120
        self.name = name

        if svg:
            self.borders = [vector.Vec2d(*v) for v in svg.paths[0].path[0]]

    def valid_location(self, v):
        valid = False
        return valid

    def ai(self, game):

        if len(filter(lambda r: r.alive, self.game.robots)) == 0:
            pyglet.clock.schedule_once(lambda dt: game.next_wave(), 0.0)
        
        
    def update(self, dt):

        pass


