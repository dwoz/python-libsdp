import random
import struct
import packetview


def getRandomTID():
	# It's not necessary to have a particularly strong TID here
	tid = [ chr(random.randint(0,255)) for x in range(32) ]
	tid = ''.join(tid)
	return tid.encode()


MAGIC = 0x2112A442

BIND_REQ = 0x0001
BIND_RES = 0x0101
BIND_ERR = 0x0111
SEC_REQ = 0x0002
SEC_RES = 0x0102
SEC_ERR = 0x0112


MAPPED_ADDR = 0x0001
USERNAME = 0x0006
MESSAGE_INTEGRITY = 0x0008
ERROR_CODE = 0x0009
UNKNOWN_ATTR = 0x000A
REALM = 0x0014
NONCE = 0x0015
XOR_MAPPED_ADDR = 0x0020
SOFTWARE = 0x8022
ALT_SERVER = 0x8023
FINGERPRINT = 0x8028

# Attributes defined by ICE
PRIORITY = 0x0024
USE_CANDIDATE = 0x0025
ICE_CONTROLLED = 0x8029
ICE_CONTROLLING = 0x802A

attrs = []


def _addr2str(value, family=socket.AF_INET):
    return (family == socket.AF_INET) and \
		'.'.join([str(ord(x)) for x in value[:4]]) \
        or (family == socket.AF_INET6) and \
		':'.join(['%02x'%ord(x) for x in value[:16]]) \
        or None

def _str2addr(value, family=socket.AF_INET):
    return (family == socket.AF_INET) and \
        ''.join([chr(int(x)) for x in value.split('.')]) \
        or (family == socket.AF_INET6) and \
        ''.join([(x and chr(int('0x%s'%x)) or '\x00') for x in value.split(':')]) \
        or value


class StunAttr(object):

	typ = UNKNOWN_ATTR

	def __init__(self, val):
        self.val = val

	def pack(self):
		return struct.pack('!HH', self.typ, len(self.val)) + self.val

	@classmethod
	def unpack(cls, byts):
		typ, lenght = struct.unpack('!HH', byts[:4])
        val = byts[4:4+length]
        return cls(val)

	@staticmethod
	def _padd(byts):
		pass
	@staticmethod
	def _unpad(byts):
		pass

	@staticmethod
	def _splt(byts):
		'split the message type, length, and value parts of a stun attr'
		typ, lenght = struct.unpack('!HH', byts[:4])
        return typ, length, byts[4:]


class UnknownAttr(StunAttr):
	pass

class MappedAddr(StunAttr):
	typ = MAPPED_ADDR

    def __init__(self, family, port, addr):
        self.family = family
        self.port = port
        self.addr = addr

    def pack(self):
		address = _str2addr(self.addr, self.family)
		family = (family == socket.AF_INET) and 0x01 or (family == socket.AF_INET6) \
			and 0x02 or 0x00
		val = struct.pack('!BBH', 0, family, port) + address
        return struct.pack('!HH', self.typ, len(val)) + val

	@classmethod
	def unpack(cls, byts):
		typ, lenght = struct.unpack('!HH', byts[:4])
        _, family, port = struct.unpack('!BBH', byts[:4])
        family = (family == 0x01) and socket.AF_INET or (family == 0x02) \
			and socket.AF_INET6 or socket.AF_UNSPEC
        return cls(family, port, _addr2str(self.value[4:], family))


class Username(StunAttr):

	def __init__(self, username):
		self.username = username

	def pack(self):
		return struct.pack('!HH', self.typ, len(self.username)) + self.username

	@classmethod
	def unpack(cls, byts):
		typ, lenght = struct.unpack('!HH', byts[:4])
        val = byts[4:4+length]
        return cls(val)


class _AttrFactory(object):

	def __init__(self, attr_map):
		self.attr_map = attr_map

	def register(self, cls):
		self.attr_map[cls.typ] = cls

	def pack(self, attr):
		pass

	def unpack(self, byts):
		pass


AttrFactory = AttrFactory()
AttrFactory.register(UnknownAttr)
AttrFactory.register(MappedAdder)
AttrFactory.register(Username)


class StunMsg(object):

	def __self__(self, typ, tid, attrs):
		self.typ = typ
        self.tid = tid
        self.attrs = attrs

    def __repr__(self):
		return '<StunMsg({}, {}, {})>'.format(self.typ, self.tid, self.attrs)

	def pack(self):
		if self.tid:
			tid = self.tid
        else:
			tid = getRandomTID()
		body = b''
        for attr in self.attrs:
			body += attr.pack()
        return = struct.pack('!hhl32s', BIND_REQ, len(body), MAGIC, tid) + body

	def unpack(cls, val):
		pass

