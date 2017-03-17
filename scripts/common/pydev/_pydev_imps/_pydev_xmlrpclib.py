# Embedded file name: scripts/common/pydev/_pydev_imps/_pydev_xmlrpclib.py
import sys
import re, string, time, operator
from types import *
try:
    unicode
except NameError:
    unicode = None

try:
    import datetime
except ImportError:
    datetime = None

try:
    _bool_is_builtin = False.__class__.__name__ == 'bool'
except (NameError, AttributeError):
    _bool_is_builtin = 0

def _decode(data, encoding, is8bit = re.compile('[\x80-\xff]').search):
    if unicode and encoding and is8bit(data):
        data = unicode(data, encoding)
    return data


def escape(s, replace = string.replace):
    s = replace(s, '&', '&amp;')
    s = replace(s, '<', '&lt;')
    return replace(s, '>', '&gt;')


if unicode:

    def _stringify(string):
        try:
            return string.encode('ascii')
        except UnicodeError:
            return string


else:

    def _stringify(string):
        return string


__version__ = '1.0.1'
try:
    long
except NameError:
    long = int

MAXINT = long(2) ** 31 - 1
MININT = long(-2) ** 31
PARSE_ERROR = -32700
SERVER_ERROR = -32600
APPLICATION_ERROR = -32500
SYSTEM_ERROR = -32400
TRANSPORT_ERROR = -32300
NOT_WELLFORMED_ERROR = -32700
UNSUPPORTED_ENCODING = -32701
INVALID_ENCODING_CHAR = -32702
INVALID_XMLRPC = -32600
METHOD_NOT_FOUND = -32601
INVALID_METHOD_PARAMS = -32602
INTERNAL_ERROR = -32603

class Error(Exception):
    """Base class for client errors."""

    def __str__(self):
        return repr(self)


class ProtocolError(Error):
    """Indicates an HTTP protocol error."""

    def __init__(self, url, errcode, errmsg, headers):
        Error.__init__(self)
        self.url = url
        self.errcode = errcode
        self.errmsg = errmsg
        self.headers = headers

    def __repr__(self):
        return '<ProtocolError for %s: %s %s>' % (self.url, self.errcode, self.errmsg)


class ResponseError(Error):
    """Indicates a broken response package."""
    pass


class Fault(Error):
    """Indicates an XML-RPC fault package."""

    def __init__(self, faultCode, faultString, **extra):
        Error.__init__(self)
        self.faultCode = faultCode
        self.faultString = faultString

    def __repr__(self):
        return '<Fault %s: %s>' % (self.faultCode, repr(self.faultString))


if _bool_is_builtin:
    boolean = Boolean = bool
    True, False = True, False
else:

    class Boolean:
        """Boolean-value wrapper.
        
        Use True or False to generate a "boolean" XML-RPC value.
        """

        def __init__(self, value = 0):
            self.value = operator.truth(value)

        def encode(self, out):
            out.write('<value><boolean>%d</boolean></value>\n' % self.value)

        def __cmp__(self, other):
            if isinstance(other, Boolean):
                other = other.value
            return cmp(self.value, other)

        def __repr__(self):
            if self.value:
                return '<Boolean True at %x>' % id(self)
            else:
                return '<Boolean False at %x>' % id(self)

        def __int__(self):
            return self.value

        def __nonzero__(self):
            return self.value


    True, False = Boolean(1), Boolean(0)

    def boolean(value, _truefalse = (False, True)):
        """Convert any Python value to XML-RPC 'boolean'."""
        return _truefalse[operator.truth(value)]


class DateTime:
    """DateTime wrapper for an ISO 8601 string or time tuple or
    localtime integer value to generate 'dateTime.iso8601' XML-RPC
    value.
    """

    def __init__(self, value = 0):
        if not isinstance(value, StringType):
            if datetime and isinstance(value, datetime.datetime):
                self.value = value.strftime('%Y%m%dT%H:%M:%S')
                return
            if datetime and isinstance(value, datetime.date):
                self.value = value.strftime('%Y%m%dT%H:%M:%S')
                return
            if datetime and isinstance(value, datetime.time):
                today = datetime.datetime.now().strftime('%Y%m%d')
                self.value = value.strftime(today + 'T%H:%M:%S')
                return
            if not isinstance(value, (TupleType, time.struct_time)):
                if value == 0:
                    value = time.time()
                value = time.localtime(value)
            value = time.strftime('%Y%m%dT%H:%M:%S', value)
        self.value = value

    def __cmp__(self, other):
        if isinstance(other, DateTime):
            other = other.value
        return cmp(self.value, other)

    def __str__(self):
        return self.value

    def __repr__(self):
        return '<DateTime %s at %x>' % (repr(self.value), id(self))

    def decode(self, data):
        data = str(data)
        self.value = string.strip(data)

    def encode(self, out):
        out.write('<value><dateTime.iso8601>')
        out.write(self.value)
        out.write('</dateTime.iso8601></value>\n')


