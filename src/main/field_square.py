
class field_square:
    def __init__(self, center, side_length, units="yds"):
        self.center=center
        self.side_length=side_length
        self.units=units
        
    def set_square_corners(self):
        # I'm not sure if we need this right now, but it might be useful later for charting
        """  
        Calulates the perimeter of the square 
            Returns the points as tuples in the following order:
               (x_0, y_0)     (x_1, y_0) 
               
               (x_0, y_1)     (x_1, y_1)  
        """

        x_0=self.center[0]-(self.side_length/2)
        x_1=self.center[0]+(self.side_length/2)

        y_1=self.center[1]+(self.side_length/2)
        y_0=self.center[1]-(self.side_length/2)
        
        self.square_corners=[(x_0, y_1), (x_1, y_1), 
                             (x_0, y_0), (x_1, y_0)]