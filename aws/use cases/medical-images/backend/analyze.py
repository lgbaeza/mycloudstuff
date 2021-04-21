import boto3
import json
import os

S3_BUCKET = ''
S3_PREFIX = 'textract-comprehend'
S3_PREFIX_OUTPUT = 'output'
DYNAMODB_TABLE = ''
LOCAL_PATH_TO_IMAGES = "images/"

def uploadFile(filepath):
    s3resource = boto3.resource('s3') 
    s3 = boto3.client('s3')
    path = filepath[:filepath.rindex("/")+1]
    filename = filepath.replace(path, "")
    s3Key = S3_PREFIX + '/' + filename
    s3OutKey = S3_PREFIX + '/' + S3_PREFIX_OUTPUT + '/' + filename
    
    s3resource.Bucket(S3_BUCKET).upload_file(filepath, s3Key)
    print("upload s3")
    return s3Key
    
def processImage(s3Key):
    results = {}
    textract = boto3.client('textract')
    translate = boto3.client('translate')
    comprehend = boto3.client('comprehend')
    comprehendMedical = boto3.client('comprehendmedical')
    
    ## TEXTRACT
    textractResponse = textract.detect_document_text(
        Document={
            'S3Object': {
                'Bucket': S3_BUCKET,
                'Name': s3Key
            }
        }
    )
    
    fullText = ''
    for block in textractResponse['Blocks']:
        if(block['BlockType'] == 'LINE'):
            fullText += block['Text'] + '\n'
    print('textract')
    results['fullText'] = fullText
    
    ### PROCESS WITH COMPREHEND
    comprehendResponse = comprehend.detect_entities(
        Text=fullText,
        LanguageCode='es'
    )
    print('comprehend')
    results['comprehend'] = comprehendResponse['Entities']
    
    ### TRANSLATE
    responseTranslate = translate.translate_text(
        Text=fullText,
        SourceLanguageCode='es',
        TargetLanguageCode='en'
    )
    fullTextEN = responseTranslate['TranslatedText']
    print("translated to EN")
    results['fullTextEN'] = fullTextEN
    
    ### PROCESS WITH COMPREHEND MEDICAL
    responseMedical = comprehendMedical.infer_icd10_cm(
        Text=fullTextEN
    )
    print("comprehendMedical")
    results['comprehendMedical'] = responseMedical['Entities']
    
    return results

def saveOutputDB(key, results):
    dynamodb = boto3.client('dynamodb')
    response = dynamodb.put_item(
        TableName=DYNAMODB_TABLE,
        Item={
            'image_id': {
                'S': key
            },
            'fullText': {
                'S': results['fullText']
            },
            'fullTextEN': {
                'S': results['fullTextEN']
            },
            'comprehend': {
                'S': json.dumps(results['comprehend'])
            },
            'medical': {
                'S': json.dumps(results['comprehendMedical'])
            },
            's3key': {
                'S': results['s3key']
            },
            's3bucket': {
                'S': results['s3bucket']
            }
        }
    )

def main():
    path = LOCAL_PATH_TO_IMAGES
    cwd = os.getcwd() + "/" + path
    for image in os.listdir(cwd):
        print("****" + image)
        s3key = uploadFile(path + image)
        results = processImage(s3key)
        results['s3key'] = s3key
        results['s3bucket'] = S3_BUCKET
        saveOutputDB(image, results)
    
main()
