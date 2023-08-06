class PiouPiouException(Exception):
    pass


class ImageGivenShouldHaveAlphaLayer(PiouPiouException):
    pass


class UnsupportedImageMode(PiouPiouException):
    pass
