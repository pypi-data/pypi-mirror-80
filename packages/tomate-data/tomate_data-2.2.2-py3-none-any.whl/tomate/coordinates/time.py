"""Coordinate managing dates and time.

Use user settings to set locales.
"""

# This file is part of the 'tomate' project
# (http://github.com/Descanonge/tomate) and subject
# to the MIT License as defined in the file 'LICENSE',
# at the root of this project. © 2020 Clément HAËCK


import locale
import logging
from typing import List, Sequence, Union, Tuple

try:
    import cftime
except ImportError:
    _has_cftime = False
else:
    _has_cftime = True

from tomate.coordinates.coord import Coord
from tomate.custom_types import KeyLike


log = logging.getLogger(__name__)
locale.setlocale(locale.LC_ALL, '')


class Time(Coord):
    """Time coordinate.

    Values are stored as floats, and can be converted
    to datetime objects.
    All conversion are done with the cftime package.
    The standard CF calendar is used. Using a different
    calendar is not presently supported, but can be implemented.
    This coordinate needs units, which must  be CF compliant.
    See `<http://cfconventions.org>`__.

    Use user settings to set locales.

    :attr units: str: CF-compliant time units.
    :attr calendar: str: CF-compliant calendar. Defaults to 'standard'.
    """
    def __init__(self, name: str = 'time', array: Sequence = None,
                 units: str = None, fullname: str = None,
                 calendar: str = 'standard'):
        if not _has_cftime:
            raise ImportError("cftime package necessary for using Time coordinate.")
        super().__init__(name, array, units=units, fullname=fullname)
        if self.units == '':
            raise ValueError("Time coordinate must be supplied"
                             " CF-compliant units.")

        self.calendar = calendar

    def get_extent_str(self, slc: KeyLike = None) -> str:
        if self.size == 1:
            return self.format(self.index2date(0))
        return "{} - {}".format(*[self.format(v)
                                  for v in self.index2date(slc)[[0, -1]]])

    def index2date(self, indices: KeyLike = None,
                   pydate: bool = False) -> Union['cftime.datetime',
                                                  List['cftime.datetime']]:
        """Return datetimes objects corresponding to indices.

        :param indices: [opt] If None, all datetimes are taken.
        :param pydate: If True, return datetime.datetime object, rather than
            cftime objects.
        :returns: Return a list if the input was a list.
        """
        if indices is None:
            indices = slice(None, None)

        if pydate:
            dates = cftime.num2pydate(self[indices], self.units, self.calendar)
        else:
            dates = cftime.num2date(self[indices], self.units, self.calendar)
        return dates

    @staticmethod
    def change_units_other(values: Sequence[float], old: str, new: str,
                           calendar: str = 'standard'):
        """Change time units."""
        dates = cftime.num2date(values, old, calendar)
        values = cftime.date2num(dates, new, calendar)
        return values

    def get_index(self, value: Union['cftime.datetime',
                                     Tuple[Union[int]], float],
                  loc: str = 'closest') -> int:
        """Return index of value.

        :param value: Time value, can be timestamps corresponding to
            self units, datetime object, or a list of values that
            can be transformed to date
            ([year, month, day [, hours, minutes, ...]])
        :param loc: {'closest', 'below', 'above'}
            Works as for Coord.get_index.
        """
        if isinstance(value, (list, tuple)):
            value = cftime.datetime(*value, calendar=self.calendar)
        if isinstance(value, cftime.datetime):
            value = cftime.date2num(value, self.units, self.calendar)
        return super().get_index(value, loc)

    def get_index_by_day(self, value: Union['cftime.datetime',
                                            Tuple[Union[int, float]],
                                            float, int],
                         loc: str = 'closest') -> int:
        """Get index of value on the same day only.

        :raises IndexError: If no timestamp is found on the same day with
            specified loc.
        :raises TypeError: If `loc` is not valid.
        """
        if isinstance(value, (list, tuple)):
            value = cftime.datetime(*value, calendar=self.calendar)
        if isinstance(value, cftime.datetime):
            value = cftime.date2num(value, self.units, self.calendar)

        date = to_date(cftime.num2date(value, self.units, self.calendar))
        if loc == 'below':
            idx = self.get_index(value, loc=loc)
            if to_date(self.index2date(idx)) != date:
                raise IndexError("No timestamp below on same day.")
            return idx
        if loc == 'above':
            idx = self.get_index(value, loc=loc)
            if to_date(self.index2date(idx)) != date:
                raise IndexError("No timestamp above on same day.")
            return idx
        if loc == 'closest':
            lo = self.get_index(value, loc='below')
            hi = self.get_index(value, loc='above')
            same_day = [to_date(self.index2date(idx)) == date
                        for idx in [lo, hi]]
            if all(same_day):
                if (self[hi] - value) < (value - self[lo]):
                    return hi
                return lo
            if same_day[0]:
                return lo
            if same_day[1]:
                return hi
            raise IndexError("No timestamp on same day.")

        raise TypeError("Invalid loc type."
                        " Expected one of: 'left', 'right', 'closest'")

    def get_indices_by_day(self, values: Sequence[float],
                           loc: str = 'closest') -> List[int]:
        """Return indices of the elements closest to values.

        Selection indices only on the same day as values.
        """
        indices = [self.get_index_by_day(v, loc) for v in values]
        return indices

    def subset_by_day(self,
                      dmin: Union['cftime.datetime', List[int],
                                  float, int] = None,
                      dmax: Union['cftime.datetime', List[int],
                                  float, int] = None,
                      exclude: bool = False) -> slice:
        """Return slice between dmin and dmax.

        Select whole days. Only date part of `dmin` and `dmax` is
        considered. This avoids some surprises when time is not 00:00:00
        on timestamps, or allow to work by day when they are multiple
        timestamp per day.

        :param: Exclude `dmin` and `dmax` of the selection if True.
            Selection still only consists of whole days.
        """
        if self.is_descending():
            raise TypeError("subset_by_day not supported for descending"
                            " coordinates.")

        indices = []
        for i, date in enumerate([dmin, dmax]):
            if date is None:
                idx = [0, self.size-1][i]
            else:
                locs = ['below', 'above']
                if i == 1:
                    locs.reverse()
                loc = locs[exclude]
                try:
                    idx = self.get_index_by_day(date, loc='closest')
                except IndexError:
                    idx = self.get_index(date, loc=loc)

                inv = {'above': 1, 'below': -1}[loc]
                while ((idx < self.size-1 if inv == 1 else idx > 0)
                       and to_date(self.index2date(idx))
                       == to_date(self.index2date(idx+inv))):
                    idx += inv
                if exclude:
                    idx += inv
            indices.append(idx)
        indices[1] += 1

        slc = slice(*indices, 1)

        return slc

    @staticmethod
    def format(value: float, fmt: str = None) -> str:
        """Format value.

        :param fmt: Passed to string.format or datetime.strftime
        """
        if isinstance(value, cftime.datetime):
            if fmt is None:
                fmt = '%x %X'
            return value.strftime(fmt)
        if fmt is None:
            fmt = '{:.2f}'
        return fmt.format(value)


def to_date(date: 'cftime.datetime'):
    """Remove time part."""
    return cftime.datetime(date.year, date.month, date.day,
                           calendar=date.calendar)
