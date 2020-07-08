import numpy as np
import numpy.polynomial.polynomial as poly
import pytest
from xarray.testing import assert_allclose

from esmtools.stats import corr, linear_slope, linregress, polyfit, rm_poly, rm_trend

TIME_TYPES = ["datetime", "cftime", "float"]


def _np_rm_poly(x, y, order):
    coefs = poly.polyfit(x, y, order)
    fit = poly.polyval(x, coefs)
    return y - fit


@pytest.mark.parametrize("gridded", (True, False))
@pytest.mark.parametrize("time_type", TIME_TYPES)
@pytest.mark.parametrize("order", (1, 2, 3, 4))
def test_rm_poly_against_time(
    gridded_da_datetime, gridded_da_cftime, gridded_da_float, time_type, gridded, order
):
    """Tests that ``rm_poly`` works against a time index."""
    data = eval(f"gridded_da_{time_type}")()
    x = data["time"]
    y = data if gridded else data.isel(lat=0, lon=0)
    detrended = rm_poly(x, y, order)
    assert (detrended != y).all()


@pytest.mark.parametrize("gridded", (True, False))
@pytest.mark.parametrize("time_type", TIME_TYPES)
def test_rm_poly_against_time_dask(
    gridded_da_datetime, gridded_da_cftime, gridded_da_float, time_type, gridded
):
    """Tests that ``rm_poly`` works against a time index with dask arrays."""
    data = eval(f"gridded_da_{time_type}")()
    x = data["time"]
    y = data if gridded else data.isel(lat=0, lon=0)
    expected = rm_poly(x, y, 2)
    actual = rm_poly(x.chunk(), y.chunk(), 2).compute()
    assert_allclose(expected, actual)


@pytest.mark.parametrize("gridded", (True, False))
@pytest.mark.parametrize("order", (1, 2, 3, 4))
def test_rm_poly_against_data(gridded_da_float, gridded, order):
    """Tests that ``rm_poly`` works against a single data series and another gridded
    data series."""
    x = gridded_da_float() if gridded else gridded_da_float().isel(lat=0, lon=0)
    y = gridded_da_float()
    detrended = rm_poly(x, y, order)
    assert (detrended != y).all()


@pytest.mark.parametrize("gridded", (True, False))
def test_rm_poly_against_data_dask(gridded_da_float, gridded):
    """Tests that ``rm_poly`` works against a single data series and another gridded
    data series with dask arrays."""
    x = gridded_da_float() if gridded else gridded_da_float().isel(lat=0, lon=0)
    y = gridded_da_float()
    expected = rm_poly(x, y, 2)
    actual = rm_poly(x.chunk(), y.chunk(), 2).compute()
    assert_allclose(expected, actual)


@pytest.mark.parametrize("order", (1, 2, 3, 4))
def test_rm_poly_validity(gridded_da_float, order):
    """Tests that grid cells are different and equal to doing it manually."""
    data = gridded_da_float()
    x = data["time"]
    y = data
    actual = rm_poly(x, y, order)
    for i in range(3):
        for j in range(3):
            single_grid_cell = y.isel(lon=i, lat=j)
            expected = _np_rm_poly(x.values, single_grid_cell.values, order)
            assert (actual.isel(lon=i, lat=j).values == expected).all()


@pytest.mark.parametrize("order", (1, 2, 3, 4))
def test_rm_poly_validity_dask(gridded_da_float, order):
    """Tests that grid cells are different and equal to doing it manually with dask
    arrays."""
    data = gridded_da_float().chunk()
    x = data["time"]
    y = data
    actual = rm_poly(x, y, order)
    for i in range(3):
        for j in range(3):
            single_grid_cell = y.isel(lon=i, lat=j)
            expected = _np_rm_poly(x.values, single_grid_cell.values, order)
            assert (actual.isel(lon=i, lat=j).values == expected).all()


@pytest.mark.parametrize("gridded", (True, False))
@pytest.mark.parametrize("time_type", TIME_TYPES)
def test_rm_trend_against_time(
    gridded_da_datetime, gridded_da_cftime, gridded_da_float, time_type, gridded
):
    """Tests that ``rm_trend`` is equivelant to ``rm_poly`` with order=1 against time
    series."""
    data = eval(f"gridded_da_{time_type}")()
    x = data["time"]
    y = data if gridded else data.isel(lat=0, lon=0)
    expected = rm_poly(x, y, 1)
    actual = rm_trend(x, y)
    assert_allclose(expected, actual)


