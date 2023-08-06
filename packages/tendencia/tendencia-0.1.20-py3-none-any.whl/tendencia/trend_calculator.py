
import rasterio
import riomucho
import numpy as np
import pymannkendall as mk
from .utils import parse_slice

np.seterr(all='raise')


def basic_run(datum, window, ij, g_args):
    print(window)
    data = datum[0]
    out = np.zeros((2, *data.shape[1:]))
    out.fill(g_args['nodata'])

    selector = g_args['selector']
    sliceObj = parse_slice(selector)

    for i, j in np.ndindex(data.shape[1:]):
        pixel = data[:, i, j]
        pixel = pixel[sliceObj]
        try:
            trend = mk.yue_wang_modification_test(pixel)
        except:
            pass
        else:
            out[0, i, j] = trend.slope
            out[1, i, j] = trend.p

    return out.astype(np.float32)


def run_trend(in_file, out_file, selector):
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
        'nodata': float32_min
    }

    processes = 4

    # run it
    with riomucho.RioMucho([in_file], out_file, basic_run,
                           windows=windows,
                           global_args=global_args,
                           options=options) as rm:

        rm.run(processes)
