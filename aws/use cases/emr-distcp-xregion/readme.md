# S3DistCP cross region

This works for cross-account, kms encrypted destination buckets

* Create state machine [sample](stepfunctions.json)
* Add policy to destination bucket
* Add permission for destination account CMK to use on source account
* Add permission in source EMR EC2 profile to use destination bucket and CMK
* Run

````json
{
    "cluster_id": "j-00000",
    "items": [
        {
            "localpath": "hdfs:///local-path",
            "source_endp": "s3.us-east-2.amazonaws.com",
            "source_s3": "s3://ursa-labs-taxi-data/",
            "dest_endp": "s3.amazonaws.com",
            "$dest_s3": "s3://bucket/prefix1/...",
            "dest_encr": "--s3ServerSideEncryption",
            "acl": "bucket-owner-full-control",
            "cmk_arn:" "ARN_CMK_TARGET"
        },
        {
            "localpath": "hdfs:///local-path",
            "source_endp": "s3.amazonaws.com",
            "source_s3": "s3://nyc-tlc/trip data/",
            "dest_endp": "s3.us-east-2.amazonaws.com",
            "$dest_s3": "s3://bucket2/prefix2/...",
            "dest_encr": "--s3ServerSideEncryption",
            "acl": "bucket-owner-full-control",
            "cmk_arn:" "ARN_CMK_TARGET"
        }
    ]
}
````