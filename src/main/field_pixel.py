<<<<<<< HEAD
=======

>>>>>>> 5ef4ecb17b8d764a53b9887d6c7311d4106bf3d7
class field_pixel:
    def __init__(self, center, pixel_length, units="yds"):
        self.center=center
        self.pixel_length=pixel_length
        self.units=units
        
<<<<<<< HEAD
    def set_pixel_corners(self):
        # I'm not sure if we need this right now, but it might be useful later for charting
        """  
        Calulates the perimeter of the pixel 
=======
    def set_square_corners(self):
        # I'm not sure if we need this right now, but it might be useful later for charting
        """  
        Calulates the perimeter of the square 
>>>>>>> 5ef4ecb17b8d764a53b9887d6c7311d4106bf3d7
            Returns the points as tuples in the following order:
               (x_0, y_0)     (x_1, y_0) 
               
               (x_0, y_1)     (x_1, y_1)  
        """

        x_0=self.center[0]-(self.pixel_length/2)
        x_1=self.center[0]+(self.pixel_length/2)

        y_1=self.center[1]+(self.pixel_length/2)
        y_0=self.center[1]-(self.pixel_length/2)
        
<<<<<<< HEAD
        self.pixel_corners=[(x_0, y_1), (x_1, y_1), 
                             (x_0, y_0), (x_1, y_0)]
=======
        self.square_corners=[(x_0, y_1), (x_1, y_1), 
                             (x_0, y_0), (x_1, y_0)]
    
>>>>>>> 5ef4ecb17b8d764a53b9887d6c7311d4106bf3d7
