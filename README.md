# AWS-VPC-Security-Scanner

"Securing The Cloud"

# Technical Architecture

![image_alt](https://github.com/Tatenda-Prince/AWS-VPC-Security-Scanner/blob/0dd2fb8b5605532b6a8a7b557a8eeaa56978cf81/img/Screenshot%202025-02-07%20125959.png)

## Project Overview

AWS VPC Security Scanner is an automated solution that scans security groups in an AWS environment to detect unrestricted inbound rules (0.0.0.0/0). It logs findings to CloudWatch, sends SNS alerts for misconfigurations, and stores logs in S3 for compliance. Additionally, it supports real-time monitoring using EventBridge.

## Project Objectives

1.Identifies open security groups with unrestricted inbound rules.

2.Logs findings to AWS CloudWatch.

3.Sends alerts via Amazon SNS.

4.Stores security findings in Amazon S3 for compliance.

5.Supports real-time monitoring using Amazon EventBridge.

## Prerequisites

1.AWS Account: Ensure you have an AWS account with sufficient permissions to create and manage resources.

2.AWS CLI: Install and configure the AWS CLI on your local machine.

3.IAM Permissions: Ensure you have the necessary IAM permissions to create and manage resources like Lambda, CloudWatch, SNS, S3, and EventBridge.

## Use Case 

You work as Security Cloud Enginner at Up The Chelsea healthcare provider needs to ensure that their cloud resources, like databases and web servers, aren't exposed to the public internet unnecessarily. The VPC security scanner alerts them whenever such misconfigurations occur.


## Step 1: Create an S3 Bucket for Compliance Logging

1.1.Go to the S3 Console.


1.2.Click Create Bucket.

1.3.Provide a unique name (e.g., `vpc-security-logs`).

Choose the region where your VPC resides.

![image_alt](https://github.com/Tatenda-Prince/AWS-VPC-Security-Scanner/blob/98ddb03dadd01dc089560616b8e645d296fd8083/img/Screenshot%202025-02-07%20123034.png) 


1.4.Enable Versioning and Server-Side Encryption (SSE) for compliance.

![image_alt](https://github.com/Tatenda-Prince/AWS-VPC-Security-Scanner/blob/6bd82f57c388175f137715e0bc74a75757c5838b/img/Screenshot%202025-02-07%20123055.png) 

Click Create Bucket.


1.5.As you can see the bucket was successfully created 

![image_alt](https://github.com/Tatenda-Prince/AWS-VPC-Security-Scanner/blob/4f2e0f656a1bffb7145ecff7f47d235adbf193d7/img/Screenshot%202025-02-07%20123127.png) 


## Step 2: Create an SNS Topic for Alerts

2.1.Go to the SNS Console.

2.2.Click Create Topic.

Provide a name (e.g., `VPC-Security-Alerts`).

![image_alt](https://github.com/Tatenda-Prince/AWS-VPC-Security-Scanner/blob/92d7b18aa884894b592ea9902e4bdbfd6f6758bd/img/Screenshot%202025-02-07%20123314.png)



Click Create Topic.

2.3.Subscribe your email or other endpoints to the topic for receiving alerts.


![image_alt](https://github.com/Tatenda-Prince/AWS-VPC-Security-Scanner/blob/9d65e50cc15c309cc845e57671f543933cb05e31/img/Screenshot%202025-02-07%20123531.png)


2.4.Make sure you confirm the subscription

![image_alt](https://github.com/Tatenda-Prince/AWS-VPC-Security-Scanner/blob/e84970a308135c3133c2ce7747c740a02bfd2acd/img/Screenshot%202025-02-07%20123559.png)


## Step 3: Create a Lambda Function to Scan Security Groups

Go to the Lambda Console.

3.1.Click Create Function.

3.2.Choose Author from scratch.

Provide a name (e.g., VPCSecurityScanner).

Choose Python 3.x as the runtime.


![image_alt](https://github.com/Tatenda-Prince/AWS-VPC-Security-Scanner/blob/fa77e0a59491aea4e9640bd0cb6c6643618f3bc2/img/Screenshot%202025-02-07%20123721.png)

3.3.Under Permissions, create a new IAM role with the following permissions:

`ec2:DescribeSecurityGroups`

`logs:CreateLogGroup`, `logs:CreateLogStream`, `logs:PutLogEvents`

`s3:PutObject`

`sns:Publish`

![image_alt](https://github.com/Tatenda-Prince/AWS-VPC-Security-Scanner/blob/a4ca62b8ae7459afa9d9142e9935b571b33ad2a1/img/Screenshot%202025-02-07%20123746.png)


3.4.Click Create Function.

## Step 4: Write the Lambda Function Code


4.1.In the Lambda function, paste the following Python code:

```python
import boto3
import json
from datetime import datetime

def lambda_handler(event, context):
    # Initialize AWS clients
    ec2 = boto3.client('ec2')
    s3 = boto3.client('s3')
    sns = boto3.client('sns')
    
    # Initialize response variables
    open_security_groups = []
    sns_topic_arn = 'arn:aws:sns:us-east-1:664418964175:VPC-Security-Alerts'  # Replace with your actual ARN
    bucket_name = 'tatenda-vpc-security-logs'  # Replace with your actual bucket name
    
    try:
        # Describe Security Groups to find open ones
        security_groups = ec2.describe_security_groups()['SecurityGroups']
        
        for sg in security_groups:
            for permission in sg['IpPermissions']:
                for ip_range in permission.get('IpRanges', []):
                    if ip_range['CidrIp'] == '0.0.0.0/0':  # Open to the world
                        open_security_groups.append(sg['GroupId'])
        
        # Check if any open security groups were found
        if open_security_groups:
            # Log findings to CloudWatch
            print(f"Open Security Groups Found: {open_security_groups}")
            
            # Send SNS alert
            sns.publish(
                TopicArn=sns_topic_arn,
                Message=f"Open Security Groups Found: {open_security_groups}",
                Subject="VPC Security Alert"
            )
            
            # Log findings to S3
            timestamp = datetime.utcnow().isoformat()
            s3.put_object(
                Bucket=bucket_name,
                Key=f"open-sg-findings/{timestamp}.json",
                Body=json.dumps(open_security_groups)
            )
            
        else:
            print("No open security groups found.")
        
    except Exception as e:
        # Catch and log any errors that occur during the process
        print(f"Error occurred: {str(e)}")
        sns.publish(
            TopicArn=sns_topic_arn,
            Message=f"Error in VPC Security Scanner: {str(e)}",
            Subject="VPC Security Alert"
        )
    
    return {
        'statusCode': 200,
        'body': json.dumps('Security Group Scan Complete')
    }

```

4.2.Replace `YOUR_REGION` and `YOUR_ACCOUNT_ID` with your AWS region and account ID.


4.3.Deploy the Lambda function.


## Step 5: Schedule the Lambda Function with EventBridge

Go to the EventBridge Console.

5.1.Click Create Rule.

Provide a name (e.g., VPCSecurityScannerRule).


Under Event Source, choose Schedule.

![image_alt](https://github.com/Tatenda-Prince/AWS-VPC-Security-Scanner/blob/e1fc5e1f28cd56c1df20b75092b32807ae1838e4/img/Screenshot%202025-02-07%20124345.png)



5.3.Set a fixed rate (e.g., 5 minutes) or a cron expression (e.g., cron(0/5 * * * ? *)).

![image_alt](https://github.com/Tatenda-Prince/AWS-VPC-Security-Scanner/blob/08c0e744b57eea100435c7ab955ddbba821e2e08/img/Screenshot%202025-02-07%20124444.png)

Under Targets, select the Lambda function you created (VPCSecurityScanner).


![image_alt](https://github.com/Tatenda-Prince/AWS-VPC-Security-Scanner/blob/352a0aa943852b1edf6fb1d0ebf5ea97201946bc/img/Screenshot%202025-02-07%20124506.png)


Click Create.


## Step 6: Test the Solution

6.1.Manually trigger the Lambda function to ensure it works.

Test the Function:

Click the Test button at the top of the Lambda function page.

In the Configure Test Event dialog, choose Create New Test Event.

Provide an event name (e.g., TestEvent).

Use the following JSON as the test event (you can leave it empty or use a simple even

```language
json
{
  "key1": "value1",
  "key2": "value2"
}

```

Click Create.

Click Test again to trigger the Lambda function.


Check Execution Results:

After the function runs, you’ll see the execution results in the Execution Results tab.

Look for a `statusCode: 200` and a message like `Security Group Scan Complete.`



![image_alt](https://github.com/Tatenda-Prince/AWS-VPC-Security-Scanner/blob/317c672318676ab2b8b64e1bc1ad8949bac9a7d0/img/Screenshot%202025-02-07%20124824.png)



6.2.Check CloudWatch Logs for output.


![image_alt]()


6.3.Verify that SNS alerts are sent.


![image_alt]()


6.4.Confirm that logs are stored in the S3 bucket.





