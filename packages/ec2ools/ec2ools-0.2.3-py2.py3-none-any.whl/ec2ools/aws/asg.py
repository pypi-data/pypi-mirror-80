import os
import sys
import json
from ec2ools.aws import (
    client, metadata)
import jmespath

from pprint import pprint
IS_PY2=False

if sys.version_info[0] < 3:
    IS_PY2=True


def sort_instances_by_launch(instances, reverse=False):
    """
    """
    instances.sort(key=lambda x: (x['LaunchTime'], x['InstanceId']), reverse=reverse )
    return instances


class AsgBase:

    def get_asg_by_instance(self, instance_id=None):
        """
        """
        if not instance_id:
            instance_id = metadata('instance-id')

        res = client('autoscaling').describe_auto_scaling_instances(
            InstanceIds=[instance_id])

        print(res)
        if len(res.get('AutoScalingInstances')) <= 0:
            return

        asg_info = res.get('AutoScalingInstances')[0]

        return asg_info


class Asg(AsgBase):

    def __init__(self, asg_name):
        self.asg_name = asg_name

    def get_instances(self):
        """
        """

        res = client('autoscaling').describe_auto_scaling_groups(
            AutoScalingGroupNames=[self.asg_name])

        if len(res.get('AutoScalingGroups', [])) <= 0:
            return

        inst = res.get('AutoScalingGroups')[0].get('Instances')

        ids = [
            i['InstanceId']
            for i in inst
        ]

        res = client('ec2').describe_instances(
            InstanceIds=ids)


        try:
            instances = jmespath.search("Reservations[].Instances[]", res)
            return instances
        except Exception as e:
            print(str(e))


    def is_oldest_instance(self, instance_id=None):
        """
        """
        if not instance_id:
            instance_id = metadata('instance-id')

        info = self.get_asg_by_instance(instance_id)

        asg_name = info['AutoScalingGroupName']

        inst = self.get_instances(asg_name)

        inst = sort_instances_by_launch(inst)

        if inst[0]['InstanceId'] == instance_id:
            return True
        return False


