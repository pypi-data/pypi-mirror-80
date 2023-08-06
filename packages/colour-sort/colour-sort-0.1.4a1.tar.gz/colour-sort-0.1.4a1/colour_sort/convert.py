from typing import Protocol

import numpy as np #type: ignore
from skimage import color #type: ignore
import cv2 #type: ignore
from PIL import Image, ImageCms #type: ignore

from colour_sort.colour_space import ColourSpace

class ColourSpaceConverter(Protocol):
    def rgb2lab(self, image: np.ndarray) -> np.ndarray:
        ...
    def rgb2hsv(self, image: np.ndarray) -> np.ndarray:
        ...
    def lab2rgb(self, image: np.ndarray) -> np.ndarray:
        ...
    def lab2hsv(self, image: np.ndarray) -> np.ndarray:
        ...
    def hsv2rgb(self, image: np.ndarray) -> np.ndarray:
        ...
    def hsv2lab(self, image: np.ndarray) -> np.ndarray:
        ...

class Cv2Converter:
    def rgb2lab(self, image: np.ndarray) -> np.ndarray:
        return cv2.cvtColor(image, cv2.COLOR_RGB2LAB)
    def rgb2hsv(self, image: np.ndarray) -> np.ndarray:
        return cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    def lab2rgb(self, image: np.ndarray) -> np.ndarray:
        return cv2.cvtColor(image, cv2.COLOR_LAB2RGB)
    def lab2hsv(self, image: np.ndarray) -> np.ndarray:
        return cv2.cvtColor(image, cv2.COLOR_LAB2HSV)
    def hsv2rgb(self, image: np.ndarray) -> np.ndarray:
        return cv2.cvtColor(image, cv2.COLOR_HSV2RGB)
    def hsv2lab(self, image: np.ndarray) -> np.ndarray:
        return cv2.cvtColor(image, cv2.COLOR_HSV2LAB)

class SkimageConverter:
    def rgb2lab(self, image: np.ndarray) -> np.ndarray:
        return color.rgb2lab(image)
    def rgb2hsv(self, image: np.ndarray) -> np.ndarray:
        return color.rgb2hsv(image)
    def lab2rgb(self, image: np.ndarray) -> np.ndarray:
        return color.lab2rgb(image)
    def lab2hsv(self, image: np.ndarray) -> np.ndarray:
        return color.lab2hsv(image)
    def hsv2rgb(self, image: np.ndarray) -> np.ndarray:
        return color.hsv2rgb(image)
    def hsv2lab(self, image: np.ndarray) -> np.ndarray:
        return color.hsv2lab(image)

class PilConverter:
    __srgb_p = ImageCms.createProfile("sRGB")
    __lab_p  = ImageCms.createProfile("LAB")

    # Convert the image to LAB colour space - https://stackoverflow.com/a/53353542
    def rgb2lab(self, image: np.ndarray) -> np.ndarray:
        im = Image.fromarray(image, mode='RGB')
        rgb2lab = ImageCms.buildTransformFromOpenProfiles(PilConverter.__srgb_p, PilConverter.__lab_p, "RGB", "LAB")
        return np.array(ImageCms.applyTransform(im, rgb2lab))

    def rgb2hsv(self, image: np.ndarray) -> np.ndarray:
        im = Image.fromarray(image, mode='RGB')
        return np.array(im.convert('HSV'))

    def lab2rgb(self, image: np.ndarray) -> np.ndarray:
        im = Image.fromarray(image, mode='LAB')
        rgb2lab = ImageCms.buildTransformFromOpenProfiles(PilConverter.__lab_p, PilConverter.__srgb_p, "LAB", "RGB")
        return np.array(ImageCms.applyTransform(im, rgb2lab))

    def lab2hsv(self, image: np.ndarray) -> np.ndarray:
        im = Image.fromarray(image, mode='LAB')
        return np.array(im.convert('HSV'))

    def hsv2rgb(self, image: np.ndarray) -> np.ndarray:
        im = Image.fromarray(image, mode='HSV')
        return np.array(im.convert('RGB'))

    def hsv2lab(self, image: np.ndarray) -> np.ndarray:
        im = Image.fromarray(image, mode='HSV')
        return np.array(im.convert('LAB'))

def convert(image: np.ndarray, converter: ColourSpaceConverter, source_type: ColourSpace, result_type: ColourSpace):
    if source_type is result_type:
        return image

    if source_type is ColourSpace.RGB and result_type is ColourSpace.LAB:
        return converter.rgb2lab(image)
    elif source_type is ColourSpace.RGB and result_type is ColourSpace.HSV:
        return converter.rgb2hsv(image)
    elif source_type is ColourSpace.LAB and result_type is ColourSpace.RGB:
        return converter.lab2rgb(image)
    elif source_type is ColourSpace.LAB and result_type is ColourSpace.HSV:
        return converter.lab2hsv(image)
    elif source_type is ColourSpace.HSV and result_type is ColourSpace.RGB:
        return converter.hsv2rgb(image)
    elif source_type is ColourSpace.HSV and result_type is ColourSpace.LAB:
        return converter.hsv2lab(image)
    raise ValueError("You know what you did")
