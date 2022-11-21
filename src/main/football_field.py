import numpy as np
from field_pixel import field_pixel
<<<<<<< HEAD
from football_field_utils import *
=======
>>>>>>> 5ef4ecb17b8d764a53b9887d6c7311d4106bf3d7



class football_field:
    """
    xlims and ylims are TUPLES that need to be input
    Choosing to set the lims NOT as the center points, but as the entire area of the field that must be covered
    I think it will be more straight forward to feed the data in this way"""
    
    """ One funny thing is that the [0,0] of a matrix is the TOP left, 
    but [0,0] of the field is the BOTTOM left"""
    
    def __init__(self, xlims, ylims, pixel_length, units="yrds"):
        self.xlims=xlims
        self.ylims=ylims
        self.pixel_length=pixel_length
        self.units=units
    
    def set_field_pixels(self):
<<<<<<< HEAD
        """ Switched over to a very small number to avoid floating-point issues in the modulus command """
        if (((self.xlims[1]-self.xlims[0]) % self.pixel_length > 1e-10) 
         or ((self.ylims[1]-self.ylims[0]) % self.pixel_length > 1e-10)):

            raise ValueError((f"Limits must be perfectly divisible by the pixel_length\n \
                               xlims={self.xlims}, ylims={self.ylims}, pixel_length={self.pixel_length}\n \
                               x mod = {(self.xlims[1]-self.xlims[0]) % self.pixel_length} \
                               y mod = {(self.ylims[1]-self.ylims[0]) % self.pixel_length}"))
=======
 
        if (((self.xlims[1]-self.xlims[0]) % self.pixel_length != 0) 
         or ((self.ylims[1]-self.ylims[0]) % self.pixel_length != 0)):
            raise ValueError("Limits must be perfectly divisible by the pixel_length")
>>>>>>> 5ef4ecb17b8d764a53b9887d6c7311d4106bf3d7
 
        x_range=np.arange (self.xlims[0], self.xlims[1], self.pixel_length)
        y_range=np.arange (self.ylims[0], self.ylims[1], self.pixel_length)
        
        field_pixels=[]

        # x,y defines the bottom-left corner    
        for x, y in [(x,y) for x in x_range for y in y_range]:
            center=(x+self.pixel_length/2, y+self.pixel_length/2)
            tmp=field_pixel(center, self.pixel_length)
<<<<<<< HEAD
            tmp.set_pixel_corners()
            field_pixels.append(tmp)

        self.field_pixels=field_pixels
        
=======
            tmp.set_square_corners()
            field_pixels.append(tmp)

        self.field_pixels=field_pixels
>>>>>>> 5ef4ecb17b8d764a53b9887d6c7311d4106bf3d7
