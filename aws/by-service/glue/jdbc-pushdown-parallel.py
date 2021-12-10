import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrame
import re

args = getResolvedOptions(sys.argv, ["JOB_NAME"])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

onprem_endpoint = "*****"
query = "*****"
dbname = "*****"
dbtable = "*****"
user = "*****"
dbpassword = "'*****"

rowCountDF = spark.read \
    .format("jdbc") \
    .option("url", "jdbc:sqlserver://" + onprem_endpoint + ":1433;databaseName=" + dbname) \
    .option("dbtable",dbtable) \
    .option("user", user) \
    .option("password", dbpassword) \
    .load()
    
rowCountDF.createOrReplaceTempView(dbtable)
rowCount = spark.sql(query).count()

filteredDF = spark.read \
    .format("jdbc") \
    .option("url", "jdbc:sqlserver://" + onprem_endpoint + ":1433;databaseName=" + dbname) \
    .option("dbtable", dbtable) \
    .option("user", user) \
    .option("password", dbpassword) \
    .option("numPartitions",4) \
    .option("lowerBound",1) \
    .option("upperBound",rowCount) \
    .option("partitionColumn","id") \
    .load()
    
filteredDF.createOrReplaceTempView(dbtable)

SQLServertable_node1 = DynamicFrame.fromDF(spark.sql(query), glueContext, "SQLServertable_node1")

#replace with your own mapping
# Script generated for node ApplyMapping
ApplyMapping_node2 = ApplyMapping.apply(
    frame=SQLServertable_node1,
    mappings=[
        ("longtext", "string", "longtext", "string"),
        ("month", "string", "month", "string"),
        ("city", "string", "city", "string"),
        ("name", "string", "name", "string"),
        ("id", "int", "id", "int"),
    ],
    transformation_ctx="ApplyMapping_node2",
)

# Script generated for node SQL Server table
SQLServertable_node3 = glueContext.write_dynamic_frame.from_catalog(
    frame=ApplyMapping_node2,
    database="target_glue_dbname",
    table_name="target_glue_tablename",
    transformation_ctx="SQLServertable_node3",
)

job.commit()
