# -*- coding: utf-8 -*-

"""Console script for ec2ools."""
import sys
import click
from ec2ools.aws.eip import EipBase


@click.group()
def main(args=None):
    pass


@main.command(name='allocate')
@click.argument('id',
              type=str)
def eip_allocate(**kw):

    print(kw)

    eip = EipBase()
    eip.allocate_eip(kw.get('id'))

if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
