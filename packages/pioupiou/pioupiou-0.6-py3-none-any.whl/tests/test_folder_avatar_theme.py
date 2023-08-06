import hashlib
import os
import typing

from PIL import Image
from PIL import ImageChops
import pytest

from pioupiou import FolderAvatarTheme
from pioupiou.chooser import HashLibChooser


class TestFolderAvatarTheme(object):
    @pytest.mark.parametrize(
        "folder_path, layers_name, token, saved_file_path, compared_image_path, height, width",
        [
            (
                "sample/cat_revoy",
                ["body", "fur", "eyes", "mouth", "accessorie"],
                "just a random string",
                "/tmp/saved_cat_avatar.png",
                "tests/test_img/saved_cat_avatar.png",
                256,
                256,
            ),
            (
                "sample/bird_revoy",
                ["tail", "hoop", "body", "wing", "eyes", "bec", "accessorie"],
                "just a random string",
                "/tmp/saved_bird_avatar.png",
                "tests/test_img/saved_bird_avatar.png",
                256,
                256,
            ),
            (
                "sample/monster_id",
                ["legs", "hair", "arms", "body", "eyes", "mouth"],
                "just a random string",
                "/tmp/saved_monster_avatar.png",
                "tests/test_img/saved_monster_avatar.png",
                120,
                120,
            ),
        ],
    )
    def test_avatar_generation_on_disk_default_random_chooser(
        self,
        folder_path: str,
        layers_name: typing.List[str],
        token: str,
        saved_file_path: str,
        compared_image_path: str,
        height: int,
        width: int,
    ):
        theme = FolderAvatarTheme(folder_path=folder_path, layers_name=layers_name)
        avatar = theme.generate_avatar(token=token)
        theme.save_on_disk(avatar, path=saved_file_path)
        assert os.path.exists(saved_file_path) is True
        assert os.path.getsize(saved_file_path) > 0
        with Image.open(saved_file_path) as avatar:
            assert avatar.height == height
            assert avatar.width == width
            # INFO - G.M - 06/07/2019 - Image should be exactly same as processed one in tests
            with Image.open(compared_image_path) as compared_avatar:
                diff = ImageChops.difference(avatar, compared_avatar)
                assert not diff.getbbox()

    @pytest.mark.parametrize(
        "folder_path, layers_name, token, saved_file_path, compared_image_path, height, width",
        [
            (
                "sample/cat_revoy",
                ["body", "fur", "eyes", "mouth", "accessorie"],
                "just a random string",
                "/tmp/saved_cat_avatar.png",
                "tests/test_img_sha256/saved_cat_avatar.png",
                256,
                256,
            ),
            (
                "sample/bird_revoy",
                ["tail", "hoop", "body", "wing", "eyes", "bec", "accessorie"],
                "just a random string",
                "/tmp/saved_bird_avatar.png",
                "tests/test_img_sha256/saved_bird_avatar.png",
                256,
                256,
            ),
            (
                "sample/monster_id",
                ["legs", "hair", "arms", "body", "eyes", "mouth"],
                "just a random string",
                "/tmp/saved_monster_avatar.png",
                "tests/test_img_sha256/saved_monster_avatar.png",
                120,
                120,
            ),
        ],
    )
    def test_avatar_generation_on_disk__sha256_chooser(
        self,
        folder_path: str,
        layers_name: typing.List[str],
        token: str,
        saved_file_path: str,
        compared_image_path: str,
        height: int,
        width: int,
    ):
        chooser = HashLibChooser(hash_algorithm=hashlib.sha256())
        theme = FolderAvatarTheme(folder_path=folder_path, layers_name=layers_name, chooser=chooser)
        avatar = theme.generate_avatar(token=token)
        theme.save_on_disk(avatar, path=saved_file_path)
        assert os.path.exists(saved_file_path) is True
        assert os.path.getsize(saved_file_path) > 0
        with Image.open(saved_file_path) as avatar:
            assert avatar.height == height
            assert avatar.width == width
            # INFO - G.M - 06/07/2019 - Image should be exactly same as processed one in tests
            with Image.open(compared_image_path) as compared_avatar:
                diff = ImageChops.difference(avatar, compared_avatar)
                assert not diff.getbbox()
