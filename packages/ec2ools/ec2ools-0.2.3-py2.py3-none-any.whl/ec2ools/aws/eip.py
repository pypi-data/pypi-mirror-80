import sys
import os
from ec2ools import aws
from ec2ools.aws import MetaService


class EipBase:

    def allocate_eip(self, alloc_id):
        """
        """
        meta = MetaService()
        instance_id = meta.query_meta('instance-id')
        eip_info = self._query_eip(alloc_id)

        if not eip_info:
            raise Exception("Invalid AllocationID")

        aws.client('ec2').associate_address(
            InstanceId=instance_id,
            AllocationId=eip_info['AllocationId'])

    def _query_eip(self, alloc_id):
        """ Query EIP record by allocation ID

        Args:
            alloc_id (str): Allocation ID of path to file containing Allocation ID

        Return
            (dict): The EIP record dict
        """
        if self._is_path(alloc_id):
            alloc_id = self._read_path(alloc_id)

        ip = aws.client('ec2').describe_addresses(AllocationIds=[alloc_id])

        if ip.get('Addresses'):
            return ip.get('Addresses')[0]

    def _is_path(self, path):
        """
        """
        if os.path.exists(path):
            return True
        return False

    def _read_path(self, path):
        """
        """
        with open(path, 'r') as f:
            return f.read().strip()
