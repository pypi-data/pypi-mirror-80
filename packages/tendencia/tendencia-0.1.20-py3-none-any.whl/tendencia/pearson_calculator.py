
import rasterio
import riomucho
import numpy as np
import pymannkendall as mk
import scipy
from scipy import stats
from .utils import parse_slice

np.seterr(all='raise')
scipy.seterr(all='raise')


def basic_run(datum, window, ij, g_args):
    print(window)
    data = datum[0]
    out = np.zeros((2, *data.shape[1:]))
    out.fill(g_args['nodata'])

    sliceObj = parse_slice(g_args['selector'])
    sliceObj2 = parse_slice(g_args['selector2'])

    for i, j in np.ndindex(data.shape[1:]):
        pixel = data[:, i, j]
        a = pixel[sliceObj]
        b = pixel[sliceObj2]
        try:
            r, p = stats.pearsonr(a, b)
        except:
            pass
        else:
            out[0, i, j] = r
            out[1, i, j] = p

    return out.astype(np.float32)


def run_pearson(in_file, out_file, selector, selector2):
    float32_min = np.finfo(np.float32).min
    # get windows from an input
    with rasterio.open(in_file) as src:
        # grabbing the windows as an example. Default behavior is identical.
        windows = [[window, ij] for ij, window in src.block_windows()]
        options = src.meta
        # since we are only writing to 2 bands
        options.update(count=2, dtype=rasterio.float32, nodata=float32_min)

    global_args = {
        'selector': selector,
        'selector2': selector2,
        'nodata': float32_min
    }

    processes = 4

    # run it
    with riomucho.RioMucho([in_file], out_file, basic_run,
                           windows=windows,
                           global_args=global_args,
                           options=options) as rm:

        rm.run(processes)
