import pytest
import sys

sys.path.insert(0, "..\\main")
from field_pixel import field_pixel
from football_field import football_field

working_football_field_1yd=football_field((10, 20), (5, 25), 1)
working_football_field_half_yd=football_field((10, 20), (5, 25), 0.5)


def test_assignment():

    assert working_football_field_1yd.xlims==(10, 20)
    assert type(working_football_field_1yd.xlims) is tuple
    assert working_football_field_1yd.ylims==(5, 25)
    assert type(working_football_field_1yd.ylims) is tuple
    assert working_football_field_1yd.pixel_length==1
    assert type(working_football_field_1yd.pixel_length) is int


    assert working_football_field_half_yd.pixel_length==0.5
    assert type(working_football_field_half_yd.pixel_length) is float


def test_field_pixels():
    working_football_field_1yd.set_field_pixels()
    working_football_field_half_yd.set_field_pixels()
    
    assert type(working_football_field_1yd.field_pixels[0]) is field_pixel
    assert type(working_football_field_1yd.field_pixels[19]) is field_pixel
    assert type(working_football_field_half_yd.field_pixels[0]) is field_pixel
    assert type(working_football_field_half_yd.field_pixels[50]) is field_pixel

    assert len(working_football_field_1yd.field_pixels) == 200
    assert len(working_football_field_half_yd.field_pixels) == 800


    assert working_football_field_1yd.field_pixels[199].center==(19.5, 24.5)
    assert working_football_field_half_yd.field_pixels[799].center==(19.75, 24.75)



non_divisible_field=football_field((1.3, 10), (1.3, 10), 0.5)

def test_non_divisivble_field():
    with pytest.raises(ValueError, match="Limits must be perfectly divisible by the pixel_length") :
<<<<<<< HEAD
        non_divisible_field.set_field_pixels()
=======
        non_divisible_field.set_field_pixels()
>>>>>>> 5ef4ecb17b8d764a53b9887d6c7311d4106bf3d7
