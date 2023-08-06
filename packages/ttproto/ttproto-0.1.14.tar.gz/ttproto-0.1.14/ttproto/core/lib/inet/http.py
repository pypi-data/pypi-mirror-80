#!/usr/bin/env python3

# Author Federico Sismondi
# Inspired from https://github.com/invernizzi/scapy-http/blob/master/scapy_http/http.py

import re
import logging
from ttproto.core.data import *
from ttproto.core.packet import *
from ttproto.core.lib.inet.meta import *
from ttproto.core import exceptions
from contextlib import contextmanager
import ttproto.core.lib.inet.tcp
import ttproto.core.lib.inet.onem2m

import six

__all__ = [
    "HTTP",
    "HTTPHeader",
    "HTTPHeaderList",
]

RESPONSE_HEADERS = [
    "Access-Control-Allow-Origin",
    "Access-Control-Allow-Credentials",
    "Access-Control-Expose-Headers",
    "Access-Control-Max-Age",
    "Access-Control-Allow-Methods",
    "Access-Control-Allow-Headers",
    "Accept-Patch",
    "Accept-Ranges",
    "Age",
    "Allow",
    "Alt-Svc",
    "Content-Disposition",
    "Content-Encoding",
    "Content-Language",
    "Content-Location",
    "Content-Range",
    "Delta-Base",
    "ETag",
    "Expires",
    "IM",
    "Last-Modified",
    "Link",
    "Location",
    "Permanent",
    "P3P",
    "Proxy-Authenticate",
    "Public-Key-Pins",
    "Retry-After",
    "Server",
    "Set-Cookie",
    "Strict-Transport-Security",
    "Trailer",
    "Transfer-Encoding",
    "Tk",
    "Vary",
    "WWW-Authenticate",
    "X-Frame-Options",
]


# - - - AUX functions - - -

def plain_str(x):
    """Convert basic byte objects to str"""
    if isinstance(x, bytes):
        return x.decode(errors="ignore")
    return str(x)


def _strip_header_name(name):
    """Takes a header key (i.e., "Host" in "Host: www.google.com",
    and returns a stripped representation of it
    """
    return plain_str(name.strip()).replace("-", "_")


def _parse_headers(s):
    headers = s.split(b"\r\n")
    headers_found = {}
    for header_line in headers:
        try:
            key, value = header_line.split(b':', 1)
        except ValueError:
            continue
        header_key = _strip_header_name(key).lower()
        headers_found[header_key] = (key, value.strip())
    return headers_found


def _parse_headers_and_body(s):
    ''' Takes a HTTP packet, and returns a tuple containing:
      _ the first line (e.g., "GET ...")
      _ the headers in a dictionary
      _ the body
    '''
    crlfcrlf = b"\r\n\r\n"
    crlfcrlfIndex = s.find(crlfcrlf)
    if crlfcrlfIndex != -1:
        headers = s[:crlfcrlfIndex + len(crlfcrlf)]
        body = s[crlfcrlfIndex + len(crlfcrlf):]
    else:
        headers = s
        body = b''

    try:
        first_line, headers = headers.split(b"\r\n", 1)
    except ValueError as e:
        raise ttproto.core.exceptions.DecodeError(s, HTTP, e)

    return first_line.strip(), _parse_headers(headers), body


def _dissect_headers(obj, s):
    """Takes a HTTP packet as the string s, and populates the scapy layer obj
    (either HTTPResponse or HTTPRequest). Returns the first line of the
    HTTP packet, and the body
    """
    first_line, headers, body = _parse_headers_and_body(s)
    for f in obj.fields_desc:
        # We want to still parse wrongly capitalized fields
        stripped_name = _strip_header_name(f.name).lower()
        try:
            _, value = headers.pop(stripped_name)
        except KeyError:
            continue
        obj.setfieldval(f.name, value)
    if headers:
        headers = {key: value for key, value in six.itervalues(headers)}
        obj.setfieldval('Unknown_Headers', headers)
    return first_line, body


def is_http_request(http_bytes):
    prog = re.compile(
        r"^(?:OPTIONS|GET|HEAD|POST|PUT|DELETE|TRACE|CONNECT) "
        r"(?:.+?) "
        r"HTTP/\d\.\d$"
    )
    crlfIndex = http_bytes.index("\r\n".encode())
    req = http_bytes[:crlfIndex].decode("utf-8")
    result = prog.match(req)

    if result:
        return True
    return False


def is_http_response(http_bytes):
    prog = re.compile(r"^HTTP/\d\.\d \d\d\d .*$")
    crlfIndex = http_bytes.index("\r\n".encode())
    req = http_bytes[:crlfIndex].decode("utf-8")
    result = prog.match(req)

    if result:
        return True
    return False


def get_http_header_by_id(value, id: str):
    """
    Returns first found tuple header (name, value) when header name "statsWith" id
    """

    headers = [(h['name'], h['value']) for h in value['headers']]

    for k, v in headers:
        print(k)
        print('comparing {} to {}'.format(str(k).lower(),id.lower()))
        if str(k).lower().startswith(id.lower()):
            return k, v

    return None