def _datetime(data):
    value = DateTime()
    value.decode(data)
    return value


def _datetime_type(data):
    t = time.strptime(data, '%Y%m%dT%H:%M:%S')
    return datetime.datetime(*tuple(t)[:6])


import base64
try:
    import cStringIO as StringIO
except ImportError:
    import StringIO

class Binary:
    """Wrapper for binary data."""

    def __init__(self, data = None):
        self.data = data

    def __str__(self):
        return self.data or ''

    def __cmp__(self, other):
        if isinstance(other, Binary):
            other = other.data
        return cmp(self.data, other)

    def decode(self, data):
        self.data = base64.decodestring(data)

    def encode(self, out):
        out.write('<value><base64>\n')
        base64.encode(StringIO.StringIO(self.data), out)
        out.write('</base64></value>\n')


def _binary(data):
    value = Binary()
    value.decode(data)
    return value


WRAPPERS = (DateTime, Binary)
if not _bool_is_builtin:
    WRAPPERS = WRAPPERS + (Boolean,)
try:
    import _xmlrpclib
    FastParser = _xmlrpclib.Parser
    FastUnmarshaller = _xmlrpclib.Unmarshaller
except (AttributeError, ImportError):
    FastParser = FastUnmarshaller = None

try:
    import _xmlrpclib
    FastMarshaller = _xmlrpclib.Marshaller
except (AttributeError, ImportError):
    FastMarshaller = None

try:
    import sgmlop
    if not hasattr(sgmlop, 'XMLParser'):
        raise ImportError()
except ImportError:
    SgmlopParser = None
else:

    class SgmlopParser:

        def __init__(self, target):
            self.finish_starttag = target.start
            self.finish_endtag = target.end
            self.handle_data = target.data
            self.handle_xml = target.xml
            self.parser = sgmlop.XMLParser()
            self.parser.register(self)
            self.feed = self.parser.feed
            self.entity = {'amp': '&',
             'gt': '>',
             'lt': '<',
             'apos': "'",
             'quot': '"'}

        def close(self):
            try:
                self.parser.close()
            finally:
                self.parser = self.feed = None

            return

        def handle_proc(self, tag, attr):
            m = re.search('encoding\\s*=\\s*[\'"]([^"\']+)["\']', attr)
            if m:
                self.handle_xml(m.group(1), 1)

        def handle_entityref(self, entity):
            try:
                self.handle_data(self.entity[entity])
            except KeyError:
                self.handle_data('&%s;' % entity)


try:
    from xml.parsers import expat
    if not hasattr(expat, 'ParserCreate'):
        raise ImportError()
except ImportError:
    ExpatParser = None
else:

    class ExpatParser:

        def __init__(self, target):
            self._parser = parser = expat.ParserCreate(None, None)
            self._target = target
            parser.StartElementHandler = target.start
            parser.EndElementHandler = target.end
            parser.CharacterDataHandler = target.data
            encoding = None
            if not parser.returns_unicode:
                encoding = 'utf-8'
            target.xml(encoding, None)
            return

        def feed(self, data):
            self._parser.Parse(data, 0)

        def close(self):
            self._parser.Parse('', 1)
            del self._target
            del self._parser


class SlowParser:
    """Default XML parser (based on xmllib.XMLParser)."""

    def __init__(self, target):
        import xmllib
        if xmllib.XMLParser not in SlowParser.__bases__:
            SlowParser.__bases__ = (xmllib.XMLParser,)
        self.handle_xml = target.xml
        self.unknown_starttag = target.start
        self.handle_data = target.data
        self.handle_cdata = target.data
        self.unknown_endtag = target.end
        try:
            xmllib.XMLParser.__init__(self, accept_utf8=1)
        except TypeError:
            xmllib.XMLParser.__init__(self)


