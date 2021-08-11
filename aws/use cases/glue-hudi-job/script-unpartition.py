import sys
from pyspark.context import SparkContext
from pyspark.sql.session import SparkSession
from awsglue.transforms import *
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrame
from awsglue.utils import getResolvedOptions
from pyspark.sql.types import *
from datetime import datetime
from pyspark.sql.functions import concat, col, lit

args = getResolvedOptions(sys.argv, ['JOB_NAME','tablename','pk_col','precombine_field','load_type'])

spark = SparkSession.builder.config('spark.serializer','org.apache.spark.serializer.KryoSerializer').config('spark.sql.hive.convertMetastoreParquet','false').getOrCreate()
sc = spark.sparkContext
glueContext = GlueContext(sc)
job = Job(glueContext)

database = '<GLUEDATABASE>'
tablename = args['tablename']
pk_col = args['pk_col']
precombine_field = args['precombine_field']
load_type = args['load_type']
s3_out_path = 's3://<BUCKETNAME>/<PATH>/'+tablename

job.init(args['JOB_NAME']+'-'+tablename, args)

datasource0 = glueContext.create_dynamic_frame.from_catalog(database = database, table_name = tablename, transformation_ctx = "datasource0")

commonConfig = {'className' : 'org.apache.hudi', 'hoodie.datasource.hive_sync.use_jdbc':'false', 'hoodie.datasource.write.precombine.field': precombine_field, 'hoodie.datasource.write.recordkey.field': pk_col, 'hoodie.table.name': tablename+'_stg', 'hoodie.consistency.check.enabled': 'true', 'hoodie.datasource.hive_sync.database': database, 'hoodie.datasource.hive_sync.table': tablename+'_stg', 'hoodie.datasource.hive_sync.enable': 'true', 'path': s3_out_path}
initLoadConfig = {'hoodie.bulkinsert.shuffle.parallelism': 68, 'hoodie.datasource.write.operation': 'bulk_insert'}
loadconfig = {'hoodie.upsert.shuffle.parallelism': 68, 'hoodie.datasource.write.operation': 'upsert', 'hoodie.cleaner.policy': 'KEEP_LATEST_COMMITS', 'hoodie.cleaner.commits.retained': 10}
unpartitionDataConfig = {'hoodie.datasource.hive_sync.partition_extractor_class': 'org.apache.hudi.hive.NonPartitionedExtractor', 'hoodie.datasource.write.keygenerator.class': 'org.apache.hudi.keygen.NonpartitionedKeyGenerator'}

if(load_type == 'UPSERT'):
    combinedConf = {**commonConfig, **unpartitionDataConfig, **loadconfig}
else:
    combinedConf = {**commonConfig, **unpartitionDataConfig, **initLoadConfig}

datasink = glueContext.write_dynamic_frame.from_options(frame = datasource0, connection_type = "marketplace.spark", connection_options = combinedConf, transformation_ctx = "datasink")
job.commit()