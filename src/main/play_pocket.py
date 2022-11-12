"""
This is going to how we do the "usable pocket" analysis, I think

Outstanding Items


[] Should I right-away convert the "center" square into a field_square object?
|-- Pro: Can keep track of it
|-- Cons: If we don't use it, then its just adding extra stuff to the code
"""

class play_pocket(football_field):

    def __init__(self, 
                football_starting_coordinates, side_length, offenceDirection, 
                gameId, playId):
        
        if type(football_starting_coordinates) is not tuple:
            raise TypeError("football_starting_coordinates must be a tuple of the form (x,y)")
            
        if offenceDirection not in ["left", "right"]:
            raise ValueError("offensive direction must be either 'left' or 'right'")

        self.football_starting_coordinates=football_starting_coordinates
        self.offenceDirection=offenceDirection.lower()
        self.gameId=gameId
        self.playId=playId
        self.side_length=side_length
        self.pocket_square_center=find_center_of_square_containing(self.football_starting_coordinates, side_length)

    def set_pocket_limits(self, pocket_depth, pocket_width):
        """ Pocket_depth is the x value, because it goes towards the endzone (i.e. the x-value)
        """
        # X-Values -- Depends on which direction the offense is going
        if self.offenceDirection=="left":
            self.xlims=(self.pocket_square_center[0], self.pocket_square_center[0]+pocket_depth)
        elif self.offenceDirection=="right":
            self.xlims=(self.pocket_square_center[0]-pocket_depth, self.pocket_square_center[0])
        else:
            raise ValueError("Offense Direction must be either 'left' or 'right'")
        # Y-Values are independent of the play direction
        self.ylims=(self.pocket_square_center[1]-pocket_width/2, self.pocket_square_center[1]+pocket_width/2)