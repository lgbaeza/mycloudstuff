import json
import boto3
import os

s3 = boto3.client('s3')
ses = boto3.client('ses')
YOUR_S3_BUCKET = "" #REPLACE
PREFIX = "async-reports/reportes/"
SOURCE_EMAIL = "" #REPLACE
EXPIRATION = 600

def lambda_handler(event, context):
    print(event)
    IdReporte = event['IdReporte']
    EmailTarget = event['EmailTarget']
    InstanceId = event['InstanceId']
    
    signedURL = generateUrl(IdReporte)
    htmlString = getTemplatedData(signedURL, IdReporte)
    print(htmlString)
    email = sendEmail(EmailTarget, htmlString)
    print(email)
    
    if (email.get('MessageId', 'ERROR') == "ERROR"):
        result = "ERROR"
        raise Exception("Error al enviar el email a " + EmailTarget)
    else:
        result = "SUCCESS" 
    
    return {
        'Result': result,
        "IdReporte": IdReporte,
        "InstanceId": InstanceId,
        "EmailTarget": EmailTarget
    }
    
def generateUrl(IdReporte):
    object_name = IdReporte + ".csv"
    s3presigned = s3.generate_presigned_url('get_object',Params={'Bucket': YOUR_S3_BUCKET,
        'Key': PREFIX + object_name},ExpiresIn=EXPIRATION)
    return s3presigned

def sendEmail(EmailTarget, htmlString):
    email = ses.send_email(
        Source=SOURCE_EMAIL,
        Destination={
            'ToAddresses': [EmailTarget]
        },
        Message={
            'Subject': {
                'Data': 'Tu descarga está lista'
            },
            'Body': {
                'Html': {
                    'Data': htmlString
                }
            }
        },
        Tags=[
            {
                'Name': 'string',
                'Value': 'string'
            },
        ]
    )
    return email
    
def getTemplatedData(signedURL, IdReporte):
    html_string = ''
    LOCAL_PATH = "/tmp/" + IdReporte + '.html'
    with open(LOCAL_PATH, 'wb') as f:
        s3.download_fileobj(YOUR_S3_BUCKET, 'async-reports/templates/emailtemplate.html', f)
        f.close()
    with open(LOCAL_PATH, 'r') as f:
        html_string = f.read()
        f.close()
    os.remove(LOCAL_PATH)
    
    html_string = html_string.replace("{S3_PRESIGN_URL}", signedURL)
    
    return html_string
    
    