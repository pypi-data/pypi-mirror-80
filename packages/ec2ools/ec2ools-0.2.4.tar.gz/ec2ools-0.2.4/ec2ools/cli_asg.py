# -*- coding: utf-8 -*-

"""Console script for ec2ools."""
import sys
import json
import click
from ec2ools.aws.asg import (
    Asg
)
from ec2ools.aws import (
    ec2
)
ctx_settings = {
    'help_option_names': ['-h', '--help']
}

@click.group(context_settings=ctx_settings)
def main():
    pass


@main.command(name='is-oldest-instance', help=("Check if the instance is "
                                               "the oldest and exit 0 if "
                                               "true and exit 1 if not. "
                                               "If --instance_id/-i is not "
                                               "specified the current instanceId "
                                               "will be used."))
@click.option('--instance_id', '-i', type=str)
def is_oldest_instance(**kw):
    """
    """
    asg = Asg()

    res = asg.is_oldest_instance(kw.get('instance_id'))

    if not res:
        exit(1)
    exit(0)

@main.command('get-instances')
def get_asg_instances(**kw):
    """
    """
    id = 'i-0523e07206641cf70'
    # inst = ec2.Instance.from_metadata()
    inst = ec2.Instance(id)
    inst.load_tags()

    asg = Asg(inst.asg_name)
    asg_find = asg.get_instances()

    from pprint import pprint
    pprint(asg_find)


@main.command(name='get-asg')
def get_asg(**kw):
    pass

