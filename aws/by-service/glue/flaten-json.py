import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrame

args = getResolvedOptions(sys.argv, ["JOB_NAME"])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

SOURCE_S3_LOCATION = ''
TARTET_S3_LOCATION = ''
TARGET_PARTITION_KEYS = ["", ""]

#Read source data
dynamicframe = glueContext.create_dynamic_frame.from_options(
        format='json',connection_type='s3',
        connection_options = {"paths": [ SOURCE_S3_LOCATION]},
        transformation_ctx = "dynamicframe")

#Resolve choice: cast to string if multiple datatypes are present
dynamicframe_resolveChoice = dynamicframe.resolveChoice(
    choice='cast:string',
    transformation_ctx = "dynamicframe_resolveChoice")

#Relationalize: flatten json
dynamicframe_relational = dynamicframe_resolveChoice.relationalize("root","/home/glue/GlueLocalOutput")
dynamicframe_relational = dynamicframe_relational.select(list(dynamicframe_relational.keys())[0])

#Write data
glueContext.write_dynamic_frame.from_options(frame = dynamicframe_relational,
                            connection_type = "s3", 
                            format = "parquet",
                            transformation_ctx = "datasink",
                            connection_options = {"path": TARTET_S3_LOCATION, "partitionKeys": TARGET_PARTITION_KEYS})