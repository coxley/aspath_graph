import click
from click.testing import CliRunner
from aspath_graph.cli import cli


def test_basic_exec():
    runner = CliRunner()
    results = {
        'help': runner.invoke(cli, ['--help']),
        'help_h': runner.invoke(cli, ['-h']),
        'version': runner.invoke(cli, ['--version']),
        'version_v': runner.invoke(cli, ['-v']),
    }
    exit_codes = set(result.exit_code for result in results.values())
    all_zero = len(exit_codes) == 1 and 0 in exit_codes
    assert all_zero
