1. Create glue connector for Hudi
2. Setup DMS Full Load + CDC    
    * make sure to specify extra connection attribute includeOpForFullLoad=true
2. crawl tables
3. create hudi job based on [script.py](script.py)
    * Replace \<GLUEDATABASE\>
    * Replace \<BUCKETNAME\> and \<PATH\>

4. create step functions based on [step.json](step.json)
5. run step functions. use INIT for initial load and UPSERT for subsequent runs from CDC
````json
{
  "load_type": "UPSERT",
  "tables": [
    {
      "tablename": "table1",
      "precombine_field": "precombine1",
      "pk_col": "pk1",
      "partition_field": "partitionfield1"
    },
    {
      "tablename": "table2",
      "precombine_field": "precombine2",
      "pk_col": "pk2",
      "partition_field": "partitionfield2"
    },
    {
      "tablename": "table3",
      "precombine_field": "precombine3",
      "pk_col": "pk3",
      "partition_field": "partitionfield3"
    }
  ]
}
````