import os

def s3_key_to_url(key: str) -> str:
    bucket = os.getenv("S3_BUCKET_NAME")
    region = os.getenv("AWS_REGION", "us-east-1")

    return f"https://{bucket}.s3.{region}.amazonaws.com/{key}"
