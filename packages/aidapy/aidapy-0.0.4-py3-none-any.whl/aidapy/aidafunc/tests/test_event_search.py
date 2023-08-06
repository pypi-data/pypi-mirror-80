"""
Tests for event_search module
"""

from datetime import datetime
import numpy as np
from aidapy import event_search


def test_event_search_df():
    start_time = datetime(2017, 7, 15, 7, 0, 0)
    end_time = datetime(2017, 7, 15, 12, 0, 0)

    data, event = event_search('df', start_time, end_time)

    target = [918, 1223, 3672, 3977, 7038, 7343, 11628, 11933, 12852, 13157,
              13158, 13463, 14076, 14381, 14382, 14687]

    assert np.allclose(target, event)


def test_event_search_edr():
    start_time = datetime(2017, 8, 20, 2, 0, 0)
    end_time = datetime(2017, 8, 20, 2, 10, 0)

    data, event = event_search('edr', start_time, end_time)

    target = [0, 3999, 8000, 11999]

    assert np.allclose(target, event)
