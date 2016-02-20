'''
utils.py
--------

Some common utilities
'''

from __future__ import print_function
import struct


def dedupe(items):
    # This function is required because set() doesn't mantain list order which
    # is important when dealing with paths
    seen = set()
    for item in items:
        if item not in seen:
            yield item
            seen.add(item)


def asn_to_label(asn, label_map={}, asdot=False):  # -> str
    '''Return label mapped to an ASN

    We follow a trend where if ASDOT notation, the value after the dot is
    metadata and before is the location. In this case let's name that

    asn: ASN as str
    label_map: dict of asn -> human label
    asdot: Whether to convert to ASDOT or not
    '''
    location = asn
    meta = 0

    # We separate the AS into location and meta. Not all people may follow
    # a convention like this which is why we can change suffix to '' below
    if asdot:
        if bytesize(int(asn)) > 2:
            dot = plain_to_dot(int(asn))
            location, meta = dot.split('.')

    # If label not found, default back to location
    location_name = label_map.get(location, location)
    # Rack switch ASNs are assumed to be (racknumber * 10) + 1
    # Anything else is considered anycast
    if all([meta, int(meta) % 10 == 1]):
        suffix = '-R%d' % (int(meta)/10)
    elif meta:
        suffix = '-CAST-%s' % meta
    else:
        suffix = ''

    return location_name + suffix


def plain_to_dot(asn):  # -> str
    '''Take ASPLAIN and return ASDOT notation'''
    barray = struct.pack('>I', asn)
    return '%d.%d' % struct.unpack('>HH', barray)


def bytesize(i):  # -> int
    '''Return bytesize'''
    return (i.bit_length() + 7) // 8


def link_paths(aspath, ownas=''):  # -> Dict[str, Any]
    '''Link AS PATH into pairs

    aspath: ASPath string
    ownas: AS to prepend to PATH
    '''
    # Remove the AS PATH origin keys
    path = aspath.split()
    path = [p for p in path if p not in ['?', 'I', 'E']]

    # Add our own AS to the beginning of the PATH
    path.insert(0, ownas)
    # Eliminate prepends, but still provide a list for .__getitem__ for zipping
    path = list(dedupe(path))

    return {'nodes': path, 'pairs': zip(path, path[1:])}
