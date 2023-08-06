"""Functions to support watermarking."""
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PyWatermark.constants import SIZE_CONSTANTS
from PyWatermark.WExceptions import WatermarkException
from PyWatermark.fontMap import FONT_MAP, AVAILABLE_FONTS
import os
import pkg_resources


def _setSize(width, height, size) -> int:
    baseSize = min(width, height) // 50

    if size not in SIZE_CONSTANTS:
        raise WatermarkException(1, val=size)

    return int(baseSize * SIZE_CONSTANTS[size])


def _setPosition(width, height, textWidth, textHeight, position) -> tuple:
    positionValues = None, None
    if position == "BR":
        positionValues = width - textWidth - width // 100, height - textHeight - height // 100

    elif position == "TR":
        positionValues = width - textWidth - width // 100, height // 100

    elif position == "BL":
        positionValues = width // 100, height - textHeight - height // 100

    elif position == "TL":
        positionValues = width // 100, height // 100

    else:
        raise WatermarkException(0, val=position)

    return positionValues


def waterMarkImages(imageFile,
                    imageOutputPath,
                    text,
                    fontName="Bangers",
                    size="M",
                    opacity=255,
                    position="BR"):
    # TODO : Try to have color as an argument as well
    """
    Watermarks your images based on whatever arguments you've provided.

        Args:
            imageFile(str): Name of the image file
            imageOutputPath(str): Specify the output folder, not the name
            fontName(str): Put the path of the font of your choice,
                            or one of those available
            size(str): Size must be in XS, S, M, L, XL, XXL
            opacity(int): Opacity must be between 0 and 255 (inclusive)
            position(str): Position must be in BR, BL, TR, TL

        Returns:
            str - Filename of your output file

    """
    fileName = imageFile.split(os.path.sep)[-1]
    try:
        photo = Image.open(imageFile).convert("RGBA")
    except IOError:
        raise WatermarkException(4, val=imageFile)

    width, height = photo.size

    COLOR = (255, 255, 255)

    textImage = Image.new('RGBA', (width, height), COLOR + (0, ))

    fontsize = _setSize(width, height, size)

    drawing = ImageDraw.Draw(textImage)

    if fontName in FONT_MAP:
        # * fontPath = "PyWaterMark\\fonts\\" + FONT_MAP[fontName] - ONLY DEVS
        fontPath = pkg_resources.resource_filename(
            'PyWatermark', 'fonts/' + FONT_MAP[fontName])
        if not os.path.isfile(fontPath):
            raise WatermarkException(2, val=fontName)
    else:
        if not os.path.isfile(fontName):
            raise WatermarkException(3, val=fontName)

    font = ImageFont.truetype(fontPath, fontsize)

    textWidth, textHeight = drawing.textsize(text, font)

    pos = _setPosition(width, height, textWidth, textHeight, position)

    drawing.text(pos, text, fill=COLOR + (opacity, ), font=font)

    combined = Image.alpha_composite(photo, textImage)

    filenameSave = fileName.split('.')
    filenameSave[1] = 'wm.png'
    filenameSave = ''.join(filenameSave)
    # * Why you can't store JPEG images with transparency
    # * https://stackoverflow.com/questions/41413956/pil-unable-to-change-the-transparency-level-for-jpeg-image
    combined.save(imageOutputPath + '\\' + filenameSave)

    return filenameSave


def getAvailableFonts():
    """
    Return a list of available fonts.

        Args:
            None
        Returns:
            List of strings
    """
    return list(AVAILABLE_FONTS)
