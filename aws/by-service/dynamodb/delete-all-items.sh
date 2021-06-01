TABLENAME="table"
aws dynamodb describe-table --table-name $TABLENAME | jq '.Table | del(.TableId, .TableArn, .ItemCount, .TableSizeBytes, .CreationDateTime, .TableStatus, .LatestStreamArn, .LatestStreamLabel, .ProvisionedThroughput.NumberOfDecreasesToday, .ProvisionedThroughput.LastIncreaseDateTime, .ProvisionedThroughput.LastDecreaseDateTime)' > schema.json
aws dynamodb delete-table --table-name $TABLENAME
aws dynamodb create-table --cli-input-json file://schema.json