'''
transform.py
------------

Ad-hoc functions that deal with transforming into what we want
'''

from __future__ import print_function
from aspath_graph.utils import dedupe, plain_to_dot, bytesize, asn_to_label


def link_paths(aspath, ownas=''):  # -> Dict[str, Any]
    '''Link AS PATH into pairs

    aspath: ASPath string
    ownas: AS to prepend to PATH
    '''
    # Remove the AS PATH origin keys
    path = aspath.split()
    path = [p for p in path if p not in ['?', 'I', 'E']]

    # Add our own AS to the beginning of the PATH if provided
    if ownas:
        path.insert(0, ownas)
    # Eliminate prepends, but still provide a list for .__getitem__ for zipping
    path = list(dedupe(path))

    return {'nodes': path, 'pairs': zip(path, path[1:])}


def generate_netjson(
        nodes,
        pairs,
        lmap={},
        ignore=[],
        asdot=False,
        ownas=''
):  # -> Dict[str, Any]
    '''Return NetJSON data as dict

    nodes: list of nodes with no repeats
    pairs: list of len=2 tuples
    lmap: dict of asn -> human name
    ignore: list of asns to ignore
    asdot: Whether to transform 4-byte ASPLAIN to ASDOT
    '''
    nodes_metadata = []
    links = []
    for node in nodes:

        # Test for ignored ASNs, if so skip.
        # Since input is via YAML, string and ints are tough for many so let
        # both (at this point only ASPLAIN should be in ignore)
        if str(node) in ignore or int(node) in ignore:
            continue

        if asdot and bytesize(int(node)) > 2:
                name = plain_to_dot(int(node))
        else:
            name = node

        metadata = {
            'id': name,
            # TODO: Add support to query NSoT or something for extra properties
            # such as datacenter, function, etc
            'label': asn_to_label(str(name)),
            'properties': {
                'rawAs': node,
            },
        }
        nodes_metadata.append(metadata)

    for source, target in pairs:

        # Test for ignored ASNs, if so skip
        source_in_ignore = str(source) in ignore or int(source) in ignore
        target_in_ignore = str(target) in ignore or int(target) in ignore
        if source_in_ignore or target_in_ignore:
            continue

        cost = 1.0

        if bytesize(int(source)) > 2:
            source = plain_to_dot(int(source))
        if bytesize(int(target)) > 2:
            target = plain_to_dot(int(target))

        link = {
            'source': source,
            'target': target,
            'cost': cost,
            'cost_text': '',
            'properties': {},
        }
        links.append(link)

    if ownas:
        if asdot and bytesize(int(ownas)) > 2:
            router_id = plain_to_dot(int(ownas))
        else:
            router_id = ownas
    else:
        router_id = 'Own AS not provided'

    return {
        'type': 'NetworkGraph',
        'protocol': 'oslr',
        'version': '0.6.6',
        'revision': '5031a799fcbe17f61d57e387bc3806de',
        'metric': 'etx',
        'router_id': router_id,
        'nodes': nodes_metadata,
        'links': links,
    }
