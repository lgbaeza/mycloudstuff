import boto3

iam = boto3.client('iam')
policies = iam.list_policies(
	Scope='Local',
    OnlyAttached=False,
	MaxItems=1000
)

for policy in policies['Policies']:
	if(policy['AttachmentCount'] == 0):
		versions = iam.list_policy_versions(PolicyArn=policy['Arn'])
		for ver in versions['Versions']:
			if(ver['IsDefaultVersion'] == False):
				deleteVersion = iam.delete_policy_version(PolicyArn=policy['Arn'],VersionId=ver['VersionId'])
		response = iam.delete_policy(PolicyArn=policy['Arn'])
		print("deletd " + policy['PolicyName'])
