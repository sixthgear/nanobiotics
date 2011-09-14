import explosion
# import score 
# import fire
# import beast

exploder = explosion.Exploder()
# pointer = score.Pointer()
# firer = fire.Firer()
# globber = beast.Beast()
effects = [
    exploder,
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
    # pointer = score.Pointer()
    # firer = fire.Firer()
    # globber = beast.Beast()
    effects = [
        exploder,
        # pointer,
        # firer,
        # globber
    ]
    

def update(dt):
    for e in effects: e.update(dt)

def draw():
    for e in effects: e.draw()
    
clear()