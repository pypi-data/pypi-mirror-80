import numpy as np
import xarray as xr

from aidapy.aidaxr.tools import check_time_serie_compatible


@xr.register_dataarray_accessor('xevents')
class AidaAccessorStatistics:
    def __init__(self, xarray_obj):
        self._obj = xarray_obj

    @check_time_serie_compatible
    def pvi(self, scale):
        """
        Returns the PVI of a timeseries

        .. math::

            y = \\frac{|x_i - x_{i+s}|^2}{<|x_i - x_{i+s}|^2>}

        where :math:`s` is the scale.

        Parameters
        ----------
        scale : int
            Scale at which to compute the PVI.

        Returns
        -------
        values : xarray.DataArray
            An xarray containing the pvi of the original timeseries.

        """
        data = self._obj.values
        if len(data.shape) == 1:
            data = data.reshape((-1, 1))
        f = np.abs((data[scale:, :]-data[:-scale, :]))
        f2 = np.sum(f**2, axis=1)
        sigma = np.mean(f2)
        result = np.array(f2/sigma)

        t = self._obj.dims[0]
        time = self._obj.coords[t]
        result = xr.DataArray(result,
                              coords=[time[0:len(f)]],
                              dims=[t],
                              attrs=self._obj.attrs)
        result.attrs['units'] = 'dimensionless'
        return result

    @check_time_serie_compatible
    def threshold(self, theta):
        """
        Returns the location of the PVI peaks above the threshold theta
        theta is usually 8 for extreme events, as reported in literature.

        Parameters
        ----------
        theta : int
            Threshold value for PVI.

        Returns
        -------
        result : np.array
            A numpy array containing the location of the pvi peaks above theta.

        """
        data = self._obj.values
        t = self._obj.dims[0]
        time = self._obj.coords[t].values
        if len(data.shape) == 1:
            data = data.reshape((-1, 1))

        filter_ = data > theta
        filter_ = filter_.any(axis=1)

        result = time[filter_]

        return result

    @check_time_serie_compatible
    def increm(self, scale):
        """
        Returns the increments of a timeseries

        .. math:: y = |x_i - x_{i+s}|

        where :math:`s` is the scale.

        Parameters
        ----------
        scale : int
            Scale at which to compute the increments.

        Returns
        -------
        kurt : np.array
            kurtosis of the increments, one per product, using the Fisher's
            definition (0 value for a normal distribution).


        result : xarray.DataArray
            An xarray containing the time series increments, one per
            product in the original timeseries.

        """
        from scipy.stats import kurtosis
        data = self._obj.values
        if len(data.shape) == 1:
            data = data.reshape((-1, 1))
        f = np.abs((data[scale:, :]-data[:-scale, :]))
        result = np.array(f)

        c = self._obj.dims[1]
        t = self._obj.dims[0]
        cols = self._obj.coords[c]
        time = self._obj.coords[t]
        result = xr.DataArray(result,
                              coords=[time[0:len(f)], cols],
                              dims=[t, c],
                              attrs=self._obj.attrs)
        kurt = kurtosis(result, axis=0, fisher=False)
        return kurt, result
