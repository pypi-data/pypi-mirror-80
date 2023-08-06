import pytest

from pioupiou import Layer
from pioupiou.exceptions import ImageGivenShouldHaveAlphaLayer


class TestLayer(object):
    def test_unit__layer__ok__nominal_case(self):
        layer = Layer(
            level=0, name="star", variation_images_paths=["tests/test_img/white_alpha_star.png"]
        )
        image = layer.get_random_image(allow_no_alpha_layer=False)
        assert image.format == "PNG"
        assert image.mode == "RGBA"

    def test_unit__layer__err__image_should_have_alpha_layer(self):
        layer = Layer(
            level=0, name="star", variation_images_paths=["tests/test_img/black_background.png"]
        )
        with pytest.raises(ImageGivenShouldHaveAlphaLayer):
            layer.get_random_image(allow_no_alpha_layer=False)

    def test_unit__layer__err__ok__allow_alpha_laver(self):
        layer = Layer(
            level=0, name="star", variation_images_paths=["tests/test_img/black_background.png"]
        )
        image = layer.get_random_image(allow_no_alpha_layer=True)
        assert image.mode == "RGBA"
