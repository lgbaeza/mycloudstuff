# S3DistCP cross region

* Create state machine [sample](stepfunctions.json)
* Run

````json
{
    "cluster_id": "j-00000",
    "items": [{
        "localpath": "hdfs:///local-path",
        "source_endp": "s3.us-east-2.amazonaws.com",
        "source_s3": "s3://ursa-labs-taxi-data/",
        "dest_endp": "s3.us-east-1.amazonaws.com",
        "$dest_s3": "s3://bucket/prefix/...",
        "dest_encr": "--s3ServerSideEncryption"
    }]
}
````