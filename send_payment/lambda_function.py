import json
import urllib.request

url = "https://8e09-31-207-9-142.ngrok-free.app/payment"


def get_named_parameter(event, name, default=None):
    """
    Get a parameter from the lambda event
    """
    return next(
        (item["value"] for item in event.get("parameters", []) if item["name"] == name),
        default,
    )


def send_payment(amount, counterparty_alias, description):
    """
    Send a payment to another user via a FastAPI payment endpoint

    Args:
        amount (str): The amount of money to send (e.g., "10.00")
        counterparty_alias (str): The alias (typically an email) of the payment recipient
        description (str): A short description or reference for the payment

    Returns:
        dict: A dictionary containing the HTTP status code and response body from the API.
              If an error occurs, it returns a 500 status code with the error message.
    """

    payload = {
        "amount": amount,
        "counterparty_alias": counterparty_alias,
        "description": description,
    }

    headers = {"Content-Type": "application/json"}

    try:
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers=headers, method="POST")
        with urllib.request.urlopen(req) as response:
            response_body = response.read().decode("utf-8")
            return {"statusCode": response.getcode(), "body": response_body}
    except Exception as e:
        return {"statusCode": 500, "body": f"Error: {str(e)}"}


def lambda_handler(event, context):
    actionGroup = event.get("actionGroup", "")
    function = event.get("function", "")
    parameters = event.get("parameters", [])

    if function == "send_payment":
        amount = get_named_parameter(event, "amount")
        counterparty_alias = get_named_parameter(event, "counterparty_alias")
        description = get_named_parameter(event, "description")

        if amount and counterparty_alias:
            response = send_payment(amount, counterparty_alias, description or "")
            responseBody = {"TEXT": {"body": json.dumps(response.get("body"))}}
        else:
            responseBody = {"TEXT": {"body": "Missing required parameters"}}
    else:
        responseBody = {"TEXT": {"body": "Invalid function"}}

    action_response = {
        "actionGroup": actionGroup,
        "function": function,
        "functionResponse": {"responseBody": responseBody},
    }

    function_response = {
        "response": action_response,
        "messageVersion": event["messageVersion"],
    }
    print("Response: {}".format(function_response))

    return function_response
