from functools import wraps


def check_time_serie_compatible(method):
    """
    Check if the xarray object in the accessor corresponds to a time serie.
    """
    @wraps(method)
    def _check_ts_shape(self, *method_args, **method_kwargs):
        xr_dim = self._obj.values.ndim
        if xr_dim > 2:
            raise ValueError(
                'The routine {} requires an xarray with a time series format.'
                '\n The dimension must be 2'.format(method.__name__))
        method_output = method(self, *method_args, **method_kwargs)

        return method_output
    return _check_ts_shape
