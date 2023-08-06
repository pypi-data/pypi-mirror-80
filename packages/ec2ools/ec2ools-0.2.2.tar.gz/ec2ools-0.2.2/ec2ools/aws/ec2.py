from ec2ools.aws import MetaService, client

class Instance:

    def __init__(self, instance_id):
        super().__init__()
        self.instance_id = instance_id
        self.asg_name = None
        self.tags = []

    @classmethod
    def from_metadata(cls):
        """ Alternate constructor to instantiate
            an Instance instance from ec2 metadata
            service
        """
        ms = MetaService()
        inst_id = ms.query_meta('instance-id')

        new = cls(inst_id)

        return new

    def load_tags(self):
        """ load ec2 instance tags.
            check for and set the following tags as props
            - autoscaling group name
        """
        if len(self.tags) > 0:
            return

        ec2c = client("ec2")

        res = ec2c.describe_tags(Filters=[
            {
                'Name': 'resource-id',
                'Values': [self.instance_id]
            }
        ])

        for t in res['Tags']:
            # we did filter but lets dbl check
            if t['ResourceId'] != self.instance_id:
                continue
            self.tags.append(t)
            if t['Key'] == 'aws:autoscaling:groupName':
                self.asg_name = t['Value']

    def return_my_asg(self):
        """ find and return an asg
            instance this instance
            is a member of
        """
        self.load_tags()
