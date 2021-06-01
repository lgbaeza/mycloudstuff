

1. Create DynamoDB Table
1. Create Lambda Function called dummy-dynamodb
    - [lambda.py](lambda.py)
    - [names.txt](names.txt)
    - [last.txt](last.txt)
1. Setup structure and table name on Lambda
1. Create Step Functions using [step.json](step.json)
1. Point Step Functions to your Lambda
1. Run a new execution with input:
```json
{
  "LOAD": "1000000",
  "ACTION": "PREPARE"
}
```
6. verify records created: 
```bash
aws dynamodb scan --table-name "table" --select "COUNT"
```