class Marshaller:
    """Generate an XML-RPC params chunk from a Python data structure.
    
    Create a Marshaller instance for each set of parameters, and use
    the "dumps" method to convert your data (represented as a tuple)
    to an XML-RPC params chunk.  To write a fault response, pass a
    Fault instance instead.  You may prefer to use the "dumps" module
    function for this purpose.
    """

    def __init__(self, encoding = None, allow_none = 0):
        self.memo = {}
        self.data = None
        self.encoding = encoding
        self.allow_none = allow_none
        return

    dispatch = {}

    def dumps(self, values):
        out = []
        write = out.append
        dump = self.__dump
        if isinstance(values, Fault):
            write('<fault>\n')
            dump({'faultCode': values.faultCode,
             'faultString': values.faultString}, write)
            write('</fault>\n')
        else:
            write('<params>\n')
            for v in values:
                write('<param>\n')
                dump(v, write)
                write('</param>\n')

            write('</params>\n')
        result = string.join(out, '')
        return result

    def __dump(self, value, write):
        try:
            f = self.dispatch[type(value)]
        except KeyError:
            raise TypeError('cannot marshal %s objects' % type(value))
        else:
            f(self, value, write)

    def dump_nil(self, value, write):
        if not self.allow_none:
            raise TypeError('cannot marshal None unless allow_none is enabled')
        write('<value><nil/></value>')

    dispatch[NoneType] = dump_nil

    def dump_int(self, value, write):
        if value > MAXINT or value < MININT:
            raise OverflowError('int exceeds XML-RPC limits')
        write('<value><int>')
        write(str(value))
        write('</int></value>\n')

    dispatch[IntType] = dump_int
    if _bool_is_builtin:

        def dump_bool(self, value, write):
            write('<value><boolean>')
            write(value and '1' or '0')
            write('</boolean></value>\n')

        dispatch[bool] = dump_bool

    def dump_long(self, value, write):
        if value > MAXINT or value < MININT:
            raise OverflowError('long int exceeds XML-RPC limits')
        write('<value><int>')
        write(str(int(value)))
        write('</int></value>\n')

    dispatch[LongType] = dump_long

    def dump_double(self, value, write):
        write('<value><double>')
        write(repr(value))
        write('</double></value>\n')

    dispatch[FloatType] = dump_double

    def dump_string(self, value, write, escape = escape):
        write('<value><string>')
        write(escape(value))
        write('</string></value>\n')

    dispatch[StringType] = dump_string
    if unicode:

        def dump_unicode(self, value, write, escape = escape):
            value = value.encode(self.encoding)
            write('<value><string>')
            write(escape(value))
            write('</string></value>\n')

        dispatch[UnicodeType] = dump_unicode

    def dump_array(self, value, write):
        i = id(value)
        if self.memo.has_key(i):
            raise TypeError('cannot marshal recursive sequences')
        self.memo[i] = None
        dump = self.__dump
        write('<value><array><data>\n')
        for v in value:
            dump(v, write)

        write('</data></array></value>\n')
        del self.memo[i]
        return

    dispatch[TupleType] = dump_array
    dispatch[ListType] = dump_array

    def dump_struct(self, value, write, escape = escape):
        i = id(value)
        if self.memo.has_key(i):
            raise TypeError('cannot marshal recursive dictionaries')
        self.memo[i] = None
        dump = self.__dump
        write('<value><struct>\n')
        for k, v in value.items():
            write('<member>\n')
            if type(k) is not StringType:
                if unicode and type(k) is UnicodeType:
                    k = k.encode(self.encoding)
                else:
                    raise TypeError('dictionary key must be string')
            write('<name>%s</name>\n' % escape(k))
            dump(v, write)
            write('</member>\n')

        write('</struct></value>\n')
        del self.memo[i]
        return

    dispatch[DictType] = dump_struct
    if datetime:

        def dump_datetime(self, value, write):
            write('<value><dateTime.iso8601>')
            write(value.strftime('%Y%m%dT%H:%M:%S'))
            write('</dateTime.iso8601></value>\n')

        dispatch[datetime.datetime] = dump_datetime

        def dump_date(self, value, write):
            write('<value><dateTime.iso8601>')
            write(value.strftime('%Y%m%dT00:00:00'))
            write('</dateTime.iso8601></value>\n')

        dispatch[datetime.date] = dump_date

        def dump_time(self, value, write):
            write('<value><dateTime.iso8601>')
            write(datetime.datetime.now().date().strftime('%Y%m%dT'))
            write(value.strftime('%H:%M:%S'))
            write('</dateTime.iso8601></value>\n')

        dispatch[datetime.time] = dump_time

    def dump_instance(self, value, write):
        if value.__class__ in WRAPPERS:
            self.write = write
            value.encode(self)
            del self.write
        else:
            self.dump_struct(value.__dict__, write)

    dispatch[InstanceType] = dump_instance


