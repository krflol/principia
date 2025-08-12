# examples/async_example.py
import asyncio
from principia import AssumptionContract, AssuranceMatcher, contract, InvalidArgumentError, be_a

# --- 1. Define a custom ASYNCHRONOUS validation check ---
# This check simulates a network call to validate a resource.
async def is_valid_remote_resource(url: str) -> bool:
    """
    An asynchronous check that simulates validating a URL by making a
    fake network call. It returns True if the URL is "valid".
    """
    print(f"   [Async Check] Verifying resource '{url}'...")
    await asyncio.sleep(0.01)  # Simulate network latency
    is_valid = url == "https://example.com/valid_resource"
    print(f"   [Async Check] Verification complete. Valid: {is_valid}")
    return is_valid

# --- 2. Define a contract that USES the async check ---
# This contract ensures that a URL is a string and that it points to a
# valid remote resource, according to our async check.
ASYNC_URL_CONTRACT = AssumptionContract(
    preconditions={
        'url': AssuranceMatcher(None, name="Resource URL")
            .must(be_a(str), InvalidArgumentError, "{name} must be a string.")
            .must(is_valid_remote_resource, InvalidArgumentError, "{name} is not a valid remote resource.")
    },
    on_success="[Principia] ✅ Async URL contract passed."
)

# --- 3. Apply the contract to an ASYNCHRONOUS function ---
@contract(ASYNC_URL_CONTRACT)
async def fetch_remote_data(url: str):
    """
    An async function protected by a contract with an async check.
    It will only execute if the URL is valid.
    """
    print("--> Core Logic: Fetching data from URL...")
    await asyncio.sleep(0.02)  # Simulate the core work
    print("--> Core Logic: Data fetched successfully.")
    return {"source": url, "data": "some important data"}

# --- 4. Execute and observe ---
async def main():
    """Main function to run the async examples."""
    print("--- Testing Principia with a VALID async call ---")
    try:
        result = await fetch_remote_data("https://example.com/valid_resource")
        print(f"--> Success: Got result: {result}")
    except InvalidArgumentError as e:
        print(f"--> This should not happen. Caught error: {e}")

    print("\n" + "-"*50)

    print("\n--- Testing Principia with an INVALID async call ---")
    try:
        await fetch_remote_data("https://example.com/invalid_resource")
    except InvalidArgumentError as e:
        print(f"--> Caught expected error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
