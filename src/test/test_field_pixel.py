import pytest
import sys

sys.path.insert(0, "..\\main")
from field_pixel import field_pixel


working_pixel=field_pixel((10, 10), 1)

def test_assignment():
    
    assert working_pixel.center==(10, 10)
    assert type(working_pixel.center) is tuple
    assert working_pixel.center[0]==10
    assert working_pixel.pixel_length==1
    assert working_pixel.pixel_length/2==0.5

def test_correct_pixel_sides():
    working_pixel.set_pixel_corners()

    assert working_pixel.pixel_corners == [(9.5, 10.5), (10.5, 10.5), 
                                          (9.5, 9.5),  (10.5, 9.5)] 


