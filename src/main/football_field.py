import numpy as np
from field_square import field_square



class football_field:
    """
    xlims and ylims are TUPLES that need to be input

    Choosing to set the lims NOT as the center points, but as the entire area of the field that must be covered
    I think it will be more straight forward to feed the data in this way"""
    
    """ One funny thing is that the [0,0] of a matrix is the TOP left, 
    but [0,0] of the field is the BOTTOM left"""
    
    def __init__(self, xlims, ylims, side_length, units="yrds"):
        self.xlims=xlims
        self.ylims=ylims
        self.side_length=side_length
        self.units=units
    
    def set_field_squares(self):
        x_range=np.arange (self.xlims[0], self.xlims[1], self.side_length)
        y_range=np.arange (self.ylims[0], self.ylims[1], self.side_length)
        
        field_squares=[]

        # x,y defines the bottom-left corner    
        for x, y in [(x,y) for x in x_range for y in y_range]:
            center=(x+self.side_length/2, y+self.side_length/2)
            tmp=field_square(center, self.side_length)
            tmp.set_square_corners()
            field_squares.append(tmp)

        self.field_squares=field_squares