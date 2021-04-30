import json
import boto3

InstanceType = "t3.micro"
YOUR_REGION = 'us-east-1' #REPLACE
YOUR_SUBNET_ID = '' #REPLACE
YOUR_SECURITY_GROUP = '' #REPLACE
YOUR_AMI_ID = "" #REPLACE
YOUR_INSTANCE_PROFILE='AsyncReportCreationRole'

ec2 = boto3.client('ec2')
ec2Resources = boto3.resource('ec2', region_name=YOUR_REGION)
def lambda_handler(event, context):
    Action = event['Action']
    EmailTarget = event['EmailTarget']
    IdReport = event['IdReport']
    
    if(Action == "Provision"):
        IdFind = ":" + event['NombreStateMachine'] + ":"
        IdIndex = IdReport.find(IdFind)
        IdLength = len(event['NombreStateMachine']) + 2
        IdReport = IdReport[IdIndex + IdLength: ]

    if(Action == "Provision"):
        InstanceId = provisionInstance(IdReport)
        return {
            'InstanceId': InstanceId,
            'IdReport': IdReport,
            'EmailTarget': EmailTarget
        }
    elif(Action == "Decommission"):
        InstanceId = event['InstanceId']
        state = decommissionInstance(InstanceId)
        if (state != "shutting-down"):
            raise Exception("Instance not shutting down: " + InstanceId)
            return {
                "Status": "Error"
            }
        else:
            return {
                'InstanceId': InstanceId,
                'IdReport': IdReport,
                'EmailTarget': EmailTarget
            }
        
def decommissionInstance(InstanceId):
    resTerminate = ec2.terminate_instances(
        InstanceIds=[InstanceId]
    )
    return resTerminate['TerminatingInstances'][0]['CurrentState']['Name']
    
def provisionInstance(IdReport):
    params = {}
    resRunInstance = ec2.run_instances(
        BlockDeviceMappings=[
            {
                'DeviceName': '/dev/sdh',
                'Ebs': {
                    'DeleteOnTermination': True,
                    'VolumeSize': 8,
                    'VolumeType': 'standard'
                }
            },
        ],
        ImageId=YOUR_AMI_ID,
        InstanceType=InstanceType,
        MaxCount=1,
        MinCount=1,
        Monitoring={
            'Enabled': False
        },
        SecurityGroupIds=[
            YOUR_SECURITY_GROUP
        ],
        SubnetId=YOUR_SUBNET_ID,
        EbsOptimized=False,
        IamInstanceProfile={
            'Name': YOUR_INSTANCE_PROFILE
        },
        InstanceInitiatedShutdownBehavior='stop',
        TagSpecifications=[
            {
                'ResourceType': 'instance',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': 'async-reports-' + IdReport
                    },
                    {
                        'Key': 'AsyncReports',
                        'Value': 'True'
                    }
                ]
            },
        ]
    )

    InstanceId = resRunInstance['Instances'][0]['InstanceId']
    return InstanceId