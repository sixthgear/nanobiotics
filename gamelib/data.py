"""
Please forgive me.
"""

import pyglet
from libs.squirtle import svg

pyglet.resource.path = ['data']
pyglet.resource.reindex()

pyglet.resource.add_font('DYLOVASTUFF.ttf')
pyglet.font.load('DYLOVASTUFF')

spritesheet = pyglet.image.ImageGrid(pyglet.resource.image('sprites.png'),8,8).get_texture_sequence()
for sprite in spritesheet:
    sprite.anchor_x = sprite.width // 2 
    sprite.anchor_y = sprite.height // 2 

bullet = pyglet.resource.image('bullet.png')
bullet.anchor_x = bullet.width // 2
bullet.anchor_y = bullet.height // 2

#background = pyglet.resource.image('stage_1_background.png')
#background.anchor_x = background.width // 2
#background.anchor_y = background.height // 2

boss_hud = []
boss_hud.append(pyglet.resource.image('boss-trim.png'))
boss_hud.append(pyglet.resource.image('boss-health.png'))
boss_hud[0].anchor_x = boss_hud[0].width // 2 
boss_hud[0].anchor_y = boss_hud[0].height // 2 
    
def load_virus(name):
    """
    Get a list of virus textures.
    """
    img = pyglet.resource.image('v_%s.png' % name)
    seq = []
    seq += pyglet.image.ImageGrid(img.get_region(0,0,64,256), 4, 1).get_texture_sequence()
    # tgrid = pyglet.image.TextureGrid(igrid)    
    seq += pyglet.image.ImageGrid(img.get_region(64,64,96,192), 2, 1).get_texture_sequence()
    return seq

def load_boss(name, rows, columns):
    """
    Bosses have a custom amount of frames, because we like to make life
    interesting.
    """

    img = pyglet.resource.image('b_%s.png' % name)
    seq = pyglet.image.ImageGrid(img.get_region(0,0,rows*512,columns*512), 
                                 rows, columns).get_texture_sequence()

    return seq    


cursor = spritesheet[7]

bosses = {
            "stomach": load_boss("slug", 2, 2),
            "heart":   load_boss("heart", 2, 3),
            "brain":   load_boss("worm",2, 2)
}

worlds = {"stomach": svg.SVG("data/stomach.svg")}

