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

![image_alt]()





