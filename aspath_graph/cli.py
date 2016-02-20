'''
CLI
---

cli.main is the entrypoint for the program, which should call to cli()
'''

from __future__ import print_function
import os
import json
import yaml
import click
import aspath_graph
import SimpleHTTPServer
from aspath_graph.junos import netconf_paths
from aspath_graph.transform import link_paths, generate_netjson


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
MODES = click.Choice(['junos-netconf', 'txt'])
WB = click.File('wb')
RB = click.File('r')


@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument('input')
@click.version_option(None, '-v', '--version')
@click.option('--mode', '-m', type=MODES, default='txt', help='Mode to use')
@click.option('--output', '-o', default='-', type=WB, help='Output file')
@click.option('--asdot', is_flag=True, help='Whether to add ASDOT notation')
@click.option('--ownas',
              default='',
              help='Apply perspective of own AS at the beginning of PATHS')
@click.option('--runserver', is_flag=True, help='Run local server on 8000')
@click.option('--user',
              default=lambda: os.environ.get('USER', ''),
              help="Only used for relevant modes")
@click.option('--nopassword', is_flag=True,
              help="If using a login mode, this will enable public key auth")
@click.option('--yaml', type=RB, help="YAML for mapping and ignoring ASes")
@click.option('--pprint', is_flag=True, help="Pretty print JSON")
@click.pass_context
def cli(ctx, **kwargs):
    '''aspath_graph converts raw ASPATHs to NetJSON Graph

    NetJSON is a series of JSON schema for defining networks, NetJSON Graph
    being specific to defining how nodes interconnect. "aspath_graph" uses this
    to represent BGP autonomous systems as 'nodes' and how they connect from
    the perspective of INPUT

    INPUT can either be a device or file depending on value of MODE. This
    defaults to a file. (txt)

    OUTPUT can be '-' to send results to STDOUT.

    If not passing '--nopassword', you will be prompted for a password for the
    relevant modes.

    When using "--asdot" to provide ASDOT notation, the raw ASPLAIN will also
    be provided on the node - just under the "raw" attribute.

    YAML can be formatted as such: (Note that "ignore" must ONLY be ASPLAIN)

        \b
        ---
        label_map:
            65001: SFO
            65002: ORD
            65003: NYC
            65003.1: NYC-R1
            65003.2: NYC-R2
        ignore:
            - 7224
            - 9059

    By default, ASDOT will be labeled according to the firsthalf. Eg, if 65001
    is configured to be labeled as DFW, 65001.211 will appear as DFW-R21. This
    assumes your ToR ASN is your spine ASN + (racknumber*10+1) - to disable
    this simply set APG_ASDOT_RAW to true/yes/anything.

    Any of the supported options can be passed via ENV by upping the case,
    replacing '-' with '_', and prefixing with 'APG'. Eg, 'APG_MODE'
    '''
    LABEL_MAP, IGNORE_LIST = parse_yaml(kwargs['yaml'])
    raw_paths = []
    if kwargs['mode'] == 'txt':
        # Click can intelligently open standard streams and files
        with click.open_file(kwargs['input']) as f:
            raw_paths = f.readlines()

    elif kwargs['mode'] == 'junos-netconf':
        # This must return as a list of stringed paths (think readlines)
        raw_paths = netconf_paths(kwargs['input'],
                                  kwargs['user'],
                                  kwargs['nopassword'])

    all_nodes = set()
    all_pairs = set()
    for path_string in raw_paths:
        path_calc = link_paths(path_string, ownas=kwargs['ownas'])
        all_nodes.update(path_calc['nodes'])
        all_pairs.update(path_calc['pairs'])

    netjson = generate_netjson(all_nodes, all_pairs,
                               lmap=LABEL_MAP, ignore=IGNORE_LIST,
                               asdot=kwargs['asdot'], ownas=kwargs['ownas'])

    if kwargs.get('pprint'):
        kwargs['output'].write(json.dumps(netjson, indent=2))
    else:
        kwargs['output'].write(json.dumps(netjson))

    if kwargs.get('runserver'):
        # This will change directory into the pkg's static directory, create
        # netjson.json, and run SimpleHTTPServer
        webpath = os.path.abspath(
                os.path.dirname(aspath_graph.__file__) + '/static')
        os.chdir(webpath)
        with open('netjson.json', 'w') as f:
            f.write(json.dumps(netjson))

        import sys
        sys.argv[1] = 8000
        SimpleHTTPServer.test()


def parse_yaml(f):  # -> tuple
    '''Parse YAML, returning label_map and ignore list'''
    if f:
        content = yaml.load(f)
    else:
        content = {}

    label_map = content.get('label_map', {})
    ignore_list = content.get('ignore', [])
    return (label_map, ignore_list)


def main():
    cli(obj={}, auto_envvar_prefix='APG')  # obj is for sharing between ctx
