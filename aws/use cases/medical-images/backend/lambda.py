import json
import boto3
DYNAMODB_TABLE = ''
CLOUDFRONT_URL = ""
API_KEY = ""

def lambda_handler(event, context):
    if(event['requestContext']['http']['method']=="GET" and event['queryStringParameters']['key'] == API_KEY):
        response = getItems()
    else:
        response = []
    return {
        'statusCode': 200,
        'body': json.dumps(response),
        'headers': {
            'content-type': "application/json",
            "Access-Control-Allow-Origin": CLOUDFRONT_URL,
            "Access-Control-Allow-Methods": "GET",
            "Access-Control-Allow-Headers" : "Content-Type"
        }
    }
    
def createPresignURL(s3key, s3bucket):
    s3 = boto3.client('s3')
    response = s3.generate_presigned_url(ClientMethod='get_object', Params={'Bucket': s3bucket, 'Key': s3key}, ExpiresIn=60)
    #print(response)
    return response
    
def getItems():
    dynamodb = boto3.client('dynamodb')
    response = dynamodb.scan(
        TableName=DYNAMODB_TABLE,
        Select='ALL_ATTRIBUTES'
    )
    results = []
    for item in response['Items']:
        results.append({
            'fullTextEN': item['fullTextEN']['S'],
            'fullText': item['fullText']['S'],
            's3path': createPresignURL(item['s3key']['S'], item['s3bucket']['S']),
            'image_id': item['image_id']['S'],
            'medical': json.loads(item['medical']['S']),
            'comprehend': json.loads(item['comprehend']['S'])
        })
    return results