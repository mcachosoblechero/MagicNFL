import numpy as np
from field_square import field_square
from football_field_utils import *


class football_field:
    """
    I know realize this is probably mis-named, since its actualy a football_field_section or something like that
        Should I re-name?
    xlims and ylims are TUPLES that need to be input
    """
    
    def __init__(self, xlims, ylims, side_length, units="yrds"):

        if type(xlims) is not tuple or type(ylims) is not tuple: 
            raise TypeError("xlims and ylims must be a tuple of the form (x,y)")

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

        
