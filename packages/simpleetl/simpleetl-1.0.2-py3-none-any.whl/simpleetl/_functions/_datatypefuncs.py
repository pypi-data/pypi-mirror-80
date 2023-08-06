import datetime
import json
import uuid
import xml.etree.ElementTree as ET
from decimal import Decimal


def is_timestamp(x):
    if isinstance(x, datetime.datetime) or x is None:
        return x

    raise ValueError("is_timestamp should receive datetime.datetime, input type is " + str(type(x)))


def is_timestamptz(x):
    dt = is_timestamp(x)
    if dt is None or (dt.tzinfo is not None and dt.tzinfo.utcoffset(dt) is not None):
        return dt
    raise ValueError("Time stamp has not time zone information: " + str(x))


def is_timekey(x):
    if isinstance(x, int):
        return x
    raise ValueError("timekey should receive integer representation, input type is " + str(type(x)))

    return None


def is_datekey(x):
    if isinstance(x, int):
        return x

    raise ValueError("datekey should receive pre-processed integer datekey, input type is " + str(type(x)))


def generate_is_varchar(length):
    def is_varchar(x):
        x = is_text(x)
        if len(x) > length:
            raise ValueError("varchar(" + str(length) + ") overflow: " + x)
        return x

    return is_varchar


def is_text(x, postfunc=None):
    #x = x.replace("\t", "\\t").replace("\n", "\\n").replace("\r", "\\r").strip()
    x = x.strip()
    if x is not None and postfunc:
        x = postfunc(x)
    return x


def is_textlower(x):
    return is_text(x, str.lower)


def is_textupper(x):
    return is_text(x, str.upper)


def is_bigint(x):
    if not isinstance(x, int):
        x = str(x).strip()
        try:
            x = int(x)
        except ValueError:
            return None
    if -9223372036854775808 <= x <= 9223372036854775807:
        return x
    else:
        raise ValueError("Bigint out of range", x)


def is_int(x):
    x = is_bigint(x)
    if x is None:
        return None
    if -2147483648 <= x <= 2147483647:  # We only want 32 bit signed integers
        return x
    else:
        raise ValueError("Integer out of range", x)


def is_boolean(x):
    if x == False or x == True:
        return x
    else:
        raise ValueError("Invalid boolean", x)


def is_uuid(x):
    try:
        return str(uuid.UUID(x))
    except ValueError as err:
        raise ValueError("Invalid UUID", x)


def is_intarray(x):
    if not isinstance(x, list):
        raise ValueError("Intarray must be list, got", type(x))
    data = str([str(int(n)) for n in x])

    return data.replace('[', '{').replace(']', '}').replace('\'', '\"')


################################################################################
# spatial
################################################################################
def is_latitude(x):
    try:
        x = float(x)
        if -90 <= x <= 90:
            return x
        else:
            raise ("Out of Earth latitude", x)
    except ValueError:
        raise ValueError("Not a float", x)


def is_longitude(x):
    try:
        x = float(x)
        if -180 <= x <= 180:
            return x
        else:
            raise ("Out of Earth logitude", x)
    except ValueError:
        raise ValueError("Not a float", x)


def is_altitude(x):
    try:
        x = float(x)
        if -1000 <= x <= 10000:
            return x
        else:
            raise ("Out of Earth altitude", x)
    except ValueError:
        raise ValueError("Not a float", x)


def is_degree(x):
    try:
        x = int(x)
        if 0 <= x < 360:
            return x
        else:
            raise ("Degree not in 0-360 range", x)
    except ValueError:
        raise ValueError("Not an integer", x)


################################################################################
# XML Schema Inspired Primitive Data Types
################################################################################

def is_non_negative_int(x):
    x = is_bigint(x)
    if x is None:
        return None
    if 0 <= x <= 2147483647:
        return x
    else:
        raise ValueError("Non-negative integer value out of range", x)


def is_non_positive_int(x):
    x = is_bigint(x)
    if x is None:
        return None
    if -2147483648 <= x <= 0:
        return x
    else:
        raise ValueError("Non-negative integer value out of range", x)


def is_positive_int(x):
    x = is_bigint(x)
    if x is None:
        return None
    if 1 <= x <= 2147483647:
        return x
    else:
        raise ValueError("Non-negative integer value out of range", x)


def is_smallint(x):
    x = is_int(x)
    if x is None:
        return None
    if -32768 <= x <= 32767:  # We only want 16bit signed integers
        return x
    else:
        raise ValueError("Smallint out of range", x)


def generate_is_numeric(precission, scale):
    digs = 10 ** (precission - scale)

    def is_numeric(x):
        if isinstance(x, str):
            x = x.strip()
        else:
            x = str(x)
        if x:
            dec = Decimal(x.replace(",", "."))
            if -digs >= dec or dec >= digs:
                raise ValueError("Numeric(" + str(precission) + "," + str(scale) + ") overflow: " + str(dec))
            return dec
        return None

    return is_numeric


def injson(x):
    try:
        if isinstance(x, str):
            x = json.loads(x)
        return json.dumps(x).replace('\\', '\\\\')

    except ValueError as err:
        print("Ill formated json", err, x)
    return None


def inxml(x):
    try:
        ET.fromstring(x)
        return x

    except ET.ParseError as err:
        print("Ill formated XML", err, x)
    return None
