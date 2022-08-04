DAYNAME_SHORT = "%a"
DAYNAME_LONG = "%A"
# 0 is Sunday
WEEKDAY_NUM = "%w"
DAY = "%d"

MONTHNAME_SHORT = "%b"
MONTHNAME_LONG = "%B"
MONTH = "%m"

YEAR = "%Y"
HOUR_24 = "%H"
HOUR_12 = "%I"

AM_PM = "%p"
MINUTE = "%M"
SECOND = "%S"


DATE_UI = DAY + "-" + MONTHNAME_SHORT + "-" + YEAR
DATE_INTERNAL = YEAR + "-" + MONTH + "-" + DAY
DATE_USER_INPUT = DATE_INTERNAL

TIME_12 = HOUR_12 + ":" + MINUTE + " " + AM_PM
TIME_12_SECONDS = HOUR_12 + ":" + MINUTE + ":" + SECOND + " " + AM_PM

TIME_24 = HOUR_24 + ":" + MINUTE
TIME_12_SECONDS = HOUR_12 + ":" + MINUTE + ":" + SECOND

TIME_UI = TIME_12


def formatter(dtformat, default=''):
    """
    Returns a function take formats a python datetime object according to the given format string
    """
    def _func(datetime_obj):
        if datetime_obj is None:
            return default
        return datetime_obj.strftime(dtformat)
    
    return _func
