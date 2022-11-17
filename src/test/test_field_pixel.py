import pytest
import sys

sys.path.insert(0, "..\\main")
from field_pixel import field_pixel


working_square=field_pixel((10, 10), 1)

def test_assignment():
    
    assert working_square.center==(10, 10)
    assert type(working_square.center) is tuple
    assert working_square.center[0]==10
    assert working_square.pixel_length==1
    assert working_square.pixel_length/2==0.5

def test_correct_square_sides():
    working_square.set_square_corners()

    assert working_square.square_corners == [(9.5, 10.5), (10.5, 10.5), 
                                          (9.5, 9.5),  (10.5, 9.5)] 


