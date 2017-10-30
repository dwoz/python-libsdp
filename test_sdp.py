from sdp import TIMESRE

import pytest

def test_times_re_a():
    assert TIMESRE.match('17d').groups() == ('17', 'd')

def test_times_re_b():
    assert TIMESRE.match('-1h').groups() == ('-1', 'h')

def test_times_re_c():
    assert TIMESRE.match('0').groups() == ('0', '')
