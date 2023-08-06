import enum
from functools import partial
import logging
import typing

import cv2
import numpy as np #type: ignore
from PIL import Image #type: ignore


from colour_sort.sort_type import SortType
from colour_sort.colour_space import ColourSpace
from colour_sort import reducer, convert

try:
    import importlib.resource as pkg_resources #type: ignore
except ImportError:
    import importlib_resources as pkg_resources #type: ignore

SHIFT_ORDERS = {
    SortType.ABC:  [0, 1, 2],
    SortType.ACB:  [0, 2, 1],
    SortType.CBA:  [2, 1, 0],
    SortType.CAB:  [2, 0, 1],
    SortType.BAC:  [1, 0, 2],
    SortType.BCA:  [1, 2, 0],
    SortType.ABCC: [0, 1, 2],
    SortType.ACBC: [0, 2, 1],
    SortType.CBAC: [2, 1, 0],
    SortType.CABC: [2, 0, 1],
    SortType.BACC: [1, 0, 2],
    SortType.BCAC: [1, 2, 0],
}

IMAGE_SIZE = 4096
TOTAL_PIXELS = IMAGE_SIZE*IMAGE_SIZE

def _reshape_image(image):
    res = cv2.resize(np.array(image), dsize=(4096, 4096), interpolation=cv2.INTER_LANCZOS4)
    return np.reshape(res, (TOTAL_PIXELS, 3))

def _reshape_image_old(image):
    new_width, new_height = IMAGE_SIZE, IMAGE_SIZE

    thumb = image.resize((new_width, new_height), resample=Image.LANCZOS)
    return np.reshape(np.array(thumb), (TOTAL_PIXELS, 3))

# https://stackoverflow.com/a/49922520
def _norm(arr):
    return ((arr - arr.min()) * (1/(arr.max() - arr.min()) * 255)).astype('uint8')

def _sort_map(src: np.ndarray, mapped: np.ndarray) -> np.ndarray:
    mapping = np.argsort(src)
    reverse_mapping = np.argsort(mapping)
    return mapped[reverse_mapping]

def _all_rgb_colours():
    with pkg_resources.open_binary('colour_sort', 'all.npy') as colours:
        return np.load(colours)

def create_sorted_image(image: Image.Image, mode: SortType, colour_space: ColourSpace, converter: convert.ColourSpaceConverter) -> Image.Image:
    result = _all_rgb_colours()
    image_arr = np.array(image)

    # TODO Tidy
    reduce_func: typing.Callable[[np.ndarray], np.ndarray]
    if mode is SortType.BRIGHTNESS:
        # Must be in LAB
        if colour_space is not ColourSpace.LAB:
            logging.warning('Colour space needs to be in LAB to correctly sort by brightness')
            colour_space = ColourSpace.LAB
        reduce_func = partial(reducer.reduce_shift, order=[0])
    elif mode is SortType.AVG:
        reduce_func = reducer.reduce_sum
    elif mode is SortType.ZORDER:
        reduce_func = reducer.reduce_z_order
    # elif mode is SortType.HILBERT:
    #     reduce_func = reducer.reduce_hilbert
    elif mode is SortType.PCA:
        reduce_func = reducer.reduce_pca
    else:
        reduce_func = partial(reducer.reduce_shift, order=SHIFT_ORDERS[mode])

    current_mode = ColourSpace.from_str(image.mode)
    result_mode = colour_space.name

    converted_result = convert.convert(result, converter, ColourSpace.RGB, colour_space)
    converted_image = convert.convert(image_arr, converter, current_mode, colour_space)

    result = np.reshape(result, (4096*4096, 3))

    # TODO Should this be part of the conversion process?
    normalized_result = np.reshape(_norm(converted_result), (4096*4096, 3))
    normalized_image = _norm(converted_image)

    reshaped = _reshape_image_old(Image.fromarray(normalized_image, mode=colour_space.name))

    # If we don't want to intentially allow overflow, use uint32 so there's enough room for the bit shifting
    if not mode.is_clip():
        normalized_result = normalized_result.astype(np.uint32)
        reshaped = reshaped.astype(np.uint32)

    criteria_image = reduce_func(reshaped)
    criteria_result = reduce_func(normalized_result)

    # We do the the sorted on result instead of converted_result since
    # it was converted so that it would reduce the same way, but ultimatly
    # we want an RGB image, which result is
    results_sorted = result[np.argsort(criteria_result)]
    sorted_image = _sort_map(criteria_image, results_sorted)

    return Image.fromarray(np.reshape(sorted_image.astype(np.uint8), (IMAGE_SIZE, IMAGE_SIZE, 3)), mode=ColourSpace.RGB.name)
