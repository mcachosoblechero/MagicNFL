from field_pixel import field_pixel
from football_field_utils import *
from football_field import *

class play_pocket(football_field):

    def __init__(self, 
                football_starting_coordinates, pixel_length, offenseDirection, 
                gameId, playId):
        
        if type(football_starting_coordinates) is not tuple:
            raise TypeError("football_starting_coordinates must be a tuple of the form (x,y)")
            
        if offenseDirection not in ["left", "right"]:
            raise ValueError("offensive direction must be either 'left' or 'right'")

        self.football_starting_coordinates=football_starting_coordinates
        self.offenseDirection=offenseDirection.lower()
        self.gameId=gameId
        self.playId=playId
        self.pixel_length=pixel_length
        self.pocket_square_center=find_center_of_square_containing(self.football_starting_coordinates, pixel_length)

    def set_pocket_limits(self, pocket_depth, pocket_width):
        """ Pocket_depth is the x value, because it goes towards the endzone (i.e. the x-value)
            The football x-coordinate is always the leading edge of the pocket
            The football y-coordinate defines the y-value for the center of its own square
            Adding the 'dangling' square so the entire pocket is contained in this definition 
        """


        # X-Values -- Depends on which direction the offense is going
        needed_x_squares = math.ceil(pocket_depth/self.pixel_length) 
        new_depth=needed_x_squares*self.pixel_length

        if self.offenseDirection=="left":
            xlims=(self.football_starting_coordinates[0], 
                        self.football_starting_coordinates[0]+new_depth)

        elif self.offenseDirection=="right":
            xlims=(self.football_starting_coordinates[0]-new_depth, 
                        self.football_starting_coordinates[0])
        else:
            raise ValueError("Offense Direction must be either 'left' or 'right'")


        # Y-Values are independent of the play direction
        needed_y_squares = math.ceil(pocket_width/self.pixel_length)
        new_width=needed_y_squares*self.pixel_length

        ylims=(self.football_starting_coordinates[1]-new_width/2,
                    self.football_starting_coordinates[1]+new_width/2)

        self.xlims=(round(xlims[0], 3),
                    round(xlims[1], 3))
                    
        self.ylims=(round(ylims[0], 3),
                    round(ylims[1], 3))