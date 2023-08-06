import pytest
import boto3
from pytest_mock import mocker
from ec2ools import aws

class Test:


    def test_get_region(self, mocker):
        """
        """
        co_mock = mocker.patch('ec2ools.aws.subprocess.check_output')
        co_mock.return_value = '{"region": "us-compton-1"}'

        assert aws.REGION is None
        assert aws.get_region() == 'us-compton-1'
        assert aws.REGION == 'us-compton-1'
        assert co_mock.call_count == 1

        # test caching
        assert aws.get_region() == 'us-compton-1'
        assert co_mock.call_count == 1


    def test_client(self, mocker):
        """
        """
        pass

    def test_metadata(self, mocker):
        """
        """
        co_mock = mocker.patch('ec2ools.aws.subprocess.check_output')
        co_mock.return_value = b'instance-id: i-testid'

        assert aws.metadata('instance-id') == 'i-testid'



    def test_metadata_exception(self, mocker):
        """
        """
        co_mock = mocker.patch('ec2ools.aws.subprocess.check_output')
        co_mock.return_value = '{"region": "us-compton-1"}'
