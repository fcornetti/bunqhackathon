from bunq.sdk.context.api_context import ApiContext
from bunq.sdk.context.bunq_context import BunqContext
from bunq import ApiEnvironmentType

# Create an API context for sandbox (easiest approach)
api_context = ApiContext.create(
    ApiEnvironmentType.SANDBOX,
    "sandbox_be8e4c04575b4b3d08d02e9784ff06385cb736e334b928728c48729d",
    "My Device Description"
)

# Save the API context to a file for future use
api_context.save("bunq_api_context.conf")