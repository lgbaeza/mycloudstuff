import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext, DynamicFrame
from awsglue.job import Job
from pyspark.sql.functions import lit

args = getResolvedOptions(sys.argv, ["JOB_NAME"])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

# Params
s3Path= "s3://bucket_name/path"

vertices = [{
    "label": "label1",
    "sqlQuery": """
        select concat("label1_", pk) as id,  
        'label1' as label,
        attr1, attr2, attr3
        from database.table
        where pk <> 'pk'
    """,
    "mappings": [
        ("id", "string", "~id", "string"),
        ("label", "string", "~label", "string"),
        ("attr1", "string", "attr1:string", "string"),
        ("attr2", "string", "attr2:string", "string"),
        ("attr3", "string", "attr3:string", "string")
    ],
    "partitions": 1,
    "s3Path": f"{s3Path}/vertices_label1/"
}]

edges = [{
    "label": "vlabel1_elabel_vlabel2",
    "sqlQuery": """
        select concat(
            'vlabel1_', pk1, '__elabel__', 'vlabel2_', pk2
        ) as id, 
        concat('vlabel1_', pk1) as node_from, 
        concat('vlabel2_', pk2) as node_to, 
        'elabel' as label 
    from database.table p
        where pk <> 'ok'
    """,
    "mappings": [
        ("id", "string", "~id", "string"),
        ("node_from", "string", "~from", "string"),
        ("node_to", "string", "~to", "string"),
        ("label", "string", "~label", "string")
    ],
    "partitions": 1,
    "s3Path": f"{s3Path}/edges_vlabel1_elabel_vlabel2/"
}]

def processTable(tableParams):
    # Read
    df = spark.sql(tableParams["sqlQuery"])
    dfCoalesce = df.coalesce(tableParams["partitions"])
    glueDF = DynamicFrame.fromDF(dfCoalesce, glueContext, "glueDF")

    # Map
    dfMapped = ApplyMapping.apply(
        frame=glueDF,
        mappings=tableParams["mappings"],
        transformation_ctx="dfMapped",
    )

    # Write
    writeDF = glueContext.write_dynamic_frame.from_options(
        frame=dfMapped,
        connection_type="s3",
        format="csv",
        connection_options={
            "path": tableParams['s3Path'],
            "partitionKeys": [],
        },
        transformation_ctx="writeDF",
    )

for vertex in vertices:
    processTable(vertex)
    
for edge in edges:
    processTable(edge)

job.commit()
