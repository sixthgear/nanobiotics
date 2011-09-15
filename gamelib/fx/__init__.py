import explosion
import gibs
# import score 
# import fire
# import beast

exploder = explosion.Exploder()
gibber = gibs.Gibber()
# pointer = score.Pointer()
# firer = fire.Firer()
# globber = beast.Beast()
effects = [
    exploder,
    gibber,
    # pointer,
    # firer,
    # globber
]

def clear():
    # del exploder
    # del pointer
    # del firer
    # del globber    
    effects = []
    exploder = explosion.Exploder()
    gibber = gibs.Gibber()
    # pointer = score.Pointer()
    # firer = fire.Firer()
    # globber = beast.Beast()
    effects = [
        exploder,
        gibber
        # pointer,
        # firer,
        # globber
    ]
    

def update(dt):
    for e in effects: e.update(dt)

def draw():
    for e in effects: e.draw()
    
clear()