import os
from python_semrush.semrush import SemrushClient

# Load the API key from environment variable
api_key = os.getenv("SEMRUSH_API")

if not api_key:
    raise ValueError("SEMRUSH_API environment variable is not set!")

# Initialize Semrush Client
client = SemrushClient(key=api_key)

# Perform an API request
result = client.domain_ranks(domain="mainiti.org")

# Print the result
print(result)

print('fdsasfdsaf')
