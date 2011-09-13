class Weapon(object):
    
    def __init__(self, xy=None):
        self.xy = xy
        self.ticks = None
        self.engaged = False

    def engage(self):
        self.engaged = True

    def disengage(self):
        self.engaged = False

    def update(self, dt):
        if self.engaged and not self.ticks: # we started shootin
            self.ticks = dt
        elif not self.engaged and self.ticks: # everything was dead
            self.ticks = None
        elif self.ticks: # things were still living
            self.ticks += dt
