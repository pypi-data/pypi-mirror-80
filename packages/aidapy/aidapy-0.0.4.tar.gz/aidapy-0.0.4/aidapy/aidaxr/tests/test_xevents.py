"""
The following test integration suite assesses the interconectivity between aidafunc, mission subpackage, and HelioPy
"""
import os
import numpy as np
import xarray as xr
import pandas as pd
from aidapy.aidaxr import xevents


def test_pvi():
    file_name_data = os.path.join(os.path.dirname(__file__),
                                  'data', 'pvi_input_f3_50pts.dat')
    data = np.loadtxt(file_name_data, unpack='True')
    data = data.T
    time = data[:, 0]
    locs = ['IA']

    foo = xr.DataArray(data[:, 1:2], coords=[time, locs],
                       dims=['time', 'space'], attrs={'units': 'nT'})
    s = 2 ** 2
    y = foo.xevents.pvi(scale=s)

    file_name_target = os.path.join(os.path.dirname(__file__),
                                    'data', 'pvi_output_f90.dat')
    target = np.loadtxt(file_name_target, unpack='True')
    target = target.T

    assert(np.allclose(y, target, atol=5e-7))


def test_threshold():
    data = np.random.rand(10, 1)
    data[2] = 27
    data[6] = 42
    times = pd.date_range("2000-01-01", periods=10)
    xr_pvi = xr.DataArray(data, coords=[times, ['pvi']], dims=['time', 'pvi'])
    threshold = xr_pvi.xevents.threshold(8)
    true_result = times[[2, 6]].to_numpy()
    assert((threshold == true_result).all())


def test_increm():
    # Scale
    s = 2*2

    file_name_input_data = os.path.join(os.path.dirname(__file__),
                                        'data', 'increm_input_f3.dat')
    data = np.loadtxt(file_name_input_data, unpack='True')
    dataT = np.transpose(data)
    # Take only the first 1000 points to calculate increments
    time = dataT[0:1000, 0]
    locs = ['IA']

    foo = xr.DataArray(dataT[0:1000, 1:2], coords=[time, locs],
                       dims=['time', 'space'], attrs={'units': 'nT'})
    y = foo.xevents.increm(scale=s)

    yyy = y[1]
    yy = np.array(yyy[:, 0])

    # Reference results from Fortran routine (already tested)
    file_name_target = os.path.join(os.path.dirname(__file__),
                                    'data', 'increm_output.dat')
    target = np.loadtxt(file_name_target, unpack='True')
    target = target.T

    assert np.allclose(yy, target, atol=5e-7)
