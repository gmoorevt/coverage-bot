import boto3
from botocore.exceptions import NoCredentialsError

class S3FileManager:
    def __init__(self, aws_access_key_id, aws_secret_access_key, region_name, bucket_name):
        self.s3 = boto3.client(
            's3',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name
        )
        self.bucket_name = bucket_name

    def list_files(self):
        try:
            response = self.s3.list_objects_v2(Bucket=self.bucket_name)
            files = [obj['Key'] for obj in response.get('Contents', [])]
            return files
        except NoCredentialsError as e:
            print(f"Error: {e}")
            return []

    def get_public_url(self, file_key):
        try:
            url = self.s3.generate_presigned_url(
                'get_object',
                Params={'Bucket': self.bucket_name, 'Key': file_key},
                ExpiresIn=3600  # URL expiration time in seconds (1 hour in this example)
            )
            return url
        except NoCredentialsError as e:
            print(f"Error: {e}")
            return None

    def upload_file(self, local_file_path, s3_key):
        try:
            self.s3.upload_file(local_file_path, self.bucket_name, s3_key)
            print(f"File uploaded successfully to S3 with key: {s3_key}")
        except NoCredentialsError as e:
            print(f"Error: {e}")
        except FileNotFoundError:
            print(f"Error: The file {local_file_path} was not found.")

# # Example usage:
# aws_access_key_id = 'YOUR_ACCESS_KEY'
# aws_secret_access_key = 'YOUR_SECRET_KEY'
# region_name = 'YOUR_REGION'
# bucket_name = 'YOUR_BUCKET_NAME'

# s3_manager = S3FileManager(
#     aws_access_key_id=aws_access_key_id,
#     aws_secret_access_key=aws_secret_access_key,
#     region_name=region_name,
#     bucket_name=bucket_name
# )

# # Upload a file to the S3 bucket
# local_file_path = 'path/to/local/file.txt'  # Replace with the path to your local file
# s3_key = 'uploaded/file.txt'  # Replace with the desired key for the file in S3
# s3_manager.upload_file(local_file_path, s3_key)
