import json
import urllib.request

base_url = "https://8e09-31-207-9-142.ngrok-free.app"


def get_named_parameter(event, name, default=None):
    """
    Get a parameter from the lambda event
    """
    return next(
        (item["value"] for item in event.get("parameters", []) if item["name"] == name),
        default,
    )


def create_savings_account():
    """
    Create a new monetary account via the savings API endpoint.

    Returns:
        dict: A dictionary containing the HTTP status code and response body from the API.
              If an error occurs, it returns a 500 status code with the error message.
    """

    url = f"{base_url}/savings/create"
    headers = {"Content-Type": "application/json"}
    try:
        req = urllib.request.Request(url, headers=headers, method="POST")
        with urllib.request.urlopen(req) as response:
            response_body = response.read().decode("utf-8")
            return {"statusCode": response.getcode(), "body": response_body}
    except Exception as e:
        return {"statusCode": 500, "body": f"Error: {str(e)}"}


def move_to_savings(amount):
    """
    Move money amount to a savings account.

    Args:
        amount (str): The amount of money to move to savings account (e.g., "5.00")

    Returns:
        dict: A dictionary containing the HTTP status code and response body from the API.
              If an error occurs, it returns a 500 status code with the error message.
    """
    url = f"{base_url}/savings/move"
    headers = {"Content-Type": "application/json"}
    payload = {"amount": amount}

    try:
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers=headers, method="POST")
        with urllib.request.urlopen(req) as response:
            response_body = response.read().decode("utf-8")
            return {"statusCode": response.getcode(), "body": response_body}
    except Exception as e:
        return {"statusCode": 500, "body": f"Error: {str(e)}"}


# def calculate_savings_plan():
#     """
#     Calculate savings plan via e endpoint
#     """


def lambda_handler(event, context):
    actionGroup = event.get("actionGroup", "")
    function = event.get("function", "")
    parameters = event.get("parameters", [])

    if function == "create_savings_account":
        response = create_savings_account()
        responseBody = {"TEXT": {"body": json.dumps(response.get("body"))}}

    elif function == "move_to_savings":
        amount = get_named_parameter(event, "amount")
        if not amount:
            responseBody = {"TEXT": {"body": "Amount is required"}}
        else:
            response = move_to_savings(amount)
            responseBody = {"TEXT": {"body": json.dumps(response.get("body"))}}

    # elif function == "calculate_savings_plan":
    #     response = calculate_savings_plan()
    #     responseBody = {"TEXT": {"body": json.dumps(response.get("body"))}}

    else:
        responseBody = {"TEXT": {"body": "Invalid function"}}

    action_response = {
        "actionGroup": actionGroup,
        "function": function,
        "functionResponse": {"responseBody": responseBody},
    }

    function_response = {
        "response": action_response,
        "messageVersion": event.get("messageVersion", "1.0"),
    }

    print("Response: {}".format(function_response))
    return function_response
