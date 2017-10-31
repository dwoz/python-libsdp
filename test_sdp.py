from sdp import TIMESRE, parse_sdp, ProtocolVersion

import pytest

def test_times_re_a():
    assert TIMESRE.match('17d').groups() == ('17', 'd')

def test_times_re_b():
    assert TIMESRE.match('-1h').groups() == ('-1', 'h')

def test_times_re_c():
    assert TIMESRE.match('0').groups() == ('0', '')


s = '''v=0
o=- 5039103018570591393 2 IN IP4 127.0.0.1
s=-
t=0 0
a=group:BUNDLE data
a=msid-semantic: WMS
m=application 9 DTLS/SCTP 5000
c=IN IP4 0.0.0.0
a=ice-ufrag:YLUR
a=ice-pwd:ag92DhPlOOT02HZ8W/JSB2a0
a=ice-options:trickle
a=fingerprint:sha-256 BC:EE:2F:F4:DF:F3:5E:28:15:98:73:27:B2:BE:07:85:60:94:98:E2:C7:D3:C9:F6:BE:2E:DC:17:E3:B0:A6:9A
a=setup:actpass
a=mid:data
a=sctpmap:5000 webrtc-datachannel 1024'''


class SDP(object):
    def __init__(
            self, version, originator, session_name, session_information, times,
            uri=None, email=None, phone=None, contact_info=None,
            bandwidth=None, timezones=None, encryption_key=None,
            attributes=None, media_descriptions=None):
       self.version = version
       self.originator = originator
       self.session_name = session_name
       self.session_information = session_information
       self.times = times
       self.uri = uri

    @classmethod
    def parse(cls, value):
        def tokens(val):
            for line in val.replace('\r', '').split('\n'):
                yield line.split('=', 1)
        for key, val in tokens(value):


def test_parse_sdp():
    SDP.parse(s)


def test_protocol_version_loads_a():
    v, x = ProtocolVersion.consume('v=0\n')
    assert v.version == 0

def test_protocol_version_loads_b():
    v = ProtocolVersion.load_val('v=0\r\n')
    assert v.version == 0

def test_protocol_version_loads_c():
    v = ProtocolVersion.load_val('v=0')
    assert v.version == 0

def test_protocol_version_dumps_a():
    assert ProtocolVersion(0).dumps() == 'v=0'