@pytest.mark.parametrize("gridded", (True, False))
def test_rm_trend_against_data(gridded_da_float, gridded):
    """Tests that ``rm_trend`` is equivelant to ``rm_poly`` with order=1 against data
    series and gridded data."""
    x = gridded_da_float() if gridded else gridded_da_float().isel(lat=0, lon=0)
    y = gridded_da_float()
    expected = rm_poly(x, y, 1)
    actual = rm_trend(x, y)
    assert_allclose(expected, actual)


@pytest.mark.parametrize("gridded", (True, False))
@pytest.mark.parametrize("time_type", TIME_TYPES)
@pytest.mark.parametrize("order", (1, 2, 3, 4))
def test_polyfit_against_time(
    gridded_da_datetime, gridded_da_cftime, gridded_da_float, time_type, gridded, order
):
    """Tests that ``polyfit`` plus ``rm_poly`` equals the original time series when
    fitting against time."""
    data = eval(f"gridded_da_{time_type}")()
    x = data["time"]
    y = data if gridded else data.isel(lat=0, lon=0)
    dt = rm_poly(x, y, order)
    fit = polyfit(x, y, order)
    diff = np.abs((dt + fit) - y)
    assert (diff < 1e-15).all()


@pytest.mark.parametrize("gridded", (True, False))
@pytest.mark.parametrize("time_type", TIME_TYPES)
def test_polyfit_against_time_dask(
    gridded_da_datetime, gridded_da_cftime, gridded_da_float, time_type, gridded
):
    """Tests that ``polyfit`` plus ``rm_poly`` equals the original time series when
    fitting against time with dask arrays."""
    data = eval(f"gridded_da_{time_type}")().chunk()
    x = data["time"]
    y = data if gridded else data.isel(lat=0, lon=0)
    dt = rm_poly(x, y, 2)
    fit = polyfit(x, y, 2)
    diff = np.abs((dt + fit) - y)
    assert (diff.compute() < 1e-15).all()


@pytest.mark.parametrize("gridded", (True, False))
@pytest.mark.parametrize("order", (1, 2, 3, 4))
def test_polyfit_against_data(gridded_da_float, gridded, order):
    """Tests that ``polyfit`` plus ``rm_poly`` equals the original time series when
    fitting against data series and gridded data."""
    x = gridded_da_float() if gridded else gridded_da_float().isel(lat=0, lon=0)
    y = gridded_da_float()
    dt = rm_poly(x, y, order)
    fit = polyfit(x, y, order)
    diff = np.abs((dt + fit) - y)
    assert (diff < 1e-15).all()


@pytest.mark.parametrize("gridded", (True, False))
def test_polyfit_against_data_dask(gridded_da_float, gridded):
    """Tests that ``polyfit`` plus ``rm_poly`` equals the original time series
    when fitting against data series and gridded data with dask arrays."""
    x = gridded_da_float() if gridded else gridded_da_float().isel(lat=0, lon=0).chunk()
    y = gridded_da_float()
    dt = rm_poly(x, y, 2)
    fit = polyfit(x, y, 2)
    diff = np.abs((dt + fit) - y)
    assert (diff.compute() < 1e-15).all()


def test_corr_two_grids(gridded_da_float):
    """Tests that correlations between two grids work."""
    x = gridded_da_float()
    y = gridded_da_float()
    corrcoeff = corr(x, y, dim="time")
    assert not corrcoeff.isnull().any()


def test_corr_grid_and_ts(ts_monthly_da, gridded_da_datetime):
    """Tests that correlation works between a grid and a time series."""
    x = ts_monthly_da()
    y = gridded_da_datetime()
    corrcoeff = corr(x, y, dim="time")
    assert not corrcoeff.isnull().any()


def test_corr_lead(gridded_da_float):
    """Tests positive lead for correlation."""
    x = gridded_da_float()
    y = gridded_da_float()
    corrcoeff = corr(x, y, dim="time", lead=3)
    assert not corrcoeff.isnull().any()


def test_corr_lag(gridded_da_float):
    """Tests negative lead for correlation."""
    x = gridded_da_float()
    y = gridded_da_float()
    corrcoeff = corr(x, y, dim="time", lead=-3)
    assert not corrcoeff.isnull().any()


def test_corr_return_p(gridded_da_float):
    """Tests that p-value is returned properly for correlation."""
    x = gridded_da_float()
    y = gridded_da_float()
    corrcoeff, pval = corr(x, y, dim="time", return_p=True)
    assert not (corrcoeff.isnull().any()) & (pval.isnull().any())
