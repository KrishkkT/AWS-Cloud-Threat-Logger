import boto3
import json
import gzip
import io
import urllib.parse

s3 = boto3.client('s3')
ses = boto3.client('ses', region_name='ap-south-1')

SENDER = "[Sender Email]"
RECIPIENT = "[Recipient Email]"

def lambda_handler(event, context):
    print("Lambda triggered.")

    for record in event.get('Records', []):
        bucket = record['s3']['bucket']['name']
        key = urllib.parse.unquote_plus(record['s3']['object']['key'])
        print(f"Processing file: {key}")

        try:
            response = s3.get_object(Bucket=bucket, Key=key)
            with gzip.GzipFile(fileobj=io.BytesIO(response['Body'].read())) as f:
                data = json.loads(f.read())

            for r in data.get('Records', []):
                event_name = r.get('eventName', '')
                error = r.get('errorCode', '')
                response_elements = r.get('responseElements')

                has_error = any(word in error for word in ['AccessDenied', 'Unauthorized', 'Fail'])
                is_failed_console_login = (
                    event_name == 'ConsoleLogin' and 
                    (response_elements is None or response_elements.get('ConsoleLogin') == 'Failure')
                )

                print(f"Event: {event_name} | Error: {error} | FailedLogin: {is_failed_console_login}")

                if has_error or is_failed_console_login:
                    print("⚠️ Failed login detected, sending email...")
                    ses.send_email(
                        Source=SENDER,
                        Destination={'ToAddresses': [RECIPIENT]},
                        Message={
                            'Subject': {'Data': '🚨 AWS Alert: Failed Login'},
                            'Body': {
                                'Text': {
                                    'Data': (
                                        "🚨 Failed Login Detected\n\n"
                                        f"User: {r.get('userIdentity', {}).get('arn', 'Unknown')}\n"
                                        f"IP: {r.get('sourceIPAddress', 'Unknown')}\n"
                                        f"Event: {event_name}\n"
                                        f"Error: {error or 'ConsoleLoginFailure'}\n"
                                        f"File: {key}\n"
                                    )
                                }
                            }
                        }
                    )
                    print("✅ Email sent.")
                else:
                    print("No failed login detected.")
        except Exception as e:
            print(f"❌ Error: {e}")
