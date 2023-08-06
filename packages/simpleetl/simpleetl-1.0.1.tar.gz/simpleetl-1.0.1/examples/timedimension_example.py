import time

from pygrametl import getvalue

from simpleetl import Dimension
from simpleetl import datatypes, LOG

nulltime = {}
nulltime["time"] = None
for t in ["timekey", "hour", "minute", "quarter", "five_minute", "quarter_str", "five_minute_str", "min_from_midnight"]:
    nulltime[t] = -1


def _timehandling(row, namemapping):
    """Convert time formats before applying to dimensions.

    :param row: The data dictionary, which contains the raw date, but which
                the output is going to be applied to too.
    :param namemapping: A dictionary describing key mappings of the input
                        dictionary.
    :return: A dictionary, containing values for the dimtime dimension.
    """
    timest = getvalue(row, 'timekey', namemapping)
    if str(timest) == "-1" or timest is None:
        return nulltime

    thistime = str(timest).rjust(4, "0")
    try:
        (_, _, _, hour, minute, _, _, _, _) = time.strptime(thistime, "%H%M")
    except ValueError as err:
        LOG.warning("Unexpected time format! " + str(timest) + " - " + str(thistime))
        return nulltime

    outrow = {}
    outrow['timekey'] = row["timekey"]
    outrow['hour'] = hour
    outrow['minute'] = minute
    outrow['time'] = ":".join([str(hour), str(minute).rjust(2, "0"), "00"])
    outrow["quarter"] = hour * 4 + int(minute / 15)
    outrow["five_minute"] = hour * 12 + int(minute / 5)
    outrow["quarter_str"] = ":".join([str(hour).rjust(2, "0"),
                                      str(int(minute / 15) * 15).rjust(2, "0")])
    outrow["five_minute_str"] = ":".join([str(hour).rjust(2, "0"),
                                          str(int(minute / 5) * 5).rjust(2, "0")])
    outrow["min_from_midnight"] = hour * 60 + minute

    return outrow


dimtime = Dimension(schema="testschema", table="dimtime", key="timekey",
                    rowexpander=_timehandling, integerkey=True)

dimtime.add_lookupatt("timekey", datatypes.timekey, -1)

dimtime.add_att('hour', datatypes.smallint)
dimtime.add_att('minute', datatypes.smallint)
dimtime.add_att('quarter', datatypes.smallint)
dimtime.add_att('five_minute', datatypes.smallint)
dimtime.add_att('min_from_midnight', datatypes.smallint)

dimtime.add_att('quarter_str', datatypes.text)
dimtime.add_att('five_minute_str', datatypes.text)

dimtime.add_att("time", datatypes.time)