# - - - HTTP - - -

class HTTPHeader(
    metaclass=InetPacketClass,
    fields=[
        ("field-name", "name", str, ''),
        ("field-value", "value", str, ''),
        ("field-content", "content", bytes, b""),
    ]):

    def __init__(self, *k, **kw):
        if len(k) == 1:
            kw["value"] = k[0]
            k = ()
        super().__init__(*k, **kw)


class HTTPHeaderList(
    metaclass=InetOrderedListClass,
    content_type=HTTPHeader
):

    @classmethod
    def _decode_message(cls, bin_slice):
        logging.info('Decoding HTTP headers')

        _, headers, body = _parse_headers_and_body(bin_slice.raw())

        headers_vals = list()

        for v in headers.values():
            logging.debug('Parsing header {} {}'.format(v[0], v[1]))
            name = v[0].decode('utf-8')
            value = v[1].decode('utf-8')
            content = '{}: {}'.format(name, value).encode('utf-8')
            headers_vals.append(HTTPHeader(name=name, value=value, content=content))

        # note: the decoding of http doesnt relay too much on the byte structure like for other protocols
        remaining_slice = bin_slice

        if headers_vals:
            return cls(headers_vals), remaining_slice
        else:
            return None, remaining_slice


class HTTP(
    metaclass=InetPacketClass,
    fields=[
        # http common head fields
        ("Http-Version", "ver", str, Omit()),

        # request message fields
        ("Method", "method", Optional(str), Omit()),
        ("Request-Uri", "uri", Optional(str), Omit()),

        # response message fields
        ("Status-Code", "status", Optional(str), Omit()),
        ("Reason-Phrase", "reason", Optional(str), Omit()),

        # http common tail fields
        ("Headers", "headers", Optional(HTTPHeaderList), Omit()),
        ("Body", "body", Optional(str), Omit()),
        ("Payload", "pl", Optional(Value), Omit()),
    ],
):
    def describe(self, desc):
        """
        HTTP REQUEST described as: ver + method + uri
        HTTP RESPONSE described as: ver + status + reason
        """
        desc.info = '{} {} {}'.format(
            self['ver'],
            self['method'] if self['method'] else self['status'],
            self['uri'] if self['uri'] else self['reason'],
        )

        return True

    @classmethod
    def http_values_as_dict_from_slice(cls, bin_slice):

        values = dict()

        header_list_value, bin_slice = HTTPHeaderList._decode_message(bin_slice)

        if is_http_request(bin_slice.raw()):
            logging.info("HTTP message is request")

            first_line, headers, body = _parse_headers_and_body(bin_slice.raw())
            logging.info("HTTP first-line {}".format(first_line))
            logging.info("HTTP body {}".format(body))

            method, uri, version = re.split(br"\s+", first_line, 2)
            logging.debug('{} {} {}'.format(version, method, uri))

            remaining_slice = bin_slice.shift_bits(bin_slice.get_bit_length())
            logging.info("Remaining slice length: {}".format(remaining_slice.get_bit_length()))
            values.update({
                'ver': version.decode("utf-8"),
                'headers': header_list_value,
                'method': method.decode("utf-8"),
                'body': body.decode("utf-8"),
                'uri': uri.decode("utf-8"),
            })

        elif is_http_response(bin_slice.raw()):
            logging.debug("HTTP message is request")

            first_line, headers, body = _parse_headers_and_body(bin_slice.raw())
            logging.debug("HTTP first-line {}".format(first_line))

            version, status, reason = re.split(br"\s+", first_line, 2)
            logging.debug('{} {} {}'.format(version, status, reason))

            remaining_slice = bin_slice.shift_bits(bin_slice.get_bit_length())
            logging.debug("Remaining slice length: {}".format(remaining_slice.get_bit_length()))

            values.update({
                'ver': version.decode("utf-8"),
                'headers': header_list_value,
                'body': body.decode("utf-8"),
                'status': status.decode("utf-8"),
                'reason': reason.decode("utf-8"),
            })
        else:
            raise ttproto.core.exceptions.NotImplemented(
                "HTTP couldn't be parsed. Seems like either a non-compliant "
                "HTTP message or TCP stream not assembled correctly?")

        return values

    @classmethod
    def _decode_message(cls, bin_slice):
        """Implementation notes:
            - we dont decode byte by byte each field for HTTP, as data structure cannot be separated in well defined parts
            as for structured structures (like IP, UDP, etc).
            - given the previous statement bin_slices are not processed as normally done by other inet classes
        """

        if not bin_slice:
            raise ttproto.core.exceptions.DecodeError(bin_slice, cls, 'Got empty slice, nothing to decode')

        # decode http bin slice into dict of values
        http_params_as_dict = HTTP.http_values_as_dict_from_slice(bin_slice)
        # build HTTP of Value type
        http_value = HTTP(**http_params_as_dict)

        print("checking values which are none in the structure")
        for i, j in http_params_as_dict.items():
            if j is None:
                print(i)

        # check if we should decode HTTP with a special binding
        if ttproto.core.lib.inet.onem2m.is_oneM2M_HTTP(http_value):

            if http_value['status'] is None:
                logging.debug('HTTP body will be decoded as oneM2M Request')
                expected_type = ttproto.core.lib.inet.onem2m.OneM2MRequest

            elif http_value['method'] is None:
                logging.debug('HTTP body will be decoded as oneM2M Reply')
                expected_type = ttproto.core.lib.inet.onem2m.OneM2MResponse

            else:
                raise ttproto.core.exceptions.DecodeError(
                    bin_slice,
                    cls,
                    'Couldnt deduce oneM2M packet type from {}'.format(http_value)
                )
            http_params_as_dict.update({'pl': expected_type._decode_from_binding(http_value)})

            return HTTP(**http_params_as_dict),BinarySlice(buff=b'')  # oneM2M as payload of HTTP

        return http_value, BinarySlice(buff=b'')  # HTTP


    #     def decoder_func():
    #         nonlocal bin_slice
    #         v = None
    #         for f in cls.fields():
    #             t = yield v
    #             v, bin_slice = f.tag.decode_message(t if t else f.type, bin_slice, None)
    #             values.append(v)
    #         yield v
    #
    #
    #
    #     # prepare the decoder
    #     decoder = decoder_func()
    #     next(decoder)
    #
    #     def decode():
    #         return next(decoder)
    #
    #     def decode_if(cond):
    #         return decoder.send(None if cond else Omit)
    #
    #     def decode_as(type):
    #         return decoder.send(type)
    #
    #     # decode the base format
    #     dp = decode()
    #     tf = decode()
    #     nh = decode()
    #     hl = decode()
    #     cid = decode()
    #     sac = decode()
    #     sam = decode()
    #     m = decode()
    #     dac = decode()
    #     dam = decode()
    #
    #     # CID extension
    #     sci = decode_if(cid)
    #     dci = decode_if(cid)
    #
    #     # TF fields
    #     iecn = decode_if(tf != 3)
    #     idscp = decode_if(not (tf & 1))
    #     #ipad = decode_as(Omit if tf & 2  else (UInt2 if tf else UInt4))
    #     ifl = decode_if(not (tf & 2))
    #
    #     # NH field
    #     inh = decode_if(nh == 0)
    #
    #     # HLIM field
    #     ihl = decode_if(hl == 0)
    #
    #
    #     # def compute_multicast():
    #     #     if dac:
    #     #         # Stateful
    #     #         if dam == 0:
    #     #             pfx, length = cls.get_context(dci)
    #     #             return IPv6Address(b"".join((b"\xff", idst[:2], bytes((length,)), pfx[:8], idst[2:])))
    #     #         else:
    #     #             return IPV6_UNSPECIFIED_ADDRESS
    #     #     else:
    #     #         # Stateless
    #     #         if dam == 0:
    #     #             return idst
    #     #         elif dam == 1:
    #     #             return IPv6Address(b"".join((b"\xff", idst[:1], b"\0\0\0\0\0\0\0\0\0", idst[1:])))
    #     #         elif dam == 2:
    #     #             return IPv6Address(b"".join((b"\xff", idst[:1], b"\0\0\0\0\0\0\0\0\0\0\0", idst[1:])))
    #     #         else:
    #     #             return IPv6Address(b"\xff\2\0\0\0\0\0\0\0\0\0\0\0\0\0" + idst)
    #     #
    #     # dst = compute_multicast() if m else compute_unicast(dam, dac, idst, hwdst, dci)
    #
    #     # next compressed header
    #     if not nh:
    #         nhc = Omit()
    #         nhc_bin = b""
    #         next_header = inh
    #     else:
    #         # here were enter a pseudo_addr context because we may need to compute an IPv6 checksum
    #         # and enter and iid context because we may have compressed addresses
    #         with InetPacketValue.ipv6_pseudo_addresses_context((src, dst)), \
    #              cls.encapsulating_iid_context(src, dst):
    #
    #             nhc, bin_slice, nhc_bin, next_header = SixLowpanNHC.decompress(bin_slice)
    #     values.append(nhc)
    #
    #     if root_header:
    #         # Generate the new slice
    #         inner_slice = BinarySlice(concatenate((ipv6_bin, nhc_bin, bin_slice.as_binary())))
    #
    #         # Decode the payload
    #         payload, inner_slice = IPv6.decode_message(inner_slice)
    #         values.append(payload)
    #
    #         if inner_slice:
    #             raise Error("Buffer not fully decoded (%d remaining bits)" % inner_slice.get_bit_length())
    #
    #         return cls(*values), bin_slice.shift_bits(bin_slice.get_bit_length())
    #     else:
    #         values.append(Omit())
    #         return cls(*values), bin_slice, ipv6_bin + nhc_bin
    #
    # #__local = threading.local()

# tell the tcp module on which tcp ports http runs (hack for those servers not running in std port 80)
for port in (80,) + tuple(range(3000, 9999)):
    ttproto.core.lib.inet.tcp.tcp_port_map[port] = HTTP

ttproto.core.lib.inet.tcp.tcp_port_map[1026] = HTTP
