""" bolt11 CLI """

import sys

import click

# import json
from .decode import decode as bolt11_decode

# disable tracebacks on exceptions
sys.tracebacklimit = 0


@click.group()
def command_group():
    """
    Python CLI for BOLT11 invoices
    decode bolt11 invoices
    """


@click.command()
@click.argument("bolt11", type=str)
def decode(bolt11):
    """
    decode a bolt11 invoice
    """
    decoded = bolt11_decode(bolt11)
    click.echo(decoded.json)


def main():
    """main function"""
    command_group.add_command(decode)
    command_group()


if __name__ == "__main__":
    main()
