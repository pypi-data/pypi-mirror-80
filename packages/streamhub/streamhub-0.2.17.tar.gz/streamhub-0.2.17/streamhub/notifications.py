import boto3
from botocore.exceptions import ClientError


def set_aws_access_key_id(aws_access_key_id):
    global AWS_ACCESS_KEY_ID
    AWS_ACCESS_KEY_ID = aws_access_key_id

def set_aws_secret_access_key(aws_secret_access_key):
    global AWS_SECRET_ACCESS_KEY
    AWS_SECRET_ACCESS_KEY = aws_secret_access_key

def set_region(aws_region):
    global AWS_REGION
    AWS_REGION = aws_region

def send_aws_email(source_email, destination_addresses, subject, body, charset):

    boto3.setup_default_session(aws_access_key_id=AWS_ACCESS_KEY_ID,
                                aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    SES = boto3.client('ses', AWS_REGION)

    try:
        response = SES.send_email(
            Source=source_email,
            Destination={
                'ToAddresses': destination_addresses
            },
            Message={
                'Subject': {
                    'Data': subject,
                    'Charset': charset
                },
                'Body': {
                    'Html': {
                        'Data': body,
                        'Charset': charset
                    }
                }
            }
        )
        print(response)
    except ClientError as e:
        print(e)
        raise Exception(e)
    finally:
        exit(-1)
