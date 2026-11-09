# Week 07 write up
### Concepts: AWS Lambda, API Gateway, DynamoDB, IAM execution roles, SQS, and dead-letter queues.

This week, I deployed PropertyLite's individual property lookup using API Gateway, Lambda, and DynamoDB. I also created an SQS queue with a dead-letter queue and verified that I could send and receive a test message.

Before starting, I rebuilt the database resources from Week 04 because I had deleted them during cleanup. I used a temporary EC2 instance to connect to private RDS, imported rets_property.sql, and repeated the data cleanup before returning to DynamoDB. When transferring the SQL file from WSL, I needed to use the /mnt/c/Users/... path instead of the Windows C:\Users\... path.

## Request path

The request path is: my laptop → API Gateway → Lambda → DynamoDB, with the result returned through Lambda and API Gateway to my laptop.

From WSL, I sent an HTTPS request using curl to the GET /properties/{id} route. API Gateway passes the listing ID to the get-property Lambda function through pathParameters. Lambda uses that ID as the L_ListingID partition key in a DynamoDB GetItem request, then returns the listing as JSON. If no item matches, the function returns a 404 response.

Lambda uses its IAM execution role to access DynamoDB. I scoped its permission to dynamodb:GetItem on the Properties table instead of granting broad DynamoDB access. RDS and EC2 were used to prepare the data; they are not part of the serverless request path.

## Troubleshooting

Initially, the API returned "Hello from Lambda!" because the function was still running its default starter code. I replaced that code and clicked Deploy. I also added conversion for DynamoDB's Decimal values so numeric fields could be serialized into JSON.

After deploying, the API returned "Internal Server Error." I checked the Lambda logs in CloudWatch and found an AccessDeniedException. The function was trying to access DynamoDB in us-east-2, while my Properties table and IAM policy referenced us-east-1. I fixed this by explicitly setting region_name="us-east-1" in the boto3 DynamoDB resource. The next curl request successfully returned the listing.

## SQS and the dead-letter queue

I created property-dlq and linked it to property-queue through a redrive policy with maxReceiveCount set to 3. This allows messages that repeatedly receive delivery attempts without being deleted to move to the dead-letter queue once the receive limit is exceeded.

The queue creation command initially failed because a copied line break broke the JSON string and the handbook's ARN placeholder had not been replaced. I corrected the JSON and supplied the actual DLQ ARN and queue URLs. I then successfully sent and received a test message. This verified the main queue's operation; I did not yet test a message moving into the dead-letter queue.

The main troubleshooting lesson this week was to use CloudWatch logs to identify the actual Lambda error and check region settings across the code, resources, and IAM policy.
