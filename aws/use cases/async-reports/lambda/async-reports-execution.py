import json
import boto3
import time

YOUR_S3_BUCKET = '' #REPLACE
YOUR_UTILITY_BUCKET = '' #REPLACE
YOUR_AWS_REGION = 'us-east-1'
YOUR_CW_LOGGROUP = '/aws/SSM/RunCommand/async-reports' #REPLACE

ssm = boto3.client('ssm')
TIMEOUT = 1800
def lambda_handler(event, context):
    print(event)
    InstanceId = event['InstanceId']
    IdReporte = event['IdReporte']
    EmailTarget = event['EmailTarget']
    TaskToken = event['TaskToken']
    
    result = runCommand(InstanceId, IdReporte, EmailTarget, TaskToken)
    #result = "MOCK"
    #raise Exception("Sorry, no numbers below zero")
    return {
        'InstanceId': InstanceId,
        'IdReporte': IdReporte,
        'EmailTarget': EmailTarget
    }
    
def runCommand(InstanceId, IdReporte, EmailTarget, TaskToken):
    output = '{\"InstanceId\":\"' + InstanceId + '\",\"IdReporte\":\"' + IdReporte + '\",\"EmailTarget\":\"' + EmailTarget + '\"}'
    output = json.dumps({
        "InstanceId":InstanceId,
        "IdReporte": IdReporte,
        "EmailTarget": EmailTarget
    })
    print(output)
    response = ssm.send_command(
        InstanceIds=[InstanceId],
        DocumentName='AWS-RunShellScript',
        TimeoutSeconds=TIMEOUT,
        Comment=IdReporte,
        Parameters={
            'commands':[ 
                'mkdir reports',
                'cd reports',
                'aws s3 cp s3://' + YOUR_UTILITY_BUCKET + '/async-reports/scripts/exportdb.php .',
                'aws s3 cp s3://' + YOUR_UTILITY_BUCKET + '/async-reports/scripts/runexport.sh .',
                'aws s3 cp s3://' + YOUR_UTILITY_BUCKET + '/async-reports/scripts/rds-combined-ca-bundle.pem .',
                'sh runexport.sh ' + IdReporte,
                "aws s3 cp " + IdReporte + ".csv s3://" + YOUR_S3_BUCKET + "/async-reports/reportes/" + IdReporte + ".csv",
                'AWS_DEFAULT_REGION=' YOUR_AWS_REGION ' aws stepfunctions send-task-success --task-output \'' + output + '\' --task-token ' + TaskToken
            ],
            'workingDirectory': [ "/home/ssm-user/" ],
            'executionTimeout': [ "1800" ]
        },
        CloudWatchOutputConfig={
            'CloudWatchLogGroupName': YOUR_CW_LOGGROUP,
            'CloudWatchOutputEnabled': True
        }
    )
    
    commandResponse = response.get('Command', None)
    commandId = commandResponse.get("CommandId", None)
    print("CommandID: " + commandId)
    result = commandResponse.get('Status', "FAILED") if commandResponse else "FAILED"
    if(result == "FAILED"):
        raise Exception("Error al ejecutar el reporte: " + result)
    
    return result 