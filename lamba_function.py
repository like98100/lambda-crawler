import boto3
import requests
from datetime import datetime

s3 = boto3.client('s3')

def lambda_handler(event, context):
    try:
        url = "https://land.naver.com/"
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        html = response.text

        now = datetime.utcnow().strftime('%Y-%m-%dT%H-%M-%S')
        key = f"naver-land/land-{now}.html"
        bucket = "like98100-crawling-bucket"  # ← 본인의 S3 버킷 이름으로 수정

        s3.put_object(
            Bucket=bucket,
            Key=key,
            Body=html,
            ContentType='text/html'
        )

        return {
            "statusCode": 200,
            "body": f"Saved to s3://{bucket}/{key}"
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": str(e)
        }
