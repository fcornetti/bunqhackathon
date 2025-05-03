from bunq.sdk.context.api_context import ApiContext
from bunq.sdk.context.bunq_context import BunqContext
from bunq.sdk.model.generated.endpoint import PaymentApiObject
from bunq.sdk.model.generated.object_ import AmountObject, PointerObject
from bunq.sdk.model.generated.endpoint import RequestInquiryApiObject
from bunq.sdk.model.generated.endpoint import MonetaryAccountBankApiObject

api_context = ApiContext.restore("bunq_api_context.conf")

BunqContext.load_api_context(api_context)

# Access the user context
user_context = BunqContext.user_context()

# Get the user ID
user_id = user_context.user_id

# Get the primary monetary account
primary_account = user_context.primary_monetary_account.id_

print(user_id, primary_account)

# Make a payment to another user
payment_id = PaymentApiObject.create(
    amount=AmountObject("1.00", "EUR"),
    counterparty_alias=PointerObject("EMAIL", "fcornetti+trainee@bunq.com"),
    description="Lunch payment"
).value

print(payment_id)

# Create a payment request
request_id = RequestInquiryApiObject.create(
    AmountObject("10.00", "EUR"),
    {
        "type": "EMAIL",
        "value": "sugardaddy@bunq.com",
        "name": "batch payment n2"
    },
    "Please pay for dinner",
    allow_bunqme=False
).value

print(request_id)

# Create a new monetary account
'''account_id = MonetaryAccountBankApiObject.create(
    currency="EUR",
    description="Savings Account"
).value

print(account_id)'''

# Make a payment to another account of the same user
payment_id = PaymentApiObject.create(
    amount=AmountObject("5.00", "EUR"),
    counterparty_alias={
        "type": "IBAN",
        "value": "NL63BUNQ2090666315",
        "name": "batch payment n2"
    },
    description="Transfer to savings"
).value

print(payment_id)