import numpy as np
from colour_sort import hilbertcurve, pymorton

'''
Reduces an 1 dimentional list of colours to integers via bit shifting
Entries are assuming to be 8-bit
image's datatype needs to be big enough to contain the largest shifted entry or overflow will occur
'''
def reduce_shift(image: np.ndarray, order: list = [0, 1, 2]) -> np.ndarray:
    if len(order) == 0:
        return ValueError("You gotta pick something")

    res = image.transpose()

    # Special case for selection of a single column
    # Logic below breaks for 2**(len(order)+1) < 8 so we just special case it
    if len(order) == 1:
        return res[order[0]]

    reduced_res = 0
    for index, shift in enumerate(range(2**(len(order)+1), -1, -8)):
        reduced_res |= (res[order[index]] << shift)

    return reduced_res


'''
Reduce via summation, this can be used for an average value ordering since the missinig division step would not affect the ordering
'''
def reduce_sum(image: np.ndarray) -> np.ndarray:
    return np.sum(image, axis=1)

'''
Reduce via a z-order transformation
'''
def reduce_z_order(image: np.ndarray) -> np.ndarray:
    return pymorton.interleave3_np(image)


'''
Reduce via distance from 3d hilbert curve
'''
def reduce_hilbert(image: np.ndarray, p = 8, n = 3) -> np.ndarray:
    curve = hilbertcurve.HilbertCurve(p, n)
    return np.apply_along_axis(curve.distance_from_coordinates, 1, image) # This is extraordinarily slow


def reduce_pca(image: np.ndarray):
    from sklearn.decomposition import PCA
    pca = PCA(n_components=1)
    return pca.fit_transform(image)[:,0]

