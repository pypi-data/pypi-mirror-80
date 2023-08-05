"""Degrees tests module.

Copyright (c) 2020 Thierry P.G. DECKER
All Rights Reserved.
Released under the MIT license

"""

import pytest

from siarnaq.degrees import Degree


def test_instanciations():
    assert isinstance(Degree(), Degree)

    assert isinstance(Degree('ce'), Degree)
    assert isinstance(Degree('fa'), Degree)
    assert isinstance(Degree('ke'), Degree)
    assert isinstance(Degree('ra'), Degree)

    assert isinstance(Degree(temp=10), Degree)

    assert isinstance(Degree(scale='ce'), Degree)
    assert isinstance(Degree(scale='fa'), Degree)
    assert isinstance(Degree(scale='ke'), Degree)
    assert isinstance(Degree(scale='ra'), Degree)

    assert isinstance(Degree(scale='ce', temp=0), Degree)
    assert isinstance(Degree(scale='fa', temp=0), Degree)
    assert isinstance(Degree(scale='ke', temp=0), Degree)
    assert isinstance(Degree(scale='ra', temp=0), Degree)

    with pytest.raises(Exception):
        assert Degree(scale='Dummy')
    with pytest.raises(Exception):
        assert Degree(temp='Dummy')
    with pytest.raises(Exception):
        assert Degree(scale='Dummy', temp='Dummy')


def test_static_methods():
    assert round(Degree.conv_ce_to_fa(temp=0), 2) == 32.00
    assert round(Degree.conv_ce_to_ke(temp=0), 2) == 273.15
    assert round(Degree.conv_ce_to_ra(temp=0), 2) == 491.67
    assert round(Degree.conv_fa_to_ce(temp=32), 2) == 0.00
    assert round(Degree.conv_fa_to_ke(temp=32), 2) == 273.15
    assert round(Degree.conv_fa_to_ra(temp=32), 2) == 491.67
    assert round(Degree.conv_ke_to_ce(temp=0), 2) == -273.15
    assert round(Degree.conv_ke_to_fa(temp=273.15), 2) == 32.00
    assert round(Degree.conv_ke_to_ra(temp=100), 2) == 180
    assert round(Degree.conv_ra_to_ce(temp=100), 2) == -217.59
    assert round(Degree.conv_ra_to_fa(temp=100), 2) == -359.67
    assert round(Degree.conv_ra_to_ke(temp=100), 2) == 55.56


def test_propertties_getters():
    assert Degree().scales == {'ce', 'fa', 'ke', 'ra'}

    r = Degree(scale='ce', temp=0)
    assert r.scale == 'ce'
    assert round(r.temp, 2) == 0.00
    assert round(r.celcius, 2) == 0.00
    assert round(r.fahrenheit, 2) == 32.00
    assert round(r.kelvin, 2) == 273.15
    assert round(r.rankine, 2) == 491.67

    r = Degree(scale='fa', temp=0)
    assert r.scale == 'fa'
    assert round(r.temp, 2) == 0.00
    assert round(r.celcius, 2) == -17.78
    assert round(r.fahrenheit, 2) == 0
    assert round(r.kelvin, 2) == 255.37
    assert round(r.rankine, 2) == 459.67

    r = Degree(scale='ke', temp=0)
    assert r.scale == 'ke'
    assert round(r.temp, 2) == 0.00
    assert round(r.celcius, 2) == -273.15
    assert round(r.fahrenheit, 2) == -459.67
    assert round(r.kelvin, 2) == 0
    assert round(r.rankine, 2) == 0

    r = Degree(scale='ra', temp=0)
    assert r.scale == 'ra'
    assert round(r.temp, 2) == 0.00
    assert round(r.celcius, 2) == -273.15
    assert round(r.fahrenheit, 2) == -459.67
    assert round(r.kelvin, 2) == 0
    assert round(r.rankine, 2) == 0


