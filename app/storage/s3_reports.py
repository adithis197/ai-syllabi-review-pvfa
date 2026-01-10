import boto3
import os

S3_BUCKET = os.getenv("S3_BUCKET")

s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION"),
)

def generate_presigned_url(key: str, expires=300):
    return s3.generate_presigned_url(
        "get_object",
        Params={
            "Bucket": S3_BUCKET,
            "Key": key,
        },
        ExpiresIn=expires,
    )

def list_all_reports():
    paginator = s3.get_paginator("list_objects_v2")
    reports = []

    for page in paginator.paginate(
        Bucket=S3_BUCKET,
        Prefix="reports/"
    ):
        for obj in page.get("Contents", []):
            key = obj["Key"]
            if not key.endswith(".pdf"):
                continue

            parts = key.split("/")
            course_code = parts[1] if len(parts) > 2 else "Unknown"
            filename = os.path.basename(key)

            presigned_url = generate_presigned_url(key)

            reports.append({
                "course_code": course_code,
                "url": presigned_url,          # ✅ REQUIRED
                "display_name": filename,      # ✅ REQUIRED
                "s3_key": key
            })

    reports.reverse()
    return reports

