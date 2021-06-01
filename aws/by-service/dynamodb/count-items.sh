TABLENAME="table"
aws dynamodb scan --table-name $TABLENAME --select "COUNT"