"""
https://tools.ietf.org/html/rfc4566
"""
from collections import namedtuple
import re
import io


TIMESRE = re.compile('(-?\d+)([dhms]{0,1})')

class FieldSpec(object):

    def __init__(self, long_name, description='', required=True, multiple=False, short_name=''):
        if not short_name:
            short_name = long_name[0]
        self.long_name = long_name
        self.short_name = short_name
        self.description = description
        self.required = required
        self.multiple = multiple


class SectionSpec(object):

    def __init__(self, name, dsecription='', required=True, multiple=False):
        self.name = name
        self.description = description
        self.required = required
        self.multiple = muliple
        self.fields = fields


time_spec = SectionSpec(
    'Time description',
    'one or more time descriptions',
    required=True,
    multiple=True,
)


time_spec.fields = [
   FieldSpec('time', 't', 'time the session is acive', True, False),
   FieldSpec('repeat', 'r', 'zero or more repeat times', False, False),
]


media_spec = SectionSpec(
    'Media description',
    'zero or more media descriptions',
    required=False,
    multiple=True
)


media_spec.fields = [
    FieldSpec('media', 'm', 'media name and transport address', True, False),
    FieldSpec('title', 'i', 'media title', False, False),
    FieldSpec('connection_info', 'c', 'connection information -- optional if included at session level', False, False),
    FieldSpec('bandwidth', 'b', 'zero or more bandwidth information lines', False, False),
    FieldSpec('key', 'k', 'encryption key', False, False),
    FieldSpec('attribute', 'a', 'zero or more media attribute lines', False, False),
]


sdp_spec = SectionSpec(
    'Session description',
    'SDP Message',
    required=True,
    multiple=False
)


sdp_spec.fields = [
    FieldSpec('version', 'v', 'protocol version', True, False),
    FieldSpec('origin', 'o', 'originator and session identifier', True, False),
    FieldSpec('session_name', 's', 'session name', True, False),
    FieldSpec('session_info', 'i', 'session information', False, False),
    FieldSpec('url', 'u', 'URI of description', False, False),
    FieldSpec('email', 'e', 'email address', False, False),
    FieldSpec('phone', 'p', 'phone number', False, False),
    FieldSpec('connection_info', 'c', 'connection information -- not required if included in all media', False, False),
    FieldSpec('bandwidth', 'b', 'zero or more bandwidth information lines', False, False),
    time_spec,
    FieldSpec('tz_adjustments', 'z', 'time zone adjustments', False, False),
    FieldSpec('key', 'k', 'encryption key', False, False),
    FieldSpec('attribute', 'a', 'zero or more session attribute lines', False, True),
    media_spec,
]


_name_to_cls = {}

def parse_sdp(val, desc=sdp_desc):
    fp = io.StringIO(val)
    n = 0
    field = desc.fields[n]
    for line in fp:
        if field.required:
            x = (field.name, line)
        print(repr(line))


class SectionValidator(object):

    def __init__(self, desc):
        self.desc = desc
        self._diter = self.iter_desc(desc)

    def next_desc(self):
        return next(self._diter)

    def __call__(self, rawsdp):
        lines = io.StringIO(s)
        desc = self.next_desc()
        for line in lines:
            name, val = line.strip('\n').split('=', 1)

    @staticmethod
    def iter_desc(*fields):
        for a in fields:
            if type(a) == _S:
                for b in iter_desc(*a.fields):
                    yield b
            else:
                yield a


class FieldValidator(object):

    def __init__(self, desc):
        self.desc = desc

    def __call__(self, rawsdp):
        lines = io.StringIO(s)
        for line in lines:
            name, val = line.strip('\n').split('=', 1)


class Loader(object):

    def __init__(self, specs, classes):
        self.specs = specs
        self.classes = classes
        self._current_spec = None

    def __call__(self, value):
        spec = self.next_spec()

    def next_spec(self):
        if self._current_spec:
            return self._current_spec


class SdpValue(object):
    pass

    @classmethod
    def consume(cls, value):
        line, leftover = value.split('\n', 1)
        name, val = line.split('=', 1)
        if name == cls.spec.name:
            return cls.load_val(val), leftover
        return None, value

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


class ProtocolVersion(SdpValue):

    def __init__(self, version=0):
        self.version = version

    def dumps(self):
        return '{}'.format(self.spec.name, self.version)

    @classmethod
    def load_val(cls, val):
        return cls(int(val))


_name_to_cls['v'] = ProtocolVersion


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
    _times_re = TIMESRE
    _mod = {
        'd': 86400,
        'h': 3600,
        'm': 60,
        's': 1,
    }

    def __init__(self, interval, duration, times):
        self.interval = interval
        self.duration = duration
        self.times = times

    @classmethod
    def loads(cls, val):
        fields = [x.strip() for x in val.split(' ') if x.strip()]

    @classmethod
    def _load_time(cls, val):
        match = self._times_re.match(val)
        if not match:
            raise Exception("Failed to parse: {}".format(val))
        if match[1]:
            return int(match[0]) * cls._mod[match[1]]
        else:
            return int(match[0])


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
