"""
https://tools.ietf.org/html/rfc4566
"""
from collections import namedtuple
import re


TIMESRE = re.compile('(-?\d+)([dhms]{0,1})')
FieldDesc = _D = namedtuple('FieldDesc', 'name, desc, required')
SectionDesc = _S = namedtuple('SectionDesc', 'fields, desc, required, multiple')
_time_desc_fields = [
   _D('t', 'time the session is acive', True),
   _D('r', 'zero or more repeat times', False),
]
_media_desc_fields = [
   _D('m', 'media name and transport address', True),
   _D('i', 'media title', False),
   _D('c', 'connection information -- optional if included at session level', False),
   _D('b', 'zero or more bandwidth information lines', False),
   _D('k', 'encryption key', False),
   _D('a', 'zero or more media attribute lines', False),

]
_sdp_fields = [
   _D('v', 'protocol version', True),
   _D('o', 'originator and session identifier', True),
   _D('s', 'session name', True),
   _D('i', 'session information', False),
   _D('u', 'URI of description', False),
   _D('e', 'email address', False),
   _D('p', 'phone number', False),
   _D('c', 'connection information -- not required if included in all media', False),
   _D('b', 'zero or more bandwidth information lines', False),
   _S(_time_desc_fields, 'Time description', True, True),
   _D('z', 'time zone adjustments', False),
   _D('k', 'encryption key', False),
   _D('a', 'zero or more session attribute lines', False),
   _S(_media_desc_fields, 'Media description', False, True),
]
sdp_desc = _S(_sdp_fields, 'Session description', True, False)


class SdpValue(object):
    pass


class ProtocolVersion(SdpValue):

    def __init__(self, value=0):
        self.value = value

    def dumps(self):
        return '{}'.format(self.value)

    @classmethod
    def loads(cls, val):
        return cls(int(val))

    @staticmethod
    def _load_str(val):
        return val

    @staticmethod
    def _load_int(val):
        return int(val)

    @staticmethod
    def _load_enum(val, enums):
        if val in enums:
            return val
        raise Exception("Unable to laod value")


class Origin(SdpValue):

    def __init__(self, username, sess_id, sess_version, nettype, addrtype, unicast_address):
        self.username = username
        self.sess_id = sess_id
        self.sess_version = sess_version
        self.nettype = nettype
        self.addrtype = addrtype
        self.unicast_address = unicast_address

    def dumps(self):
        return ' '.join([
            self.username,
            str(self.sess_id),
            str(self.session_version),
            self.nettype,
            self.addrtype,
            self.unicast_address,
        ])

    @classmethod
    def loads(cls, val):
        fields = [x.strip() for x in val.split(' ') if x.strip()]
        return cls(
            cls._load_str(fields[0]),
            cls._load_int(fields[1]),
            cls._load_int(fields[2]),
            cls._load_enum(fields[3], ('IN',)),
            cls._load_enum(fields[4], ('IPV4', 'IPV6')),
            cls._load_str(fields[5]),
        )


class SessionName(SdpValue):

    def __init__(self, value, encoding='utf-8'):
        self.value = value
        self.encoding = encoding

    def dumps(self):
        return '{}'.format(self.value)

    @classmethod
    def loads(cls, val):
        return cls(val)


class Uri(SdpValue):

    def __init__(self, value):
        self.value = value

    def dumps(self):
        return '{}'.format(self.value)

    @classmethod
    def loads(cls, val):
        return cls(val)


class Email(SdpValue):

    def __init__(self, value):
        self.value = value

    def dumps(self):
        return '{}'.format(self.value)

    @classmethod
    def loads(cls, val):
        return cls(val)


class PhoneNumber(SdpValue):

    def __init__(self, value):
        self.value = value

    def dumps(self):
        return '{}'.format(self.value)

    @classmethod
    def loads(cls, val):
        return cls(val)


class ConnectionData(SdpValue):

    def __init__(self, nettype, addrtype, connection_address):
        self.nettype = nettype
        self.addrtype = addrtype
        self.connection_address = connection_address

    def dumps(self):
        return '{} {} {}'.format(self.nettype, self.addrtype, self.connection_address)

    @classmethod
    def loads(cls, val):
        fields = [x.strip() for x in val.split(' ') if x.strip()]
        return cls(
            cls._load_enum(fields[0], ('IN',)),
            cls._load_enum(fields[1], ('IP4', 'IP6',)),
            cls._load_str(fields[2]), ## TODO: _load_addr
        )


class Bandwidth(SdpValue):
    def __init__(self, bwtype, bandwidth):
        self.bwtype = bwtype
        self.bandwidth = bandwidth

    def dumps(self):
        return '{}:{}'.format(self.bwtype, self.bandwith)

    @classmethod
    def loads(cls, val):
        fields = [x.strip() for x in val.split(':') if x.strip()]
        return cls(
            cls._load_enum(fields[0], ('CT', 'AS',)),
            cls._load_str(fields[1]),
        )


class Timing(SdpValue):

    def __init__(self, start_time, stop_time):
        self.start_time = start_time
        self.stop_time = stop_time

    def dumps(self):
        return '{} {}'.format(self.start_time, self.stop_time)

    @classmethod
    def loads(cls, val):
        fields = [x.strip() for x in val.split(' ') if x.strip()]
        return cls(
            cls._load_int(fields[0]),
            cls._load_int(fields[1]),
        )



class RepeatTimes(SdpValue):

    def __init__(self, interval, duration, times):
        self.interval = interval
        self.duration = duration
        self.times = times

    def _load_time(self, val):
        pass


class TimeZones(SdpValue):

    def __init__(self, zones):
        self.zones = zones


class EncryptionKeys(SdpValue):

    def __init__(self, method, key=None):
        self.method = method
        self.key = key


class Attributes(SdpValue):

    def __init__(self, attr, val=None):
        self.attr = attr
        self.val = val


class MediaDescrption(SdpValue):

    def __init__(self, port, proto, fmts):
        self.port = port
        self.proto = proto
        self.fmts = fmts
