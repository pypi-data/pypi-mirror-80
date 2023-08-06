
import time
import click
from click import utils
from numpy.core.numeric import Infinity
import rasterio
import numpy as np
import pymannkendall as mk
import riomucho
import tendencia_utils as utils
from .trend_calculator import run_trend
from .pearson_calculator import run_pearson
from .inspect_calculator import run_inspect

# np.seterr(all='raise')

colormap = {
    0: (0, 0, 0),
    1: (252, 3, 1, 255),
    2: (247, 132, 2, 255),
    3: (255, 253, 166, 255),
    4: (223, 253, 118, 255),
    5: (47, 246, 3, 255),
    6: (15, 87, 2, 255),
}


@click.group()
def cli():
    pass


@click.command()
@click.option('--out', '-o', 'out_file', required=True)
@click.option('--selector', '-s', required=True)
@click.argument('in_file', required=True)
def trend(out_file, selector, in_file):
    print(out_file, selector, in_file)
    run_trend(in_file, out_file, selector)


@click.command()
@click.option('--out', '-o', 'out_file', required=True)
@click.option('--selector', '-s', required=True)
@click.option('--selector2', '-s2', required=True)
@click.argument('in_file', required=True)
def pearson(out_file, selector, selector2, in_file):
    click.echo('pearson')
    run_pearson(in_file, out_file, selector, selector2)


@click.command()
@click.argument('in_file', required=True)
def inspect(in_file):
    run_inspect(in_file)


@click.command()
@click.argument('in_file', required=True)
def print_func(in_file):
    with rasterio.open(in_file) as src:
        print(src.read())


@click.command()
@click.argument('in_file', required=True)
@click.argument('out_file', required=True)
def remap(in_file, out_file):
    with rasterio.open(in_file) as src:
        data = src.read()
        profile = src.profile
        profile.update(count=1, nodata=0, dtype=rasterio.uint8)
        f = np.frompyfunc(utils.trend_remap, 2, 1)
        out = f(data[0], data[1])
        with rasterio.open(out_file, 'w', **profile) as dst:
            dst.write(out.astype(rasterio.uint8), 1)
            dst.write_colormap(1, colormap)


cli.add_command(trend)
cli.add_command(pearson)
cli.add_command(inspect)
# cli.add_command(scale)
cli.add_command(print_func, "print")
cli.add_command(remap)


if __name__ == "__main__":
    cli()
