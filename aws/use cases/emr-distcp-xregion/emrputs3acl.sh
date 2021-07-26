S3_PATH=$1
ACL=$2
CMK_ARN=$3
aws s3 cp --recursive --acl $ACL $S3_PATH $S3_PATH --metadata-directive REPLACE --sse aws:kms --sse-kms-key-id $CMK_ARN