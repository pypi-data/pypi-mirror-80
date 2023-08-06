
import rasterio
import numpy as np
import scipy
from .utils import parse_slice

np.seterr(all='raise')
scipy.seterr(all='raise')


def run_inspect(in_file):
    with rasterio.open(in_file) as src:
        data = src.read()
        random_x = np.random.randint(0, src.width)
        random_y = np.random.randint(0, src.height)
        pixel = data[:, random_x, random_y]
        print(pixel)
        
