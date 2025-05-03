from bunq.sdk.context.api_context import ApiContext
from bunq.sdk.context.bunq_context import BunqContext
from bunq import ApiEnvironmentType
import os

from dotenv import load_dotenv

load_dotenv()

SANDBOX_API_KEY = os.getenv("SANDBOX_API_KEY")
if SANDBOX_API_KEY is None:
    raise ValueError("SANDBOX_API_KEY environment variable not set")

ENVIRONMENT = os.getenv("ENVIRONMENT", "sandbox")  # valid values: sandbox, production

environment_type = ApiEnvironmentType.SANDBOX
if ENVIRONMENT == "production":
    environment_type = ApiEnvironmentType.PRODUCTION


# Create an API context for sandbox (easiest approach)
api_context = ApiContext.create(
    environment_type, SANDBOX_API_KEY, "My Device Description"
)

# Save the API context to a file for future use
api_context.save("bunq_api_context.conf")
