import math

def find_center_of_square_containing(point, side_length):
    """ 
    going to use math.floor to find the lowest x,y value
    to make this work for side_length of arbitrary length (i.e. non-integer), 
    need to manipulate the value b/c math.floor will only return an integer

    start run into floating-point errors (I think thats whats causing it, at least) when side_length > 0.00005. 
    I think this is ok for our purposes considering 0.00005 yards == 0.0018 inches == 0.04572 milimeters
    limiting factor now would be processing time anyway
    """

    divisor=1/side_length
    x_low=math.floor(point[0]*divisor)/divisor
    y_low=math.floor(point[1]*divisor)/divisor
    
    center=(x_low+side_length/2,
            y_low+side_length/2)

    return center

