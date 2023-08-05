"""Distances tests module.

Copyright (c) 2020 Thierry P.G. DECKER
All Rights Reserved.
Released under the MIT license

"""
import pytest

from siarnaq.distances import Distance


def test_instanciations():
    assert isinstance(Distance(), Distance)

    assert isinstance(Distance('km'), Distance)
    assert isinstance(Distance(scale='km'), Distance)
    assert isinstance(Distance('mi'), Distance)
    assert isinstance(Distance(scale='mi'), Distance)

    with pytest.raises(Exception):
        assert Distance(scale='Dummy')
    with pytest.raises(Exception):
        assert Distance(dist='Dummy')
    with pytest.raises(Exception):
        assert Distance(scale='Dummy', dist='Dummy')


def test_conv_km_to_mi():
    assert round(Distance.conv_km_to_mi(1), 2) == 0.62


def test_conv_mi_to_km():
    assert round(Distance.conv_mi_to_km(1), 2) == 1.61


def test_propertty_getter_scales():
    assert Distance().scales == {'km', 'mi'}


def test_propertty_getter_scale():
    assert Distance().scale == 'km'
    assert Distance(scale='km').scale == 'km'
    assert Distance(scale='mi').scale == 'mi'


def test_property_getter_dist():
    assert Distance(dist=10).dist == 10
    assert Distance(scale='km', dist=10).dist == 10
    assert Distance(scale='mi', dist=10).dist == 10


def test_property_getter_kilometer():
    assert Distance(scale='km', dist=10).kilometer == 10
    assert Distance(scale='mi', dist=10).kilometer == 16.09


def test_property_getter_mile():
    assert round(Distance(scale='km', dist=10).mile, 2) == 6.22
    assert Distance(scale='mi', dist=10).mile == 10


def test_property_setter_dist():
    r = Distance(scale='km')
    r.dist = 10
    assert r.dist == 10


def test_property_setter_scale():
    with pytest.raises(Exception):
        r = Distance(scale='km', dist=1)
        r.scale = 'Dummy'
    r = Distance(scale='km', dist=1)
    r.scale = 'mi'
    assert r.scale == 'mi'
    assert round(r.dist, 2) == 0.62
    assert round(r.mile, 2) == 0.62
    assert round(r.kilometer, 2) == 1
    r = Distance(scale='mi', dist=1)
    r.scale = 'km'
    assert r.scale == 'km'
    assert round(r.dist, 2) == 1.61
    assert round(r.mile, 2) == 1
    assert round(r.kilometer, 2) == 1.61


def test_str():
    assert str(Distance()) == '0.0 km'
    assert str(Distance(scale='mi', dist=1)) == '1.0 mi'


def test_repr():
    assert repr(Distance()) == 'Distance(\'km\', 0.0)'
    assert repr(Distance(scale='mi', dist=1)) == 'Distance(\'mi\', 1.0)'


def test_add():
    r = Distance(dist=10)
    r = r + 1
    assert r.dist == 11
    r += 1
    assert r.dist == 12
    r = 1 + r
    assert r.dist == 13

    r1 = Distance(dist=10)
    r2 = Distance(dist=10)
    r = r1 + r2
    assert r.scale == 'km'
    assert r.dist == 20
    assert r.kilometer == 20
    assert round(r.mile, 2) == 12.43

    r1 = Distance(scale='mi', dist=10)
    r2 = Distance(scale='mi', dist=10)
    r1 += r2
    assert r1.scale == 'mi'
    assert r1.dist == 20
    assert round(r1.kilometer, 2) == 32.18
    assert r1.mile == 20

    r1 = Distance(scale='mi', dist=10)
    r2 = Distance(scale='km', dist=10)
    r1 += r2
    assert r1.scale == 'mi'
    assert round(r1.dist, 2) == 16.22
    assert round(r1.kilometer, 2) == 26.09
    assert round(r1.mile, 2) == 16.22


def test_sub():
    r = Distance(dist=10)
    r = r - 1
    assert r.dist == 9
    r -= 1
    assert r.dist == 8

    r1 = Distance(scale='km', dist=5)
    r2 = Distance(scale='km', dist=5)
    r = r1 - r2
    assert r.scale == 'km'
    assert round(r.dist, 2) == 0.00

    r1 = Distance(scale='km', dist=5)
    r2 = Distance(scale='km', dist=5)
    r1 -= r2
    assert r.scale == 'km'
    assert round(r.dist, 2) == 0.00

    r1 = Distance(scale='mi', dist=5)
    r2 = Distance(scale='km', dist=5)
    r = r1 - r2
    assert r.scale == 'mi'
    assert round(r.dist, 2) == 1.89

    with pytest.raises(Exception):
        r = 1 - r


def test_mul():
    r = Distance(scale='mi', dist=10)
    r = r * 2
    assert r.dist == 20
    assert r.scale == 'mi'
    r *= 2
    assert r.dist == 40
    assert r.scale == 'mi'
    r = 2 * r
    assert r.dist == 80
    assert r.scale == 'mi'


def test_div():
    r = Distance(scale='km', dist=100)
    r = r / 2
    assert r.dist == 50
    assert r.scale == 'km'
    r /= 2
    assert r.dist == 25
    assert r.scale == 'km'
    with pytest.raises(Exception):
        r = 2 / r
