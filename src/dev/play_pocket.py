"""
This is going to how we do the "usable pocket" analysis class, I think

Outstanding Items
[] Left/Right Distinction
|-- need some way to determine which way the offense is going. I think this is in the raw data
|-- need to determine how to incorporate/flip the x coords when moving left

[] Should I right-away convert the "center" square into a field_square object?
|-- Pro: Can keep track of it
|-- Cons: If we don't use it, then its just adding extra stuff to the code


"""

class play_pocket(football_field):

    def __init__(self, football_starting_coordinates, offense_direction, gameId, playId, side_length):
        
        if type(football_starting_coordinates) is not tuple:
            raise TypeError("football_starting_coordinates must be a tuple of the form (x,y)")
            
        if offense_direction not in ["left", "right"]:
            raise ValueError("offensive direction must be either 'left' or 'right'")

        self.football_starting_coordinates=football_starting_coordinates
        self.offense_direction=offense_direction.lower()
        self.gameId=gameId
        self.playId=playId
        self.side_length=side_length
    
    def set_pocket_square_senter(self):
        self.pocket_square_center=find_center_of_square_containing(self.football_starting_coordinates, side_length)