# Python Imports
import io
import gzip
import pickle
from typing import Any, Optional

# Third Party Imports
import boto3

class S3Wrapper:
    def __init__(self):
        self._client = boto3.client('s3')

    def put_object_pickled_gzip(self, s3_bucket: str, s3_key: str, obj: Any) -> bool:
        """Put a pickled python object"""
        assert isinstance(s3_bucket, str)
        assert isinstance(s3_key, str)
        assert object is not None

        # Convert Object to Pickled GZIP File
        gz_buffer = io.BytesIO()
        with gzip.GzipFile(mode='w', fileobj=gz_buffer) as gz_file:
            pickle.dump(obj, gz_file)  # Saves 50% of space!

        response = self._client.put_object(
            Bucket=s3_bucket, Body=gz_buffer.getvalue(), Key=s3_key)
        assert response['ResponseMetadata']['HTTPStatusCode'] == 200

    def get_object_pickled_gzip(self, s3_bucket: str, s3_key: str) -> Optional[bytes]:
        assert isinstance(s3_bucket, str)
        assert isinstance(s3_key, str)

        response = self._client.get_object(Bucket=s3_bucket, Key=s3_key)
        http_status_code = response['ResponseMetadata']['HTTPStatusCode']
        assert http_status_code == 200
        with gzip.open(response['Body'], 'rb') as f_in:
            pickled_obj = f_in.read()  # Extract GZIP
            unpickled_obj = pickle.loads(pickled_obj)  # Un-pickle
        return unpickled_obj
        