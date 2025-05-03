from typing import Optional, Union
from bunq.sdk.context.api_context import ApiContext
from bunq.sdk.context.bunq_context import BunqContext
from bunq.sdk.model.generated.endpoint import PaymentApiObject
from bunq.sdk.model.generated.object_ import AmountObject, PointerObject
from bunq.sdk.model.generated.endpoint import RequestInquiryApiObject
from bunq.sdk.model.generated.endpoint import MonetaryAccountBankApiObject
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
api_context = ApiContext.restore("bunq_api_context.conf")
BunqContext.load_api_context(api_context)


@app.get("/")
def read_root():
    # Access the user context
    user_context = BunqContext.user_context()

    # Get the user ID
    user_id = user_context.user_id

    # Get the primary monetary account
    primary_account = user_context.primary_monetary_account.id_

    results = {"user_id": user_id, "primary_account": primary_account}
    return results


class PaymentRequest(BaseModel):
    amount: str
    counterparty_alias: str
    description: Optional[str] = None


@app.post("/payment")
def create_payment(payment: PaymentRequest):
    """
    Create a payment to another user.
    """
    print(f"payment: {payment}")
    try:
        payment_id = PaymentApiObject.create(
            amount=AmountObject(payment.amount, "EUR"),
            # TODO: change counterparty_alias
            counterparty_alias=PointerObject("EMAIL", "fcornetti+trainee@bunq.com"),
            description=payment.description or "",
        ).value
        print(f"payment_id {payment_id}")
        return {"payment_id": payment_id}
    except Exception as e:
        return {"error": str(e)}


@app.post("/savings/create")
def create_savings_account():
    """
    Create a new monetary account
    """
    try:
        account_id = MonetaryAccountBankApiObject.create(
            currency="EUR",
            description="Savings Account"
        ).value
        print(f"account_id {account_id}")
        return {"account_id": account_id}
    except Exception as e:
        return {"error": str(e)}

@app.post("/savings/move")
def move_to_savings():
    """
    Move money to a savings account
    """
    try:
        payment_id = PaymentApiObject.create(
        amount=AmountObject("5.00", "EUR"),
        counterparty_alias={
            "type": "IBAN",
            "value": "NL63BUNQ2090666315",
            "name": "batch payment n2"
        },
        description="Transfer to savings"
        ).value
        print(f"payment_id {payment_id}")
        return {"payment_id": payment_id}
    except Exception as e:
        return {"error": str(e)}

@app.post("/savings/plan")
def calculate_savings_plan():
    """
    Calculate savings plan
    """
