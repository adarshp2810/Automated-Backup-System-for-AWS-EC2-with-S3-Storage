import boto3
import json
from datetime import datetime, timedelta

# Initialize clients
ec2_client = boto3.client('ec2')
s3_client = boto3.client('s3')

# Environment variables
VOLUME_ID = 'your-vol-id'
S3_BUCKET_NAME = 'your-bucket name'

def lambda_handler(event, context):
    try:
        # Create EC2 snapshot
        snapshot = create_snapshot()

        # Store metadata in S3
        store_metadata(snapshot)

        # Cleanup old snapshots and metadata
        cleanup_old_data()

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Snapshot created successfully',
                'snapshotId': snapshot['SnapshotId']
            })
        }
    except Exception as e:
        print(f"Error: {str(e)}")
        raise

def create_snapshot():
    response = ec2_client.create_snapshot(
        VolumeId=VOLUME_ID,
        Description=f"Automated backup - {datetime.utcnow().isoformat()}"
    )
    return response

def store_metadata(snapshot):
    metadata = {
        'snapshotId': snapshot['SnapshotId'],
        'volumeId': snapshot['VolumeId'],
        'startTime': snapshot['StartTime'].isoformat(),
        'state': snapshot['State'],
        'progress': snapshot.get('Progress', None),
        'volumeSize': snapshot['VolumeSize']
    }

    s3_client.put_object(
        Bucket=S3_BUCKET_NAME,
        Key=f"snapshots/{snapshot['SnapshotId']}.json",
        Body=json.dumps(metadata),
        ContentType='application/json'
    )

def cleanup_old_data():
    cutoff_date = datetime.utcnow() - timedelta(days=15)  # 15 days retention

    # Get all snapshots for the volume
    response = ec2_client.describe_snapshots(
        OwnerIds=['self'],
        Filters=[{'Name': 'volume-id', 'Values': [VOLUME_ID]}]
    )

    snapshots = response.get('Snapshots', [])

    for snapshot in snapshots:
        snapshot_time = snapshot['StartTime'].replace(tzinfo=None)
        if snapshot_time < cutoff_date:
            # Delete EC2 snapshot
            ec2_client.delete_snapshot(SnapshotId=snapshot['SnapshotId'])

            # Delete metadata from S3
            s3_client.delete_object(
                Bucket=S3_BUCKET_NAME,
                Key=f"snapshots/{snapshot['SnapshotId']}.json"
            )
