"""Temperatures conversions.

This module helps to create and manage Degree type objects.

Copyright (c) 2020 Thierry P.G. DECKER
All Rights Reserved.
Released under the MIT license

"""


class Degree:
    """Degree class.

    Exemples:

        Create Degree object:

            >>> Degree()
            Degree('ce', 0.0)
            >>> Degree(temp=10)
            Degree('ce', 10.0)
            >>> Degree(scale='fa')
            Degree('fa', 0.0)
            >>> Degree(scale='ke', temp=5)
            Degree('ke', 5.0)

        Additions:

            >>> Degree('fa', 10) + 1
            Degree('fa', 11.0)
            >>> r = Degree('fa', 10)
            >>> r += 1
            >>> r
            Degree('fa', 11.0)
            >>> 1 + Degree('ke', 10)
            Degree('ke', 11.0)
            >>> Degree('fa', 10) + Degree('fa', 10)
            Degree('fa', 20.0)
            >>> Degree('ce', 0) + Degree('fa', 32)
            Degree('ce', 0.0)

        Substractions (not commutative operation):

            >>> Degree('fa', 10) - 1
            Degree('fa', 9.0)
            >>> r = Degree('ke', 10)
            >>> r -= 1
            >>> r
            Degree('ke', 9.0)
            >>> Degree('ce', 0) - Degree('ke', 0)
            Degree('ce', 273.15)

        Multiplications:

            >>>Degree('ce', 10) * 2
            Degree('ce', 20.0)
            >>>3 * Degree('fa', 1)
            Degree('fa', 3.0)

        Divisions (not commutative operation):

            >>>Degree('ke', 10) / 2
            Degree('ce', 5.0)

        Representations:

            >>> str(Degree('fa', 1100.15))
            '1100.15 °F'
            >>> str(Degree('ke', 10.00))
            '10.00 K'
            >>> repr(Degree('ke', 100.15))
            "Degree('ke', 100.15)"

        Properties:

            >>> r = Degree('ce', 0)
            >>> r.celcius
            0.0
            >>> r.fahrenheit
            32.00
            >>> r = Degree('ce', 0)
            >>> r.scale = 'fa'
            >>> r.temp
            32.0

        Static methods:

            Temperature coversions:

                >>> Degree.conv_ce_to_fa(10)
                50.0
                >>> Degree.conv_ce_to_ke(0)
                273.15
                >>> Degree.conv_fa_to_ce(32)
                0.0
                >>> Degree.conv_fa_to_ke(32)
                273.15


    """
    _scales = {
        #
        # Supported scales
        #
        'ce',  # Celcius
        'fa',  # Fahrenheit
        'ke',  # Kelvin
        'ra'  # Rankine
    }

    def __init__(self, scale='ce', temp=0.):
        """Initialize new Degree instances.

        Raises:
            NameError if the given scale is not supported.
        """
        if scale not in self._scales:
            raise NameError(scale)
        self._scale = scale
        self._temp = float(temp)

    def __add__(self, other):
        new_scale = self.scale
        new_temp = self.temp
        if isinstance(other, Degree):
            if self.scale == 'ce':
                new_temp += other.celcius
            elif self.scale == 'fa':
                new_temp += other.fahrenheit
            elif self.scale == 'ke':
                new_temp += other.kelvin
            elif self.scale == 'ra':
                new_temp += other.rankine
        else:
            new_temp += float(other)
        return Degree(scale=new_scale, temp=new_temp)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        new_scale = self.scale
        new_temp = self.temp
        if isinstance(other, Degree):
            if self.scale == 'ce':
                new_temp -= other.celcius
            elif self.scale == 'fa':
                new_temp -= other.fahrenheit
            elif self.scale == 'ke':
                new_temp -= other.kelvin
            elif self.scale == 'ra':
                new_temp -= other.rankine
        else:
            new_temp -= float(other)
        return Degree(scale=new_scale, temp=new_temp)

    def __mul__(self, other):
        return Degree(scale=self.scale, temp=self.temp * float(other))

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        return Degree(scale=self.scale, temp=self.temp / float(other))

    def __str__(self):
        if self.scale == 'ce':
            return f'{self.temp} °C'
        if self.scale == 'fa':
            return f'{self.temp} °F'
        if self.scale == 'ke':
            return f'{self.temp} K'
        if self.scale == 'ra':
            return f'{self.temp} °Ra'

    def __repr__(self):
        return f'Degree(\'{self.scale}\', {self.temp})'

    @property
    def scales(self):
        """Supported temperature scales.

        Returns:
            A set of the managed scales.
        """
        return self._scales

    @property
    def scale(self):
        """Scale of the object.

        Returns:
            A string containing a scale included in the supported scales set.
        """
        return self._scale

    @scale.setter
    def scale(self, scale):
        """Set the scale

        Set the scale value and convert the temperature value in the new scale.

        Raises:
             NameError if the given scale is not supported.
        """
        if scale not in self._scales:
            raise NameError(scale)

        if scale != self._scale:

            if self._scale == 'ce' and scale == 'fa':
                self._temp = self.conv_ce_to_fa(temp=self._temp)
            if self._scale == 'ce' and scale == 'ke':
                self._temp = self.conv_ce_to_ke(temp=self._temp)
            if self._scale == 'ce' and scale == 'ra':
                self._temp = self.conv_ce_to_ra(temp=self._temp)

            if self._scale == 'fa' and scale == 'ce':
                self._temp = self.conv_fa_to_ce(temp=self._temp)
            if self._scale == 'fa' and scale == 'ke':
                self._temp = self.conv_fa_to_ke(temp=self._temp)
            if self._scale == 'fa' and scale == 'ra':
                self._temp = self.conv_fa_to_ra(temp=self._temp)

            if self._scale == 'ke' and scale == 'ce':
                self._temp = self.conv_ke_to_ce(temp=self._temp)
            if self._scale == 'ke' and scale == 'fa':
                self._temp = self.conv_ke_to_fa(temp=self._temp)
            if self._scale == 'ke' and scale == 'ra':
                self._temp = self.conv_ke_to_ra(temp=self._temp)

            if self._scale == 'ra' and scale == 'ce':
                self._temp = self.conv_ra_to_ce(temp=self._temp)
            if self._scale == 'ra' and scale == 'fa':
                self._temp = self.conv_ra_to_fa(temp=self._temp)
            if self._scale == 'ra' and scale == 'ke':
                self._temp = self.conv_ra_to_ke(temp=self._temp)

            self._scale = scale

    @property
    def temp(self):
        """Temperature of the object.

        The temperature is stored in the scale of the object.

        returns:
            A float containing the temperature of the object.
        """
        return self._temp

    @temp.setter
    def temp(self, temp):
        """Set the temperature

        """
        if float(temp) != self._temp:
            self._temp = float(temp)

    @property
    def celcius(self):
        """Celcius value.

        Returns:
            A float containg the Celcius value.
        """
        if self._scale == 'ce':
            return self._temp
        if self._scale == 'fa':
            return self.conv_fa_to_ce(self._temp)
        if self._scale == 'ke':
            return self.conv_ke_to_ce(self._temp)
        if self._scale == 'ra':
            return self.conv_ra_to_ce(self._temp)

    @property
    def fahrenheit(self):
        """Fahrenheit value.

        Returns:
            A float containing the Fahrenheit value.
        """
        if self._scale == 'ce':
            return self.conv_ce_to_fa(self._temp)
        if self._scale == 'fa':
            return self._temp
        if self._scale == 'ke':
            return self.conv_ke_to_fa(self._temp)
        if self._scale == 'ra':
            return self.conv_ra_to_fa(self._temp)

    @property
    def kelvin(self):
        """Kelvin value.

        Returns:
            A float containing the Kelvine value.
        """
        if self._scale == 'ce':
            return self.conv_ce_to_ke(self._temp)
        if self._scale == 'fa':
            return self.conv_fa_to_ke(self._temp)
        if self._scale == 'ke':
            return self._temp
        if self._scale == 'ra':
            return self.conv_ra_to_ke(self._temp)

    @property
    def rankine(self):
        """Fahrenheit value.

        Returns:
            A float containing the Fahrenheit value.
        """
        if self._scale == 'ce':
            return self.conv_ce_to_ra(self._temp)
        if self._scale == 'fa':
            return self.conv_fa_to_ra(self._temp)
        if self._scale == 'ke':
            return self.conv_ke_to_ra(self.temp)
        if self._scale == 'ra':
            return self._temp

    @staticmethod
    def conv_ce_to_fa(temp):
        """Convert Celcius value to Fahrenheit.

        Args:
            temp: A float containing the Celcius value to convert.

        Returns:
            A float containing the Fahrenheit value.
        """
        return ((9 * temp) / 5) + 32

    @staticmethod
    def conv_ce_to_ke(temp):
        """Convert Celcius value to Kelvin.

        Args:
            temp: A float containing the Celcius value to convert.

        Returns:
            A float containing the Kelvin value.
        """
        return temp + 273.15

    @staticmethod
    def conv_ce_to_ra(temp):
        """Convert Celcius value to Rankine.

        Args:
            temp: A float containing the Celcius value to convert.

        Returns:
            A float containing the Rankine value.
        """
        return temp * 1.8 + 32 + 459.67

    @staticmethod
    def conv_fa_to_ce(temp):
        """Convert Fahrenheit value to Celcius.

        Args:
            temp: A float containing the Fahrenheit value.

        returns:
            A Float containing the Celcius value.
        """
        return ((temp - 32) * 5) / 9

    @staticmethod
    def conv_fa_to_ke(temp):
        """Convert Fahrenheit value to Kelvin.

        Args:
            temp: A float containing the Fahrenheit value.

        returns:
            A Float containing the Kelvin value.
        """
        return ((temp + 459.67) * 5) / 9

    @staticmethod
    def conv_fa_to_ra(temp):
        """Convert Fahrenheit value to Rankine.

        Args:
            temp: A float containing the Fahrenheit value.

        returns:
            A Float containing the Rankine value.
        """
        return temp + 459.67

    @staticmethod
    def conv_ke_to_ce(temp):
        """Convert Kelvin value to Celcius.

        Args:
            temp: A float containing the Kelvin value.

        returns:
            A Float containing the Celcius value.
        """
        return temp - 273.15

    @staticmethod
    def conv_ke_to_fa(temp):
        """Convert Kelvin value to Fahrenheit.

        Args:
            temp: A float containing the Kelvin value.

        returns:
            A Float containing the Fahrenheit value.
        """
        return ((9 * temp) / 5) - 459.67

    @staticmethod
    def conv_ke_to_ra(temp):
        """Convert Kelvin value to Fahrenheit.

        Args:
            temp: A float containing the Kelvin value.

        returns:
            A Float containing the Rankine value.
        """
        return temp * 1.8

    @staticmethod
    def conv_ra_to_ce(temp):
        """Convert Rankine value to Celcius.

        Args:
            temp: A float containing the Rankine value.

        returns:
            A Float containing the Celcius value.
        """
        return (temp - 459.67 - 32) / 1.8

    @staticmethod
    def conv_ra_to_fa(temp):
        """Convert Rankine value to Fahrenheit.

        Args:
            temp: A float containing the Rankine value.

        returns:
            A Float containing the Fahrenheit value.
        """
        return temp - 459.67

    @staticmethod
    def conv_ra_to_ke(temp):
        """Convert Rankine value to Fahrenheit.

        Args:
            temp: A float containing the Rankine value.

        returns:
            A Float containing the Kelvin value.
        """
        return temp / 1.8
