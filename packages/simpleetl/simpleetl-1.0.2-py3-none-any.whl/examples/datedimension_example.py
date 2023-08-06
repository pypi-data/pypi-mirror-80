import datetime
from math import ceil

from pygrametl import getvalue

from simpleetl import Dimension
from simpleetl import datatypes

# Define a "default" date, when no date is found.
nulldate = {}
nulldt = -1
nulldate["date"] = None
nulldate["holiday"] = False
for r in ["datekey", "year", "month", "day", "quarter", "weekday", "iso_year", "iso_weeknumber",
          "iso_weekday", "month_str", "day_us_str", "season", "season_us_str"]:
    nulldate[r] = -1


def _datehandling(row, namemapping):
    """ A method for handling and converting date formats from a string and
        exploding and adding it to a dictionary.

    :param row: The data dictionary, which contains the raw date, but which
                the output is going to be applied to too.
    :param namemapping: A dictionary describing key mappings of the input
                        dictionary.
    :return: A dictionary, containing values for the dimdate dimension.
    """
    datekey = getvalue(row, 'datekey', namemapping)

    if datekey is None or datekey == nulldt:
        return nulldate
    dt = datetime.datetime.strptime(str(datekey), "%Y%m%d", )
    outrow = {}

    outrow['day'] = dt.day
    outrow['month'] = dt.month
    outrow['year'] = dt.year
    outrow['quarter'] = ceil(dt.month / 3)
    outrow['weekday'] = dt.weekday()
    (outrow["iso_year"],
     outrow['iso_weeknumber'],
     outrow['iso_weekday']) = dt.isocalendar()
    outrow['datekey'] = dt.year * 10000 + dt.month * 100 + dt.day
    outrow['date'] = dt.strftime("%Y-%m-%d")
    wds = ["Mandag", "Tirsdag", "Onsdag",
           "Torsdag", "Fredag", "Lørdag", "Søndag"]

    mrds = ["Januar", "Februar", "Marts", "April", "Maj", "Juni", "Juli", "August", "September", "Oktober", "November",
            "December"]
    outrow["month_str"] = mrds[dt.month - 1]
    outrow["day_us_str"] = wds[dt.weekday()]
    outrow["holiday"] = False
    # import holidays
    # dk_holidays = holidays.Denmark()
    # dt in dk_holidays or (dt.month == 12 and dt.day in (24, 31))
    season = 0
    if 3 <= dt.month <= 5:
        season = 1
    elif 6 <= dt.month <= 8:
        season = 2
    elif 9 <= dt.month <= 11:
        season = 3
    seasons = ["Vinter", "Forår", "Sommer", "Efterår"]
    outrow["season"] = season
    outrow["season_us_str"] = seasons[season]

    return outrow


dimdate = Dimension(schema="testschema", table="dimdate", key="datekey",
                    rowexpander=_datehandling, integerkey=True)

dimdate.add_lookupatt("datekey", datatypes.datekey, nulldt)

dimdate.add_att('year', datatypes.smallint)
dimdate.add_att('month', datatypes.smallint)
dimdate.add_att('day', datatypes.smallint)
dimdate.add_att('weekday', datatypes.smallint)
dimdate.add_att('iso_weeknumber', datatypes.smallint)
dimdate.add_att('iso_weekday', datatypes.smallint)
dimdate.add_att('iso_year', datatypes.smallint)
dimdate.add_att('quarter', datatypes.smallint)

dimdate.add_att('season_us_str', datatypes.text)
dimdate.add_att('day_us_str', datatypes.text)
dimdate.add_att('month_str', datatypes.text)

dimdate.add_att("date", datatypes.date)
dimdate.add_att("holiday", datatypes.boolean)
