import vector
import math
    
def point_to_AABB(a, b, b_width, b_height):
    if a.x < b.x: return False
    if a.x > b.x + b_width: return False
    if a.y < b.y: return False
    if a.y > b.y + b_height: return False
    return True
    
def circle_to_AABB(a, a_radius, b, b_width, b_height):
    #todo: this needs to handle collisions with vertecies better
    # test for voroni regions
    if a.x + a_radius < b.x: return False
    if a.x - a_radius > b.x + b_width: return False
    if a.y + a_radius < b.y: return False
    if a.y - a_radius > b.y + b_height: return False
    
    return True    
    
def AABB_to_AABB(a, a_width, a_height, b, b_width, b_height):
    if a.x > b.x + b_width: return False
    if b.x > a.x + a_width: return False
    if a.y > b.y + b_height: return False
    if b.y > a.y + a_height: return False
    return True
            
def circle_to_circle(a, a_radius, b, b_radius):
    return (a.x - b.x) ** 2 + (a.y - b.y) ** 2 < (a_radius + b_radius) ** 2
    
def inv_circle_to_circle(a, a_radius, b, b_radius):
    return (a.x - b.x) ** 2 + (a.y - b.y) ** 2 > abs(a_radius - b_radius) ** 2    