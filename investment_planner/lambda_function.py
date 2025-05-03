import json
import urllib.request


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
    Create a new monetary account via e endpoint
    """


def move_to_savings():
    """
    Move money to savings account via e endpoint
    """

def calculate_savings_plan():
    """
    Calculate savings plan via e endpoint
    """


def lambda_handler(event, context):
    actionGroup = event.get("actionGroup", "")
    function = event.get("function", "")
    parameters = event.get("parameters", [])


    # action_response = {
    #     "actionGroup": actionGroup,
    #     "function": function,
    #     "functionResponse": {"responseBody": responseBody},
    # }

    # function_response = {
    #     "response": action_response,
    #     "messageVersion": event["messageVersion"],
    # }
    # print("Response: {}".format(function_response))

    # return function_response
