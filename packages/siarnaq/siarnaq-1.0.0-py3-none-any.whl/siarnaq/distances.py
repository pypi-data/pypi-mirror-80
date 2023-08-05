"""Disances conversions.

Copyright (c) 2020 Thierry P.G. DECKER
All Rights Reserved.
Released under the MIT license

"""


class Distance:
    """Distance class.

    """
    _scales = {
        'km',  # Kilometer
        'mi',  # Mile
    }

    def __init__(self, scale='km', dist=0.):
        """Initialize new Distance instances.

        Raises:
            NameError if the given scale is not supported.
        """
        if scale not in self._scales:
            raise NameError(scale)
        self._scale = scale
        self._dist = float(dist)

    def __add__(self, other):
        new_scale = self.scale
        new_dist = self.dist
        if isinstance(other, Distance):
            if self.scale == 'km':
                new_dist += other.kilometer
            elif self.scale == 'mi':
                new_dist += other.mile
        else:
            new_dist += float(other)
        return Distance(scale=new_scale, dist=new_dist)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        new_scale = self.scale
        new_dist = self.dist
        if isinstance(other, Distance):
            if self.scale == 'km':
                new_dist -= other.kilometer
            elif self.scale == 'mi':
                new_dist -= other.mile
        else:
            new_dist -= float(other)
        return Distance(scale=new_scale, dist=new_dist)

    def __mul__(self, other):
        return Distance(scale=self.scale, dist=self.dist * float(other))

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        return Distance(scale=self.scale, dist=self.dist / float(other))

    def __str__(self):
        if self.scale == 'km':
            return f'{self.dist} km'
        if self.scale == 'mi':
            return f'{self.dist} mi'

    def __repr__(self):
        return f'Distance(\'{self.scale}\', {self.dist})'

    @property
    def scales(self):
        """Supported distances scales.

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

        Set the scale value and convert the distance value in the new scale.

        Raises:
             NameError if the given scale is not supported.
        """
        if scale not in self._scales:
            raise NameError(scale)

        if scale != self._scale:

            if self._scale == 'km' and scale == 'mi':
                self.dist = self.conv_km_to_mi(dist=self.dist)
            if self._scale == 'mi' and scale == 'km':
                self.dist = self.conv_mi_to_km(dist=self.dist)

            self._scale = scale

    @property
    def dist(self):
        """Distance of the object.

        Returns:
            A Float containing a distance included in the object's scale.
        """
        return self._dist

    @dist.setter
    def dist(self, dist):
        """Set The distance

        """
        if float(dist) != self._dist:
            self._dist = float(dist)

    @property
    def kilometer(self):
        """Kilometer value.

        Returns:
            A float containg the Kilometer value.
        """
        if self._scale == 'km':
            return self._dist
        if self._scale == 'mi':
            return self.conv_mi_to_km(self._dist)

    @property
    def mile(self):
        """Mile value.

        Returns:
            A float containg the Mile value.
        """
        if self._scale == 'km':
            return self.conv_km_to_mi(self._dist)
        if self._scale == 'mi':
            return self._dist

    @staticmethod
    def conv_km_to_mi(dist):
        """Convert Kilometer value to Mile.

        Args:
            dist: A float containing the Kilometer value to convert.

        Returns:
            A float containing the Mile value.
        """
        return dist / 1.609

    @staticmethod
    def conv_mi_to_km(dist):
        """Convert Mile value to Kilometer.

        Args:
            dist: A float containing the Mile value to convert.

        Returns:
            A float containing the Kilomeer value.
        """
        return dist * 1.609
