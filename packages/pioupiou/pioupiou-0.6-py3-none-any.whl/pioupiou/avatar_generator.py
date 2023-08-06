from abc import abstractmethod
import glob
import logging
import random
import typing

from PIL import Image

from pioupiou.chooser import Chooser
from pioupiou.exceptions import ImageGivenShouldHaveAlphaLayer
from pioupiou.exceptions import UnsupportedImageMode
from pioupiou.utils import generate_name

LAYER_FILE_IMAGE_PATTERN = "{folder_path}/{layer_name}_[0-9]*.png"
PILLOW_ALPHA_MODES = ["RGBA", "LA", "RGBa"]
LOGGER_NAME = "pioupiou"

try:
    from typing import Protocol
except ImportError:
    from typing_extensions import Protocol  # type: ignore

# High Level generator


class AvatarGeneratorInterface(Protocol):
    name: str

    @abstractmethod
    def generate_avatar(self, token: str) -> Image:
        pass

    @abstractmethod
    def save_on_disk(self, avatar: Image, path: str) -> str:
        pass


class AvatarGenerator(AvatarGeneratorInterface):
    def __init__(
        self,
        themes: typing.List[AvatarGeneratorInterface],
        theme_chooser: Chooser = random.Random(),
        name: str = None,
    ):
        assert themes
        self.themes = {}  # type: typing.Dict[str, AvatarGeneratorInterface]
        self.name = name or generate_name()
        self.theme_chooser = theme_chooser
        for theme in themes:
            self.themes[theme.name] = theme

    def generate_avatar(self, token: str, theme_name: typing.Optional[str] = None) -> Image:
        if theme_name:
            avatar_theme = self.themes[theme_name]
        else:
            for themes in self.themes:
                seed = "{}-{}-{}".format(
                    token, self.name, "-".join([theme_name for theme_name in self.themes.keys()])
                )
                self.theme_chooser.seed(seed)
            avatar_theme = self.theme_chooser.choice(tuple(self.themes.values()))
        return avatar_theme.generate_avatar(token)

    def save_on_disk(self, avatar: Image, path: str) -> str:
        """
        Save avatar on disk
        :param avatar: image of avatar to save
        :param path: path where image should be saved
        :return: path of image saved, same as path given in entry
        """
        avatar.save(path)
        return path


# Low level Theme generation


class Layer(object):
    def __init__(self, level: int, variation_images_paths: typing.List[str], name: str):
        """
         An layer is a part of an avatar theme, a layer
        :param variation_images_paths: paths of different images possible for this layer, a
        layer as differents image variations
        :param level: level of layer, higher mean image will apply be over others.
        :param images: path of image
        """
        self.level = level
        self.variations_images_paths = variation_images_paths
        self.name = name

    def get_random_image(
        self, chooser: Chooser = random.Random(), allow_no_alpha_layer: bool = False
    ) -> Image:
        """Get random image from layer based on current seed"""
        assert self.variations_images_paths
        chosen_path = chooser.choice(self.variations_images_paths)
        logging.getLogger(LOGGER_NAME).debug(
            'open "{}" for layer "{}" of level "{}"'.format(chosen_path, self.name, self.level)
        )
        image = Image.open(chosen_path)
        # INFO - GM - 03/07/2019 - We do not support image without alpha layer unless
        if image.mode not in PILLOW_ALPHA_MODES:
            if not allow_no_alpha_layer:
                raise ImageGivenShouldHaveAlphaLayer(
                    "This image  doesn't contain alpha layer but this layer is required"
                    "to process correctly this layer"
                )
            else:
                if image.mode == "RGB":
                    image = image.convert("RGBA")
                elif image.mode == "LA":
                    image = image.convert("L")
                else:
                    raise UnsupportedImageMode(
                        "the mode {} of this image is unsupported".format(image.mode)
                    )
        return image


class AvatarTheme(AvatarGeneratorInterface):
    def __init__(
        self,
        layers: typing.List[Layer],
        chooser: typing.Optional[Chooser] = None,
        name: typing.Optional[str] = None,
    ):
        self.layers = layers
        self.chooser = chooser or random.Random()
        self.name = name or generate_name()

    def generate_avatar(self, token: str) -> Image:
        """
        Generate avatar Image by obtaining layer and applying them
        :param token: token used as seed to decide layer variation to use.
        """
        sorted_layers = sorted(self.layers, key=lambda x: x.level)
        self.chooser.seed(token + sorted_layers[0].name)
        current_image = sorted_layers[0].get_random_image(
            allow_no_alpha_layer=True, chooser=self.chooser
        )
        for layer in sorted_layers[1:]:
            self.chooser.seed(token + layer.name)
            current_image = Image.alpha_composite(
                current_image, layer.get_random_image(chooser=self.chooser)
            )
        return current_image

    def save_on_disk(self, avatar: Image, path: str) -> str:
        """
        Save avatar on disk
        :param avatar: image of avatar to save
        :param path: path where image should be saved
        :return: path of image saved, same as path given in entry
        """
        avatar.save(path)
        return path


class FolderAvatarTheme(AvatarTheme):
    """
    Theme based on folder allowing easy setup of theme.
    """

    def __init__(
        self,
        folder_path: str,
        layers_name: typing.List[str],
        chooser: Chooser = None,
        name: typing.Optional[str] = None,
    ):
        """

        :param folder_path: path of folder where different layers are available
        :param layers_name: name of layers, order is important to decide which layer is over which. last layers are
        put over previous one.
        """
        self.folder_path = folder_path
        self.layers_name = layers_name
        layers = []
        for layer_number, layer_name in enumerate(layers_name):
            file_list = sorted(
                glob.glob(
                    LAYER_FILE_IMAGE_PATTERN.format(
                        folder_path=self.folder_path, layer_name=glob.escape(layer_name)
                    )
                )
            )
            assert file_list
            layers.append(
                Layer(level=layer_number, variation_images_paths=file_list, name=layer_name)
            )
        assert layers
        super().__init__(layers, chooser, name=name)