class Unmarshaller:
    """Unmarshal an XML-RPC response, based on incoming XML event
    messages (start, data, end).  Call close() to get the resulting
    data structure.
    
    Note that this reader is fairly tolerant, and gladly accepts bogus
    XML-RPC data without complaining (but not bogus XML).
    """

    def __init__(self, use_datetime = 0):
        self._type = None
        self._stack = []
        self._marks = []
        self._data = []
        self._methodname = None
        self._encoding = 'utf-8'
        self.append = self._stack.append
        self._use_datetime = use_datetime
        if use_datetime and not datetime:
            raise ValueError('the datetime module is not available')
        return

    def close(self):
        if self._type is None or self._marks:
            raise ResponseError()
        if self._type == 'fault':
            raise Fault(**self._stack[0])
        return tuple(self._stack)

    def getmethodname(self):
        return self._methodname

    def xml(self, encoding, standalone):
        self._encoding = encoding

    def start(self, tag, attrs):
        if tag == 'array' or tag == 'struct':
            self._marks.append(len(self._stack))
        self._data = []
        self._value = tag == 'value'

    def data(self, text):
        self._data.append(text)

    def end(self, tag, join = string.join):
        try:
            f = self.dispatch[tag]
        except KeyError:
            pass
        else:
            return f(self, join(self._data, ''))

    def end_dispatch(self, tag, data):
        try:
            f = self.dispatch[tag]
        except KeyError:
            pass
        else:
            return f(self, data)

    dispatch = {}

    def end_nil(self, data):
        self.append(None)
        self._value = 0
        return

    dispatch['nil'] = end_nil

    def end_boolean(self, data):
        if data == '0':
            self.append(False)
        elif data == '1':
            self.append(True)
        else:
            raise TypeError('bad boolean value')
        self._value = 0

    dispatch['boolean'] = end_boolean

    def end_int(self, data):
        self.append(int(data))
        self._value = 0

    dispatch['i4'] = end_int
    dispatch['int'] = end_int

    def end_double(self, data):
        self.append(float(data))
        self._value = 0

    dispatch['double'] = end_double

    def end_string(self, data):
        if self._encoding:
            data = _decode(data, self._encoding)
        self.append(_stringify(data))
        self._value = 0

    dispatch['string'] = end_string
    dispatch['name'] = end_string

    def end_array(self, data):
        mark = self._marks.pop()
        self._stack[mark:] = [self._stack[mark:]]
        self._value = 0

    dispatch['array'] = end_array

    def end_struct(self, data):
        mark = self._marks.pop()
        dict = {}
        items = self._stack[mark:]
        for i in range(0, len(items), 2):
            dict[_stringify(items[i])] = items[i + 1]

        self._stack[mark:] = [dict]
        self._value = 0

    dispatch['struct'] = end_struct

    def end_base64(self, data):
        value = Binary()
        value.decode(data)
        self.append(value)
        self._value = 0

    dispatch['base64'] = end_base64

    def end_dateTime(self, data):
        value = DateTime()
        value.decode(data)
        if self._use_datetime:
            value = _datetime_type(data)
        self.append(value)

    dispatch['dateTime.iso8601'] = end_dateTime

    def end_value(self, data):
        if self._value:
            self.end_string(data)

    dispatch['value'] = end_value

    def end_params(self, data):
        self._type = 'params'

    dispatch['params'] = end_params

    def end_fault(self, data):
        self._type = 'fault'

    dispatch['fault'] = end_fault

    def end_methodName(self, data):
        if self._encoding:
            data = _decode(data, self._encoding)
        self._methodname = data
        self._type = 'methodName'

    dispatch['methodName'] = end_methodName


