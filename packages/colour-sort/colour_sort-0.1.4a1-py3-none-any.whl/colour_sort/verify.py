import sys

import numpy as np
from PIL import Image

def _colour_check(img: Image.Image) -> np.array:
    check = np.zeros(256*256*256, dtype=np.bool)
    img_a = np.array(img).astype(np.uint32) # Oh god they all have to be uint32 because 255 << 16 = 16711680
    if np.product(img_a.shape[:2]) != 256*256*256:
        raise Exception('Image is not the correct shape')

    flattened = np.reshape(img_a, (256*256*256, 3))

    np.left_shift(flattened[:,0], 16, out=flattened[:,0])
    np.left_shift(flattened[:,1], 8, out=flattened[:,1])

    indexed = flattened[:,0] | flattened[:,1] | flattened[:,2]
    check[indexed] = True
    return check


def verify_image(img: Image.Image) -> bool:
    check = _colour_check(img)
    return np.all(check)

def missing_colours(img: Image.Image) -> bool:
    check = _colour_check(img)
    indicies = np.where(check == False)[0]
    r = (indicies & 0x00FF0000) >> 16
    g = (indicies & 0x0000FF00) >> 8
    b = (indicies & 0x000000FF)
    return np.stack([r, g, b], axis=1)

if __name__ == '__main__':
    img = Image.open(sys.argv[1])
    print(verify_image(img))
