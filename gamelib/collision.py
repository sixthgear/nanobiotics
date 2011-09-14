import math
    
def point_to_AABB(a_x, a_y, b_x, b_y, b_width, b_height):
    if a_x < b_x: return False
    if a_x > b_x + b_width: return False
    if a_y < b_y: return False
    if a_y > b_y + b_height: return False
    return True
    
def circle_to_AABB(a_x, a_y, a_radius, b_x, b_y, b_width, b_height):
    #todo: this needs to handle collisions with vertecies better
    # test for voroni regions
    if a_x + a_radius < b_x: return False
    if a_x - a_radius > b_x + b_width: return False
    if a_y + a_radius < b_y: return False
    if a_y - a_radius > b_y + b_height: return False
    
    return True    
    
def AABB_to_AABB(a_x, a_y, a_width, a_height, b_x, b_y, b_width, b_height):
    if a_x > b_x + b_width: return False
    if b_x > a_x + a_width: return False
    if a_y > b_y + b_height: return False
    if b_y > a_y + a_height: return False
    return True
            
def circle_to_circle(a_x, a_y, a_radius, b_x, b_y, b_radius):
    return (a_x - b_x) ** 2 + (a_y - b_y) ** 2 < (a_radius + b_radius) ** 2