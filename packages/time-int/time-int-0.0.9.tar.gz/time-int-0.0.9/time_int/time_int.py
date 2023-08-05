from magic_kind import MagicKind
from math import floor
from calendar import timegm
from datetime import datetime, timedelta, timezone
from time import gmtime, struct_time, time, strftime

from typing import Dict, Callable, Union


class TimeTruncUnit(MagicKind):
    """Values to be used as arguments to TimeInt.trunc(num=1) method"""

    YEAR: str = "year"
    MONTH: str = "month"
    WEEK: str = "week"
    DAY: str = "day"
    HOUR: str = "hour"
    MINUTE: str = "minute"


class TimeInt(int):
    """Integer that represents a naive time since epoch."""

    MIN: int = 0  # Jan 1, 1970, start of epoch
    MAX: int = 32_503_680_000  # Jan 1, 3000
    UTC: timezone = timezone.utc

    def __new__(cls, value: Union[int, float, str]) -> "TimeInt":
        value = int(value)
        if cls.MIN <= value <= cls.MAX:
            return super().__new__(cls, value)
        else:
            raise ValueError(f"TimeInt value out of range: {value}")

    def get_struct_time(self) -> struct_time:
        """Get struct_time (time package)."""
        return gmtime(float(self))

    def get_datetime(self) -> datetime:
        """Get datetime (datetime package)."""
        return datetime.fromtimestamp(float(self), tz=self.UTC)

    @classmethod
    def from_struct_time(cls, st: struct_time) -> "TimeInt":
        """TimeInt from a struct_time object (time package)."""
        return TimeInt(timegm(st))

    @classmethod
    def from_datetime(cls, dt: datetime) -> "TimeInt":
        """TimeInt from a datetime object (datetime package)."""
        return TimeInt(timegm(dt.utctimetuple()))

    @classmethod
    def from_float_string(cls, epoch: str) -> "TimeInt":
        """TimeInt from string like "1590177600.000000000"""
        return cls(floor(float(epoch)))

    @classmethod
    def now(cls) -> "TimeInt":
        """Get the TimeInt for most recent second (e.g. we round down)."""
        return TimeInt(floor(time()))

    def get_pretty(self) -> str:
        """Get as formatted string leaving off parts that are 0 on end.

        For example, if the time lands on the hour, leave off minutes
        and seconds. If it happens to fall right on the second where
        a year changes, just give the year number etc.
        """
        st = gmtime(float(self))
        if st.tm_sec:
            form = "%Y-%m-%d %I:%M:%S %p"
        elif st.tm_min:
            form = "%Y-%m-%d %I:%M %p"
        elif st.tm_hour:
            form = "%Y-%m-%d %I %p"
        elif st.tm_mday != 1:
            form = "%Y-%m-%d"
        elif st.tm_mon != 1:
            form = "%Y-%m"
        else:
            form = "%Y"
        return strftime(form, st)

    def trunc(self, unit: str, num: int = 1) -> "TimeInt":
        """Combination of the trunc_* methods.

        Args:
            unit: One of the TimeTruncUnit values.
            num: like num arg in trunc_* methods, not valid for week.
        Raises:
            ValueError: if unit is not class attribute of TimeTruncUnit
            ValueError: if num is not greater than 0.
            ValueError: if unit is TimeTruncUnit.WEEK and num is anything but 1.
        Returns:
            Rounded down TimeInt value.
        """
        if unit not in TimeTruncUnit:
            expected = ", ".join(sorted([f'"{_}"' for _ in TimeTruncUnit]))
            raise ValueError(
                f'Got time trunc unit of "{unit}", but expected one of {expected}'
            )
        elif num < 1:
            raise ValueError(f"number of units must be int of 1 or more, but got {num}")
        elif num != 1 and unit == TimeTruncUnit.WEEK:
            raise ValueError(
                "When truncating to week, you can not specify a num "
                f"other than the default of 1, but got {num}"
            )
        if unit == TimeTruncUnit.WEEK:
            return self.trunc_week()
        else:
            return self._trunc_function_map[unit](self, num=num)

    @property
    def second(self) -> int:
        """Get seconds as an integer in range of 0 to 59."""
        return gmtime(float(self)).tm_sec

    @property
    def minute(self) -> int:
        """Get minute as an integer in range of 0 to 59."""
        return gmtime(float(self)).tm_min

    @property
    def hour(self) -> int:
        """Get hour day as an integer in range of 0 to 23."""
        return gmtime(float(self)).tm_hour

    @property
    def day(self) -> int:
        """Get day of the month as an integer in range of 1 to 31."""
        return gmtime(float(self)).tm_mday

    @property
    def weekday(self) -> int:
        """Get day of the week where Sunday is 0.

        datetime and time packages follow a convention where Monday is 0.
        But in our case of sticking with UTC rather than local timezones
        this has the undesirable result of working and market trading
        hours in time zones to the East (like Australia and Japan) starting
        before the week officially starts.

        In order to put business Mon-Fri workday hours all over the world
        in the same week, we change the at the start of Sunday UTC instead of
        the start of Monday UTC. Thus Sunday is 0 up to Friday being 6.
        """
        return (gmtime(float(self)).tm_wday + 1) % 7

    @property
    def month(self) -> int:
        """Get the month as an integer in range of 1 to 12."""
        return gmtime(float(self)).tm_mon

    @property
    def year(self) -> int:
        """Get the year as an integer, e.g. 1985 or 2012."""
        return gmtime(float(self)).tm_year

    def trunc_year(self, num: int = 1) -> "TimeInt":
        """Round TimeInt down to the start of year (or group of years).

        Args:
            num: round down to units of this many years since year 0. (Historically there
                 is no actual year 0, rather 1 B.C. is followed by 1 A.D. But for our
                 purposes we pretend, this means, for example, the year 2000 is grouped
                 as the start of the last century rather than the end of it).
        Returns:
            TimeInt at start of month, or group of num months.
        """
        st = gmtime(float(self))
        year = st.tm_year - (st.tm_year % num)
        values = (year, 1, 1, 0, 0, 0, 0, 0, 0)
        return TimeInt(timegm(struct_time(values)))

    def trunc_month(self, num: int = 1) -> "TimeInt":
        """Round TimeInt down to the start of month (or group of months).
        Args:
            num: round down to units of this many months since start of year.
        Returns:
            TimeInt at start of month, or group of num months.
        """
        st = gmtime(float(self))
        month = st.tm_mon - ((st.tm_mon - 1) % num)
        values = (st.tm_year, month, 1, 0, 0, 0, 0, 0, 0)
        return TimeInt(timegm(struct_time(values)))

    def trunc_week(self) -> "TimeInt":
        """Round TimeInt down to the start of latest Sunday."""
        dt = datetime.fromtimestamp(float(self), tz=self.UTC)
        # Note, for some reason weekday() from datetime has Monday as 0.
        # We tweak the results so that Sunday is 0 instead.
        week_day = (dt.weekday() + 1) % 7
        delta = timedelta(
            days=week_day, hours=dt.hour, minutes=dt.minute, seconds=dt.second
        )
        sunday_dt = dt - delta
        return TimeInt(int(sunday_dt.timestamp()))

    def trunc_day(self, num: int = 1) -> "TimeInt":
        """Round TimeInt down to the start of day (or group of days).

        Args:
            num: round down to units of this many days since start of month.
        Returns:
            TimeInt at start of day, or group of num days.
        """
        st = gmtime(float(self))
        day = st.tm_mday - ((st.tm_mday - 1) % num)
        values = (st.tm_year, st.tm_mon, day, 0, 0, 0, 0, 0, 0)
        return TimeInt(timegm(struct_time(values)))

    def trunc_hour(self, num: int = 1) -> "TimeInt":
        """Round TimeInt down to the start of hour (or group of hours).

        Args:
            num: round down to units of this many hours since start of day.
        Returns:
            TimeInt at start of hour, or group of num hours.
        """
        st = gmtime(float(self))
        hour = st.tm_hour - (st.tm_hour % num)
        values = (st.tm_year, st.tm_mon, st.tm_mday, hour, 0, 0, 0, 0, 0)
        return TimeInt(timegm(struct_time(values)))

    def trunc_minute(self, num: int = 1) -> "TimeInt":
        """Round TimeInt down to the start of minute (or group of minutes).

        Args:
            num: round down to units of this many hours since start of day.
        Returns:
            TimeInt at start of minute, or group of num minutes.
        """
        st = gmtime(float(self))
        minute = st.tm_min - (st.tm_min % num)
        values = (st.tm_year, st.tm_mon, st.tm_mday, st.tm_hour, minute, 0, 0, 0, 0)
        return TimeInt(timegm(struct_time(values)))

    _trunc_function_map: Dict[str, Callable] = {
        TimeTruncUnit.YEAR: trunc_year,
        TimeTruncUnit.MONTH: trunc_month,
        TimeTruncUnit.WEEK: trunc_week,
        TimeTruncUnit.DAY: trunc_day,
        TimeTruncUnit.HOUR: trunc_hour,
        TimeTruncUnit.MINUTE: trunc_minute,
    }


# Convert MIN and MAX from regular ints to TimeInt
TimeInt.MIN = TimeInt(TimeInt.MIN)
TimeInt.MAX = TimeInt(TimeInt.MAX)
