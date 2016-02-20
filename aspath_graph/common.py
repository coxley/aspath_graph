from __future__ import print_function
import struct
import click


def error(msg):
    click.secho('ERROR: %s' % msg, fg='red', err=True)


def info(msg):
    click.secho('INFO: %s' % msg, fg='blue', err=True)


def success(msg):
    click.secho('SUCCESS: %s' % msg, fg='green', err=True)


ASN_MAP = {
    '65036': 'IAD1',
    '65044': 'SFO2',
    '65056': 'DEVC',
    '65300': 'SFO2_DEV',
    '64600': 'CORP_WAN',
    '65201': 'CORP_SFO2',
    '65202': 'CORP_IAD1',
    '9059': 'AWS_EU',
    '7224': 'AWS',
}
AWS = [7224, 9059]