class _MultiCallMethod:

    def __init__(self, call_list, name):
        self.__call_list = call_list
        self.__name = name

    def __getattr__(self, name):
        return _MultiCallMethod(self.__call_list, '%s.%s' % (self.__name, name))

    def __call__(self, *args):
        self.__call_list.append((self.__name, args))


class MultiCallIterator:
    """Iterates over the results of a multicall. Exceptions are
    thrown in response to xmlrpc faults."""

    def __init__(self, results):
        self.results = results

    def __getitem__(self, i):
        item = self.results[i]
        if type(item) == type({}):
            raise Fault(item['faultCode'], item['faultString'])
        else:
            if type(item) == type([]):
                return item[0]
            raise ValueError('unexpected type in multicall result')


class MultiCall:
    """server -> a object used to boxcar method calls
    
    server should be a ServerProxy object.
    
    Methods can be added to the MultiCall using normal
    method call syntax e.g.:
    
    multicall = MultiCall(server_proxy)
    multicall.add(2,3)
    multicall.get_address("Guido")
    
    To execute the multicall, call the MultiCall object e.g.:
    
    add_result, address = multicall()
    """

    def __init__(self, server):
        self.__server = server
        self.__call_list = []

    def __repr__(self):
        return '<MultiCall at %x>' % id(self)

    __str__ = __repr__

    def __getattr__(self, name):
        return _MultiCallMethod(self.__call_list, name)

    def __call__(self):
        marshalled_list = []
        for name, args in self.__call_list:
            marshalled_list.append({'methodName': name,
             'params': args})

        return MultiCallIterator(self.__server.system.multicall(marshalled_list))


def getparser(use_datetime = 0):
    """getparser() -> parser, unmarshaller
    
    Create an instance of the fastest available parser, and attach it
    to an unmarshalling object.  Return both objects.
    """
    if use_datetime and not datetime:
        raise ValueError('the datetime module is not available')
    if FastParser and FastUnmarshaller:
        if use_datetime:
            mkdatetime = _datetime_type
        else:
            mkdatetime = _datetime
        target = FastUnmarshaller(True, False, _binary, mkdatetime, Fault)
        parser = FastParser(target)
    else:
        target = Unmarshaller(use_datetime=use_datetime)
        if FastParser:
            parser = FastParser(target)
        elif SgmlopParser:
            parser = SgmlopParser(target)
        elif ExpatParser:
            parser = ExpatParser(target)
        else:
            parser = SlowParser(target)
    return (parser, target)


def dumps(params, methodname = None, methodresponse = None, encoding = None, allow_none = 0):
    """data [,options] -> marshalled data
    
    Convert an argument tuple or a Fault instance to an XML-RPC
    request (or response, if the methodresponse option is used).
    
    In addition to the data object, the following options can be given
    as keyword arguments:
    
        methodname: the method name for a methodCall packet
    
        methodresponse: true to create a methodResponse packet.
        If this option is used with a tuple, the tuple must be
        a singleton (i.e. it can contain only one element).
    
        encoding: the packet encoding (default is UTF-8)
    
    All 8-bit strings in the data structure are assumed to use the
    packet encoding.  Unicode strings are automatically converted,
    where necessary.
    """
    if not (isinstance(params, TupleType) or isinstance(params, Fault)):
        raise AssertionError('argument must be tuple or Fault instance')
        if isinstance(params, Fault):
            methodresponse = 1
        elif not (methodresponse and isinstance(params, TupleType) and len(params) == 1):
            raise AssertionError('response tuple must be a singleton')
        if not encoding:
            encoding = 'utf-8'
        if FastMarshaller:
            m = FastMarshaller(encoding)
        else:
            m = Marshaller(encoding, allow_none)
        data = m.dumps(params)
        if encoding != 'utf-8':
            xmlheader = "<?xml version='1.0' encoding='%s'?>\n" % str(encoding)
        else:
            xmlheader = "<?xml version='1.0'?>\n"
        if methodname:
            methodname = isinstance(methodname, StringType) or methodname.encode(encoding)
        data = (xmlheader,
         '<methodCall>\n<methodName>',
         methodname,
         '</methodName>\n',
         data,
         '</methodCall>\n')
    elif methodresponse:
        data = (xmlheader,
         '<methodResponse>\n',
         data,
         '</methodResponse>\n')
    else:
        return data
    return string.join(data, '')


