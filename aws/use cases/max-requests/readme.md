# Max Requests Sample
Some times, as developers we want to build cool new fatures on the cloud but we still need to interact with legacy resources that don't scale. Often, this resources have constraints such as maximum requests per second that enable IT operators to handle the load.
Since it's a known pattern to decouple applications using queue management systems, to address the situation explained before, I built a simple component using AWS Step Functions, SQS and Lambda, that will buffer the requests you need to perform to this non-scalable resources such as SOAP services or REST APIs.

### Architecture
![Architecture](https://github.com/lgbaeza/mycloudstuff/blob/main/aws/use%20cases/max-requests/architecture.png?raw=true)

### How it works
1. Push your requests to be made to SQS
2. A CloudWatch Alarm determines when the State machine should run
3. The State Machine invokes a Lambda functions that counts the amount of messages on the queue and creates an array variable with length = amount of messages/10 (max messages allowed by SQS ReceiveMessages API)
4. Map state of the State Machine invokes several times in parallel a Lambda function (controlled with MaxConcurrency)
5. Each Lambda invocation performs the HTTP Request to your resources and stores the result somewhere for you to pickup
6. The workflow of the State Machine determines if there are still messages in SQS and repeats

### AWS Step Functions Orchestration
![State Machine Image](https://github.com/lgbaeza/mycloudstuff/blob/main/aws/use%20cases/max-requests/step-graph.png?raw=true)

### Test results
![Test Results](https://github.com/lgbaeza/mycloudstuff/blob/main/aws/use%20cases/max-requests/test-results.png?raw=true)

### Get started
* [Cloud Formation with sample resources available ](https://raw.githubusercontent.com/lgbaeza/mycloudstuff/main/aws/use%20cases/max-requests/cloud-formation-template.yaml)

