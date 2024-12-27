# Automated Backup System for AWS EC2 with S3 Storage

## Project Overview
This project automates the backup process for AWS EC2 instances by periodically creating snapshots of EBS volumes and storing snapshot metadata in an S3 bucket. It also implements lifecycle management to clean up old snapshots and metadata files.

---

## Key Features
- **Automated Snapshot Creation**: Takes regular snapshots of a specified EBS volume.
- **Metadata Management**: Stores snapshot metadata as JSON files in an S3 bucket.
- **Retention Policy**: Deletes snapshots and metadata older than the defined retention period (default: 15 days).
- **Monitoring and Alerts**: Utilizes AWS CloudWatch for task scheduling, monitoring, and logging.

---

## Architecture

### Components
1. **AWS Lambda**:
   - Core logic for creating, managing, and cleaning up snapshots and metadata.
2. **Amazon EC2**:
   - Instance hosting the EBS volume to be backed up.
3. **Amazon S3**:
   - Storage for metadata files associated with snapshots.
4. **AWS CloudWatch**:
   - Schedules Lambda functions via cron expressions.
   - Monitors logs and metrics for backup operations.
5. **IAM Role**:
   - Grants Lambda the necessary permissions for EC2, S3, and CloudWatch interactions.

### Diagram
*(Insert architecture diagram here)*

---

## Prerequisites
1. AWS Account.
2. IAM Role with the following permissions:
   - `ec2:CreateSnapshot`, `ec2:DescribeSnapshots`, `ec2:DeleteSnapshot`.
   - `s3:PutObject`, `s3:DeleteObject`.
   - `logs:CreateLogGroup`, `logs:CreateLogStream`, `logs:PutLogEvents`.
3. Configured AWS CLI or AWS Management Console access.
4. An EC2 instance with an attached EBS volume.

---

## Setup

### 1. **Create an S3 Bucket**
```bash
aws s3api create-bucket --bucket ec2-backup-metadata-bucket-12 --region <region>
```
### 2. Set Up the Lambda Function

#### Deploy the Python Script
- Use the provided `lambda_function.py` script.

#### Steps:
1. **Create a Lambda Function**:
   - Create a new Lambda function via the **AWS Management Console** or **AWS CLI**.
2. **Upload the Script**:
   - Package the `lambda_function.py` script into a `.zip` file and upload it to the Lambda function.
3. **Assign IAM Role**:
   - Assign an IAM role to the Lambda function with the required permissions:
     - `ec2:CreateSnapshot`, `ec2:DescribeSnapshots`, `ec2:DeleteSnapshot`
     - `s3:PutObject`, `s3:DeleteObject`
     - `logs:CreateLogGroup`, `logs:CreateLogStream`, `logs:PutLogEvents`
4. **Set Environment Variables**:
   - Configure the following environment variables for the Lambda function:
     - `VOLUME_ID`: EBS volume ID (e.g., `vol-07fe2661320289fa4`).
     - `S3_BUCKET_NAME`: Name of the S3 bucket (e.g., `ec2-backup-metadata-bucket-12`).

---

### 3. Configure CloudWatch Rule

#### Steps:
1. **Create CloudWatch Events Rule**:
   - Use the AWS CLI to create a CloudWatch Events rule that triggers the Lambda function every 10 minutes:
     ```bash
     aws events put-rule --schedule-expression "rate(10 minutes)" --name EC2SnapshotRule
     ```
2. **Add Lambda Function as Target**:
   - Add the Lambda function as the target for the created rule. This ensures the Lambda function runs automatically as per the defined schedule.

## Testing

1. **Deploy the Lambda Function**:
   - Ensure the Lambda function is deployed with the correct script and configuration.

2. **Trigger the Function**:
   - Manually trigger the Lambda function or allow it to run automatically via the CloudWatch rule.

3. **Verify**:
   - Check the **EC2 Snapshots** section in the AWS Management Console to confirm snapshots are created.
   - Verify that metadata files are stored in the **S3 bucket**.
   - Ensure old snapshots and metadata are deleted after the retention period.

---

## Monitoring

1. **CloudWatch Logs**:
   - Review the CloudWatch logs for any errors or debugging information.

2. **S3 Object Management**:
   - Confirm that metadata files are present and accurate in the S3 bucket.

3. **EC2 Console**:
   - Ensure snapshots are created and deleted as per the configured lifecycle.
  
![snap](https://github.com/user-attachments/assets/e80f0d2e-909e-49cd-818e-a5f3a937d10c)

![snapshot](https://github.com/user-attachments/assets/0e23d3a9-8749-4f41-8690-88ab2c4a6273)



