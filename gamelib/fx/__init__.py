import lepton
import bubbles
import explosion
import gibs

exploder = explosion.Exploder()
gibber = gibs.Gibber()
# bubbler = bubbles.Bubbler()

effects = [
    gibber,
    exploder,
]
 
def clear():
    effects = []
    exploder = explosion.Exploder()
    gibber = gibs.Gibber()
    effects = [
        gibber,
        exploder,
    ]
    

def update(dt):
    # lepton.default_system.update(dt)
    for e in effects: e.update(dt)

def draw():
    for e in effects: e.draw()
    
clear()