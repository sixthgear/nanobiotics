import lepton
import bubbles
import explosion
import gibs

exploder = explosion.Exploder()
gibber = gibs.Gibber()
# bubbler = bubbles.Bubbler()

effects = [
    exploder,
    gibber
]
 
def clear():
    effects = []
    exploder = explosion.Exploder()
    gibber = gibs.Gibber()
    effects = [
        exploder,
        gibber
    ]
    

def update(dt):
    # lepton.default_system.update(dt)
    for e in effects: e.update(dt)

def draw():
    for e in effects: e.draw()
    
clear()