def test_propertties_setters():
    #
    # From 'ce' to 'fa'
    #
    r = Degree(scale='ce', temp=0)
    r.scale = 'fa'
    assert round(r.temp, 2) == 32.00
    assert round(r.celcius, 2) == 0
    assert round(r.fahrenheit, 2) == 32.00
    assert round(r.kelvin, 2) == 273.15
    assert round(r.rankine, 2) == 491.67
    #
    # From 'ce' to 'ke'
    #
    r = Degree(scale='ce', temp=0)
    r.scale = 'ke'
    assert round(r.temp, 2) == 273.15
    assert round(r.celcius, 2) == 0.00
    assert round(r.fahrenheit, 2) == 32.00
    assert round(r.kelvin, 2) == 273.15
    assert round(r.rankine, 2) == 491.67
    #
    # From 'ce' to 'ra'
    #
    r = Degree(scale='ce', temp=0)
    r.scale = 'ra'
    assert round(r.temp, 2) == 491.67
    assert round(r.celcius, 2) == 0.00
    assert round(r.fahrenheit, 2) == 32.00
    assert round(r.kelvin, 2) == 273.15
    assert round(r.rankine, 2) == 491.67
    #
    # From 'fa' to 'ce'
    #
    r = Degree(scale='fa', temp=0)
    r.scale = 'ce'
    assert round(r.temp, 2) == -17.78
    assert round(r.celcius, 2) == -17.78
    assert round(r.fahrenheit, 2) == 0.00
    assert round(r.kelvin, 2) == 255.37
    assert round(r.rankine, 2) == 459.67
    #
    # From 'fa' to 'ke'
    #
    r = Degree(scale='fa', temp=0)
    r.scale = 'ke'
    assert round(r.temp, 2) == 255.37
    assert round(r.celcius, 2) == -17.78
    assert round(r.fahrenheit, 2) == 0.00
    assert round(r.kelvin, 2) == 255.37
    assert round(r.rankine, 2) == 459.67
    #
    # From 'fa' to 'ra'
    #
    r = Degree(scale='fa', temp=0)
    r.scale = 'ra'
    assert round(r.temp, 2) == 459.67
    assert round(r.celcius, 2) == -17.78
    assert round(r.fahrenheit, 2) == 0.00
    assert round(r.kelvin, 2) == 255.37
    assert round(r.rankine, 2) == 459.67
    #
    # From 'ke' to 'ce'
    #
    r = Degree(scale='ke', temp=0)
    r.scale = 'ce'
    assert round(r.temp, 2) == -273.15
    assert round(r.celcius, 2) == -273.15
    assert round(r.fahrenheit, 2) == -459.67
    assert round(r.kelvin, 2) == 0.00
    assert round(r.rankine, 2) == 0.00
    #
    # From 'ke' to 'fa'
    #
    r = Degree(scale='ke', temp=0)
    r.scale = 'fa'
    assert round(r.temp, 2) == -459.67
    assert round(r.celcius, 2) == -273.15
    assert round(r.fahrenheit, 2) == -459.67
    assert round(r.kelvin, 2) == 0.00
    assert round(r.rankine, 2) == 0.00
    #
    # From 'ke' to 'ra'
    #
    r = Degree(scale='ke', temp=0)
    r.scale = 'ra'
    assert round(r.temp, 2) == 0.00
    assert round(r.celcius, 2) == -273.15
    assert round(r.fahrenheit, 2) == -459.67
    assert round(r.kelvin, 2) == 0.00
    assert round(r.rankine, 2) == 0.00
    #
    # From 'ra' to 'ce'
    #
    r = Degree(scale='ra', temp=0)
    r.scale = 'ce'
    assert round(r.temp, 2) == -273.15
    assert round(r.celcius, 2) == -273.15
    assert round(r.fahrenheit, 2) == -459.67
    assert round(r.kelvin, 2) == 0.00
    assert round(r.rankine, 2) == 0.00
    #
    # From 'ra' to 'fa'
    #
    r = Degree(scale='ra', temp=0)
    r.scale = 'fa'
    assert round(r.temp, 2) == -459.67
    assert round(r.celcius, 2) == -273.15
    assert round(r.fahrenheit, 2) == -459.67
    assert round(r.kelvin, 2) == 0.00
    assert round(r.rankine, 2) == 0.00
    #
    # From 'ra' to 'ke'
    #
    r = Degree(scale='ra', temp=0)
    r.scale = 'ke'
    assert round(r.temp, 2) == 0.00
    assert round(r.celcius, 2) == -273.15
    assert round(r.fahrenheit, 2) == -459.67
    assert round(r.kelvin, 2) == 0.00
    assert round(r.rankine, 2) == 0.00

    with pytest.raises(Exception):
        r = Degree()
        r.scale = 'Dummy'


