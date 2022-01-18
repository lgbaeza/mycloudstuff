# Glue data prepro
This example runs an AWS Glue job in response to an object being uploaded to Amazon S3. Requirements:
* A state machine starts when a file is uploaded to a specific path of an Amazon S3 Bucket, using Eventbridge rule for S3 notifications
* Incoming file is not UTF-8 encoded, so preprocessing is performed by an AWS Lambda function
* After finishing preprocessing, the glue job is run

# Steps to deploy
1. Create an AWS Lambda function with [sample package provided](csvencodings.py.zip)
2. Provide your own bucket and path for processed files at line 8 and 9
````python
# output bucket name
OUTPUT_BUCKET_NAME=''
OUTPUT_PATH = ""
````

3. Create the AWS Glue Job

4. Create the AWS Step Functions machine using [sample state machine definition provided](stepfunctions.json)
5. Replace the 000000000000 at line 11 with your own AWS account id 
````json
        "FunctionName": "arn:aws:lambda:us-east-1:000000000000:function:csvencoding"
````
6. Replace csvencoding at line 31 for the name of your job name 
````json
    "Glue StartJobRun": {
      "Type": "Task",
      "Resource": "arn:aws:states:::glue:startJobRun.sync",
      "Parameters": {
        "JobName": "csvencoding"
      },
      "End": true
    }
````
7. Create an AWS EventBridge rule using the following example pattern. Replace **BUCKETNAME** with your own bucket name and **path/to/input/files/** with your own path
````json
{
  "source": ["aws.s3"],
  "detail-type": ["Object Created"],
  "detail": {
    "bucket": {
      "name": ["BUCKETNAME"]
    },
    "object": {
      "key": [{
        "prefix": "path/to/input/files/"
      }]
    }
  }
}
````
8. Add the state machine created on step 4 as the target