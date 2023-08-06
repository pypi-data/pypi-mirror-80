import simpleetl._functions._datatypefuncs as _tfuncs
from simpleetl import LOG as _LOG

from simpleetl._modules.Datatype import Datatype as _Datatype

smallint = _Datatype("smallint", _tfuncs.is_smallint)
smallint_notnull = _Datatype("smallint", _tfuncs.is_smallint, False)

int = _Datatype("integer", _tfuncs.is_int)
int_notnull = _Datatype("integer", _tfuncs.is_int, False)

bigint = _Datatype("bigint", _tfuncs.is_bigint)
bigint_notnull = _Datatype("bigint", _tfuncs.is_bigint, False)

numeric7_2 = _Datatype("numeric(7,2)", _tfuncs.generate_is_numeric(7, 2))
numeric8_6 = _Datatype("numeric(8,6)", _tfuncs.generate_is_numeric(7, 2))
numeric3_1 = _Datatype("numeric(3,1)", _tfuncs.generate_is_numeric(3, 1))


def varchar(length):
    if length < 1:
        _LOG.error("varchar length must be at least 1")
    return _Datatype("varchar(" + str(length) + ")", _tfuncs.generate_is_varchar(length))


text = _Datatype("text", _tfuncs.is_text)
text_notnull = _Datatype("text", _tfuncs.is_text, True)
textlower = _Datatype("text", _tfuncs.is_textlower)
textlower_notnull = _Datatype("text", _tfuncs.is_textlower, True)
textupper = _Datatype("text", _tfuncs.is_textupper)
textupper_notnull = _Datatype("text", _tfuncs.is_textupper, True)

timekey = _Datatype("integer", _tfuncs.is_timekey)
time = _Datatype("time without time zone", _tfuncs.is_text)
timestamp = _Datatype("timestamp without time zone", _tfuncs.is_timestamp)
timestamp_with_timezone = _Datatype("timestamp with time zone", _tfuncs.is_timestamp)

boolean = _Datatype("boolean", _tfuncs.is_boolean)

datekey = _Datatype("integer", _tfuncs.is_datekey)
date = _Datatype("date", _tfuncs.is_text)

geography = _Datatype("geography", _tfuncs.is_text)

jsonb = _Datatype("jsonb", _tfuncs.injson)

xml = _Datatype("xml", _tfuncs.inxml)

numeric18_10 = _Datatype("numeric(18,10)", _tfuncs.generate_is_numeric(18, 10))

uuid = _Datatype("uuid", _tfuncs.is_uuid)
intarray = _Datatype("INTEGER[]", _tfuncs.is_intarray)
################################################################################
# spatial
################################################################################
# WGS-84
latitude = _Datatype('numeric(18,10)', _tfuncs.is_latitude)
# WGS-84
longitude = _Datatype('numeric(18,10)', _tfuncs.is_longitude)
# WGS-84
altitude = _Datatype('numeric(18,10)', _tfuncs.is_altitude)
# Compass direction/degree [0,360], assumed to be an integer
degree = _Datatype('int', _tfuncs.is_degree)

################################################################################
# XML Schema inspired basic data types
################################################################################
non_negative_int = _Datatype('int', _tfuncs.is_non_negative_int)
non_positive_int = _Datatype('int', _tfuncs.is_non_positive_int)
positive_int = _Datatype('int', _tfuncs.is_positive_int)