def loads(data, use_datetime = 0):
    """data -> unmarshalled data, method name
    
    Convert an XML-RPC packet to unmarshalled data plus a method
    name (None if not present).
    
    If the XML-RPC packet represents a fault condition, this function
    raises a Fault exception.
    """
    p, u = getparser(use_datetime=use_datetime)
    p.feed(data)
    p.close()
    return (u.close(), u.getmethodname())


class _Method:

    def __init__(self, send, name):
        self.__send = send
        self.__name = name

    def __getattr__(self, name):
        return _Method(self.__send, '%s.%s' % (self.__name, name))

    def __call__(self, *args):
        return self.__send(self.__name, args)


class Transport:
    """Handles an HTTP transaction to an XML-RPC server."""
    user_agent = 'xmlrpclib.py/%s (by www.pythonware.com)' % __version__

    def __init__(self, use_datetime = 0):
        self._use_datetime = use_datetime

    def request(self, host, handler, request_body, verbose = 0):
        h = self.make_connection(host)
        if verbose:
            h.set_debuglevel(1)
        self.send_request(h, handler, request_body)
        self.send_host(h, host)
        self.send_user_agent(h)
        self.send_content(h, request_body)
        errcode, errmsg, headers = h.getreply()
        if errcode != 200:
            raise ProtocolError(host + handler, errcode, errmsg, headers)
        self.verbose = verbose
        try:
            sock = h._conn.sock
        except AttributeError:
            sock = None

        return self._parse_response(h.getfile(), sock)

    def getparser(self):
        return getparser(use_datetime=self._use_datetime)

    def get_host_info(self, host):
        x509 = {}
        if isinstance(host, TupleType):
            host, x509 = host
        import urllib
        auth, host = urllib.splituser(host)
        if auth:
            import base64
            auth = base64.encodestring(urllib.unquote(auth))
            auth = string.join(string.split(auth), '')
            extra_headers = [('Authorization', 'Basic ' + auth)]
        else:
            extra_headers = None
        return (host, extra_headers, x509)

    def make_connection(self, host):
        import httplib
        host, extra_headers, x509 = self.get_host_info(host)
        return httplib.HTTP(host)

    def send_request(self, connection, handler, request_body):
        connection.putrequest('POST', handler)

    def send_host(self, connection, host):
        host, extra_headers, x509 = self.get_host_info(host)
        connection.putheader('Host', host)
        if extra_headers:
            if isinstance(extra_headers, DictType):
                extra_headers = extra_headers.items()
            for key, value in extra_headers:
                connection.putheader(key, value)

    def send_user_agent(self, connection):
        connection.putheader('User-Agent', self.user_agent)

    def send_content(self, connection, request_body):
        connection.putheader('Content-Type', 'text/xml')
        connection.putheader('Content-Length', str(len(request_body)))
        connection.endheaders()
        if request_body:
            connection.send(request_body)

    def parse_response(self, file):
        return self._parse_response(file, None)

    def _parse_response--- This code section failed: ---

0	LOAD_FAST         'self'
3	LOAD_ATTR         'getparser'
6	CALL_FUNCTION_0   None
9	UNPACK_SEQUENCE_2 None
12	STORE_FAST        'p'
15	STORE_FAST        'u'

18	SETUP_LOOP        '125'

21	LOAD_FAST         'sock'
24	POP_JUMP_IF_FALSE '45'

27	LOAD_FAST         'sock'
30	LOAD_ATTR         'recv'
33	LOAD_CONST        1024
36	CALL_FUNCTION_1   None
39	STORE_FAST        'response'
42	JUMP_FORWARD      '60'

45	LOAD_FAST         'file'
48	LOAD_ATTR         'read'
51	LOAD_CONST        1024
54	CALL_FUNCTION_1   None
57	STORE_FAST        'response'
60_0	COME_FROM         '42'

60	LOAD_FAST         'response'
63	POP_JUMP_IF_TRUE  '70'

66	BREAK_LOOP        None
67	JUMP_FORWARD      '70'
70_0	COME_FROM         '67'

