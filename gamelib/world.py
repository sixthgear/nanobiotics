import vector

from gamelib.enemies import base

class World(object):
    """
    World object contains world geometry and tells game whats up
    """

    def __init__(self, svg, game, name="Unknown"):
        self.game = game
        self.countdown = 120
        self.name = name

        if svg:
            self.borders = [vector.Vec2d(*v) for v in svg.paths[0].path[0]]
            print self.borders

    def valid_location(self, v):
        valid = False
        return valid

    def update(self, dt):

        if self.countdown > 0:
            self.countdown -= 1
            return

        self.countdown = 120

        if len(filter(lambda r: r.alive, self.game.robots)) == 0:
            self.game.next_wave()

