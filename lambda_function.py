import json
import os
import boto3
from bunq.sdk.context.api_context import ApiContext
from bunq.sdk.context.bunq_context import BunqContext
from bunq.sdk.model.generated.endpoint import PaymentApiObject
from bunq.sdk.model.generated.object_ import AmountObject
from bunq.sdk.model.generated.endpoint import RequestInquiryApiObject
from bunq.sdk.model.generated.endpoint import MonetaryAccountBankApiObject
from bunq import ApiEnvironmentType

from bunq.sdk.model.generated.object_ import PointerObject

# Initialize S3 client to retrieve API context file
s3 = boto3.client('s3')

def lambda_handler(event, context):
    try:
        # Get API context file from S3
        bucket_name = os.environ['BUCKET_NAME']
        api_context_key = os.environ['API_CONTEXT_KEY']
        
        # Download API context file from S3
        s3.download_file(bucket_name, api_context_key, '/tmp/bunq_api_context.conf')
        
        # Restore API context from file
        api_context = ApiContext.restore('/tmp/bunq_api_context.conf')
        BunqContext.load_api_context(api_context)
        
        # Access the user context
        user_context = BunqContext.user_context()
        
        # Get the user ID
        user_id = user_context.user_id
        
        # Get the primary monetary account
        primary_account = user_context.primary_monetary_account.id_
        
        results = {
            'user_id': user_id,
            'primary_account': primary_account
        }
        
        # Check which operation to perform based on event input
        operation = event.get('operation', 'status')
        
        if operation == 'payment':
            # Make a payment to another user using proper Pointer object
            payment_id = PaymentApiObject.create(
                amount=AmountObject(event.get('amount', '1.00'), event.get('currency', 'EUR')),
                counterparty_alias=PointerObject(
                    type_=event.get('pointer_type', 'EMAIL'),
                    name=event.get('recipient_name', 'Recipient Name'),  # Ensure name is included
                    value=event.get('recipient_value', 'fcornetti+trainee@bunq.com')
                ),
                description=event.get('description', 'Payment from Lambda')
            ).value
            results['payment_id'] = payment_id
            
        elif operation == 'request':
            # Create a payment request
            request_id = RequestInquiryApiObject.create(
                AmountObject(event.get('amount', '10.00'), event.get('currency', 'EUR')),
                PointerObject(
                    type_=event.get('pointer_type', 'EMAIL'),
                    name=event.get('recipient_name', 'Payment Request Recipient'),
                    value=event.get('recipient_value', 'sugardaddy@bunq.com')
                ),
                event.get('description', 'Please pay for dinner'),
                allow_bunqme=event.get('allow_bunqme', False)
            ).value
            results['request_id'] = request_id
            
        elif operation == 'iban_payment':
            # Make a payment to another account using IBAN
            payment_id = PaymentApiObject.create(
                amount=AmountObject(event.get('amount', '5.00'), event.get('currency', 'EUR')),
                counterparty_alias=PointerObject(
                    type_='IBAN',
                    name=event.get('recipient_name', 'IBAN Recipient'),
                    value=event.get('iban', 'NL63BUNQ2090666315')
                ),
                description=event.get('description', 'Transfer to savings')
            ).value
            results['payment_id'] = payment_id
            
        elif operation == 'new_account':
            # Create a new monetary account
            account_id = MonetaryAccountBankApiObject.create(
                currency=event.get('currency', 'EUR'),
                description=event.get('description', 'Savings Account')
            ).value
            results['account_id'] = account_id
        
        return {
            'statusCode': 200,
            'body': json.dumps(results)
        }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e),
                'trace': str(e.__traceback__.tb_frame.f_globals.get('__file__')),
                'line': e.__traceback__.tb_lineno
            })
        }