70	LOAD_FAST         'self'
73	LOAD_ATTR         'verbose'
76	POP_JUMP_IF_FALSE '108'

79	LOAD_GLOBAL       'sys'
82	LOAD_ATTR         'stdout'
85	LOAD_ATTR         'write'
88	LOAD_CONST        'body: %s\n'
91	LOAD_GLOBAL       'repr'
94	LOAD_FAST         'response'
97	CALL_FUNCTION_1   None
100	BINARY_MODULO     None
101	CALL_FUNCTION_1   None
104	POP_TOP           None
105	JUMP_FORWARD      '108'
108_0	COME_FROM         '105'

108	LOAD_FAST         'p'
111	LOAD_ATTR         'feed'
114	LOAD_FAST         'response'
117	CALL_FUNCTION_1   None
120	POP_TOP           None
121	JUMP_BACK         '21'
124	POP_BLOCK         None
125_0	COME_FROM         '18'

125	LOAD_FAST         'file'
128	LOAD_ATTR         'close'
131	CALL_FUNCTION_0   None
134	POP_TOP           None

135	LOAD_FAST         'p'
138	LOAD_ATTR         'close'
141	CALL_FUNCTION_0   None
144	POP_TOP           None

145	LOAD_FAST         'u'
148	LOAD_ATTR         'close'
151	CALL_FUNCTION_0   None
154	RETURN_VALUE      None
-1	RETURN_LAST       None

Syntax error at or near `POP_BLOCK' token at offset 124


class SafeTransport(Transport):
    """Handles an HTTPS transaction to an XML-RPC server."""

    def make_connection(self, host):
        import httplib
        host, extra_headers, x509 = self.get_host_info(host)
        try:
            HTTPS = httplib.HTTPS
        except AttributeError:
            raise NotImplementedError("your version of httplib doesn't support HTTPS")
        else:
            return HTTPS(host, None, **(x509 or {}))

        return


class ServerProxy:
    """uri [,options] -> a logical connection to an XML-RPC server
    
    uri is the connection point on the server, given as
    scheme://host/target.
    
    The standard implementation always supports the "http" scheme.  If
    SSL socket support is available (Python 2.0), it also supports
    "https".
    
    If the target part and the slash preceding it are both omitted,
    "/RPC2" is assumed.
    
    The following options can be given as keyword arguments:
    
        transport: a transport factory
        encoding: the request encoding (default is UTF-8)
    
    All 8-bit strings passed to the server proxy are assumed to use
    the given encoding.
    """

    def __init__(self, uri, transport = None, encoding = None, verbose = 0, allow_none = 0, use_datetime = 0):
        import urllib
        type, uri = urllib.splittype(uri)
        if type not in ('http', 'https'):
            raise IOError('unsupported XML-RPC protocol')
        self.__host, self.__handler = urllib.splithost(uri)
        if not self.__handler:
            self.__handler = '/RPC2'
        if transport is None:
            if type == 'https':
                transport = SafeTransport(use_datetime=use_datetime)
            else:
                transport = Transport(use_datetime=use_datetime)
        self.__transport = transport
        self.__encoding = encoding
        self.__verbose = verbose
        self.__allow_none = allow_none
        return

    def __request(self, methodname, params):
        request = dumps(params, methodname, encoding=self.__encoding, allow_none=self.__allow_none)
        response = self.__transport.request(self.__host, self.__handler, request, verbose=self.__verbose)
        if len(response) == 1:
            response = response[0]
        return response

    def __repr__(self):
        return '<ServerProxy for %s%s>' % (self.__host, self.__handler)

    __str__ = __repr__

    def __getattr__(self, name):
        return _Method(self.__request, name)


Server = ServerProxy
if __name__ == '__main__':
    server = ServerProxy('http://time.xmlrpc.com/RPC2')
    sys.stdout.write('%s\n' % server)
    try:
        sys.stdout.write('%s\n' % (server.currentTime.getCurrentTime(),))
    except Error:
        import traceback
        traceback.print_exc()

    multi = MultiCall(server)
    multi.currentTime.getCurrentTime()
    multi.currentTime.getCurrentTime()
    try:
        for response in multi():
            sys.stdout.write('%s\n' % (response,))

    except Error:
        import traceback
        traceback.print_exc()