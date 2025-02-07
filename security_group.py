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
