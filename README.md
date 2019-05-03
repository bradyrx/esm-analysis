# esmtools 

A toolbox for functions related to Earth System Model analysis, with a focus on biogeochemical oceanography.

**Note**: This is more of a personal package with functions I use commonly. It doesn't have any testing (as of now) or documentation, and isn't supposed to function as a full analysis package.

Please check out [`climpred`](https://github.com/bradyrx/climpred) for a package in development made for analysis of climate prediction ensembles.

## Installation
```shell
pip install git+https://github.com/bradyrx/esmtools
```

## Modules

`carbon`

Functions for the carbon cycle and carbonate chemistry.

`colormaps`

Load in a custom colormap (see below).

`loadutils`

Load in sample datasets or masks.

`filtering`

Functions for filtering output over space and time.

`physics`

Functions related to physical conversions.

`stats`

Functions for time series and spatial statistics

`vis`

Functions for colorbars, coloarmaps, and projecting data globally or regionally.

**Note**: Little development in the future will go towards visualization. We suggest [proplot](https://github.com/lukelbd/proplot) to users for a phenomenal `matplotlib` wrapper.

## Colormaps

Colormap RGB files are from NCL's color table reference. The title of each colorbar below is the keywork for et.colormaps.load_cmap(str)

```python
import esmtools as et
import numpy as np
import matplotlib.pyplot as plt

cmap = et.colormaps.load_cmap('amwg')
x = np.random.randn(50,50)
plt.pcolor(x, cmap=cmap)
plt.colorbar()
plt.show()
```

### Sequential

#### cools (12 colors)
![cools](https://www.ncl.ucar.edu/Document/Graphics/ColorTables/Images/precip_11lev_labelbar.500.png "cools")

#### gmt_cool (10 colors)
![gmt_cool](https://www.ncl.ucar.edu/Document/Graphics/ColorTables/Images/GMT_cool_labelbar.500.png "gmt_cool")

### Diverging

#### brown_blue (12 levels)
![brown_blue](https://www.ncl.ucar.edu/Document/Graphics/ColorTables/Images/BrownBlue12_labelbar.500.png "brown_blue")

#### cmp_flux (22 levels)
![cmp_flux](https://www.ncl.ucar.edu/Document/Graphics/ColorTables/Images/cmp_flux_labelbar.500.png "cmp_flux")

#### green_magenta (16 levels)
![green_magenta](https://www.ncl.ucar.edu/Document/Graphics/ColorTables/Images/GreenMagenta16_labelbar.500.png "green_magenta")

### Rainbow
There is little to no place for using rainbow colormaps. But sometimes we like to have fun and make pretty, perceptually-meaningless plots!

#### amwg (256 levels)
![amwg](https://www.ncl.ucar.edu/Document/Graphics/ColorTables/Images/amwg256_labelbar.500.png "amwg")

#### nice_gfdl (225 levels)
![nice_gfdl](https://www.ncl.ucar.edu/Document/Graphics/ColorTables/Images/nice_gfdl_labelbar.500.png "nice_gfdl")

## Contact
Developed and maintained by Riley Brady.

email: riley.brady@colorado.edu

web: https://www.rileyxbrady.com
