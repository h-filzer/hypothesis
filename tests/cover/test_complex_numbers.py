# coding=utf-8
#
# This file is part of Hypothesis, which may be found at
# https://github.com/HypothesisWorks/hypothesis-python
#
# Most of this work is copyright (C) 2013-2018 David R. MacIver
# (david@drmaciver.com), but it contains contributions by others. See
# CONTRIBUTING.rst for a full list of people who may hold copyright, and
# consult the git log if you need to determine who owns an individual
# contribution.
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file, You can
# obtain one at http://mozilla.org/MPL/2.0/.
#
# END HEADER

from __future__ import division, print_function, absolute_import

import sys

import hypothesis.strategies as st
from hypothesis import given
from tests.common.debug import minimal
from hypothesis.strategies import complex_numbers


def test_minimal():
    assert minimal(complex_numbers(), lambda x: True) == 0


def test_minimal_nonzero_real():
    assert minimal(complex_numbers(), lambda x: x.real != 0) == 1


def test_minimal_nonzero_imaginary():
    assert minimal(complex_numbers(), lambda x: x.imag != 0) == 1j


def test_minimal_quadrant1():
    assert minimal(
        complex_numbers(),
        lambda x: x.imag > 0 and x.real > 0
    ) == 1 + 1j


def test_minimal_quadrant2():
    assert minimal(
        complex_numbers(),
        lambda x: x.imag > 0 and x.real < 0
    ) == -1 + 1j


def test_minimal_quadrant3():
    assert minimal(
        complex_numbers(),
        lambda x: x.imag < 0 and x.real < 0
    ) == -1 - 1j


def test_minimal_quadrant4():
    assert minimal(
        complex_numbers(),
        lambda x: x.imag < 0 and x.real > 0
    ) == 1 - 1j


@given(st.data(), st.integers(-5, 5).map(lambda x: 10 ** x))
def test_max_magnitude_respected(data, mag):
    c = data.draw(complex_numbers(max_magnitude=mag))
    assert abs(c) <= mag * (1 + sys.float_info.epsilon)


def test_minimal_max_magnitude_zero():
    assert minimal(
        complex_numbers(max_magnitude=0),
        lambda x: True
    ) == 0


@given(st.data(), st.integers(-5, 5).map(lambda x: 10 ** x))
def test_min_magnitude_respected(data, mag):
    c = data.draw(complex_numbers(min_magnitude=mag))
    assert abs(c) >= mag * (1 - sys.float_info.epsilon)


def test_minimal_min_magnitude_zero():
    assert minimal(
        complex_numbers(min_magnitude=0),
        lambda x: True
    ) == 0


def test_minimal_min_magnitude_none():
    assert minimal(
        complex_numbers(min_magnitude=None),
        lambda x: True
    ) == 0


# FIXME : expect this to be 1, but 0.5 returned
@pytest.mark.skipif(True, reason='to determine')
def test_minimal_min_magnitude_positive():
    assert minimal(
        complex_numbers(min_magnitude=0.5),
        lambda x: True
    ) == 1


def test_minimal_max_magnitude_finite():
    assert minimal(
        complex_numbers(max_magnitude=1.5),
        lambda x: True
    ) == 0


# FIXME : expect this to be 1, but 0.5 returned
@pytest.mark.skipif(True, reason='to determine')
def test_minimal_minmax_magnitude():
    assert minimal(
        complex_numbers(min_magnitude=0.5, max_magnitude=1.5),
        lambda x: True
    ) == 1


def test_minimal_minmax_magnitude_equal():
    assert minimal(
        complex_numbers(min_magnitude=1, max_magnitude=1),
        lambda x: True
    ) == 1
