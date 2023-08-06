import os
import requests
import boto3
import subprocess
import shlex
import json

EC2_METADATA='/usr/bin/ec2-metadata'
REGION=None

def client(name, region=None):
    """
    """
    if not region:
        region = get_region()
    return boto3.client(name, region_name=region)


def get_region():
    """ Get region from metadata
        and cache value in global
        constant
    """
    global REGION

    if os.environ.get("AWS_REGION"):
        REGION = os.environ.get("AWS_REGION")

    if REGION is None:
        cmd = "curl -s http://169.254.169.254/latest/dynamic/instance-identity/document"
        res = subprocess.check_output(shlex.split(cmd))
        REGION= json.loads(res)['region']
    return REGION


def metadata(name):
    """
    """
    arg = "--{}".format(name)

    cmd = "{} {}".format(EC2_METADATA, arg)

    try:
        res = subprocess.check_output(shlex.split(cmd))
        return res.decode().split(":")[1].strip()
    except Exception as e:
        print(str(e))



METADATA_HOST = "169.254.169.254"


class MetaService:

    _SESSION = None

    def __init__(self, revision='latest'):
        self.revision = revision

    @property
    def session(self):
        if MetaService._SESSION is None:
            sess = requests.Session()
            MetaService._SESSION = sess
        return MetaService._SESSION

    @property
    def url(self):
        return "http://{}/{}".format(
            METADATA_HOST,
            self.revision)

    def query(self, path):
        """ query path from the meta data service
        """
        req = self.session.get("{}/{}".format(self.url, path))

        if req.status_code != 200:
            raise Exception("Metadata query error: ", path)

        return req.text

    def query_meta(self, path):
        """ query a path from the meta-data namespace
        """
        res = self.query("meta-data/{}".format(path))
        return res

    def identity_doc(self):
        """ query the instance identity document
            and return json as a dict
        """
        res = self.query("dynamic/instance-identity/document")
        return json.loads(res)