def test_add():
    r1 = Degree(scale='ce', temp=1.0)
    r2 = Degree(scale='ce', temp=20.0)
    r = r1 + r2
    assert r.scale == 'ce'
    assert r.temp == 21.00

    r1 = Degree(scale='fa', temp=1.0)
    r2 = Degree(scale='fa', temp=2.0)
    r = r1 + r2
    assert r.scale == 'fa'
    assert r.temp == 3.00

    r1 = Degree(scale='fa', temp=1.0)
    r = r1 + 2.00
    assert r.scale == 'fa'
    assert r.temp == 3.00

    r1 = Degree(scale='ke', temp=1.0)
    r = 2.00 + r1
    assert r.scale == 'ke'
    assert r.temp == 3.00

    r1 = Degree(scale='ce', temp=1.0)
    r2 = Degree(scale='ce', temp=1.0)
    r1 += r2
    assert r1.scale == 'ce'
    assert r1.temp == 2.00

    r1 = Degree(scale='ce', temp=0.0)
    r2 = Degree(scale='ke', temp=0.0)
    r1 += r2
    assert r1.scale == 'ce'
    assert r1.temp == -273.15

    r1 = Degree(scale='ra', temp=0.0)
    r2 = Degree(scale='ke', temp=0.0)
    r1 += r2
    assert r1.scale == 'ra'
    assert r1.temp == 0.00

    r1 = Degree(scale='ke', temp=0.0)
    r2 = Degree(scale='ra', temp=0.0)
    r1 += r2
    assert r1.scale == 'ke'
    assert r1.temp == 0.00


def test_sub():
    r1 = Degree(scale='ce', temp=1.0)
    r2 = Degree(scale='ce', temp=2.0)
    r = r1 - r2
    assert r.scale == 'ce'
    assert r.temp == -1.00

    r1 = Degree(scale='fa', temp=1.0)
    r = r1 - 2.00
    assert r.scale == 'fa'
    assert r.temp == -1.00

    r1 = Degree(scale='ce', temp=1.0)
    r2 = Degree(scale='ce', temp=1.0)
    r1 -= r2
    assert r1.scale == 'ce'
    assert r1.temp == 0.00

    r1 = Degree(scale='fa', temp=0.0)
    r2 = Degree(scale='ce', temp=0.0)
    r1 = r1 - r2
    assert r1.scale == 'fa'
    assert r1.temp == -32.00

    r1 = Degree(scale='ke', temp=0.0)
    r2 = Degree(scale='ra', temp=0.0)
    r1 = r1 - r2
    assert r1.scale == 'ke'
    assert r1.temp == 0.00

    r1 = Degree(scale='ra', temp=0.0)
    r2 = Degree(scale='ke', temp=0.0)
    r1 = r1 - r2
    assert r1.scale == 'ra'
    assert r1.temp == 0.00


def test_mul():
    r1 = Degree(scale='ce', temp=2.0)
    r = r1 * 10
    assert r.scale == 'ce'
    assert r.temp == 20.00

    r1 = Degree(scale='fa', temp=2.0)
    r = 20 * r1
    assert r.scale == 'fa'
    assert r.temp == 40.00

    r1 = Degree(scale='ke', temp=2.0)
    r = 20 * r1
    assert r.scale == 'ke'
    assert r.temp == 40.00

    r1 = Degree(scale='ra', temp=20.0)
    r = r1 * 2
    assert r.scale == 'ra'
    assert r.temp == 40.00


def test_div():
    r1 = Degree(scale='ce', temp=2.0)
    r = r1 / 10
    assert r.scale == 'ce'
    assert r.temp == 0.20

    r1 = Degree(scale='fa', temp=10.0)
    r = r1 / 10
    assert r.scale == 'fa'
    assert r.temp == 1.0

    r1 = Degree(scale='ke', temp=5.0)
    r = r1 / 2
    assert r.scale == 'ke'
    assert r.temp == 2.5

    r1 = Degree(scale='ra', temp=10.0)
    r = r1 / 2
    assert r.scale == 'ra'
    assert r.temp == 5.0


def test_str():
    r = Degree('ce')
    assert str(r) == '0.0 °C'

    r.scale = 'fa'
    r.temp = 0
    assert str(r) == '0.0 °F'

    r.scale = 'ke'
    r.temp = 0
    assert str(r) == '0.0 K'

    r.scale = 'ra'
    r.temp = 0
    assert str(r) == '0.0 °Ra'


def test_repr():
    r = Degree('ce')
    assert repr(r) == 'Degree(\'ce\', 0.0)'

    r.scale = 'fa'
    r.temp = 0
    assert repr(r) == 'Degree(\'fa\', 0.0)'

    r.scale = 'ke'
    r.temp = 0
    assert repr(r) == 'Degree(\'ke\', 0.0)'

    r.scale = 'ra'
    r.temp = 0
    assert repr(r) == 'Degree(\'ra\', 0.0)'
