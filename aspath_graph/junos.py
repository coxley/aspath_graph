'''
junos.py
--------

This has several functions for getting AS PATHs from Junos via NETCONF
'''

from __future__ import print_function
from getpass import getpass
from jnpr.junos import Device


def netconf_paths(hostname, user, nopassword):  # -> list[str]
    '''Return AS PATHS from Junos NETCONF enabled device'''
    if nopassword:
        dev = Device(host=hostname, user=user)
    else:
        dev = Device(host=hostname, user=user, password=getpass())

    dev.open()
    bgp_routes = dev.rpc.get_route_information(terse=True, protocol='bgp')[1]

    paths = [rt.find('rt-entry').find('as-path').text for rt in bgp_routes
             if rt.tag == 'rt']
    return paths
