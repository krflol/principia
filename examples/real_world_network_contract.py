# -*- coding: utf-8 -*-
"""
real_world_network_contract.py: A practical, real-world example of a
behavioral contract for a network client.
"""

import sys
import requests
sys.path.append('..')
from src.principia import principia

# --- 1. Define the Behavioral Check Function ---

def is_well_behaved_http_client(client):
    """
    This behavioral check verifies that an HTTP client object conforms to
    our application's specific requirements for safe network access.

    A "well-behaved" client must:
    1.  Have a `get` method.
    2.  Correctly handle a request timeout.
    3.  Return a dictionary on a successful (200) response.
    4.  Return `None` on a server error (e.g., 404, 500).
    5.  Not raise unexpected exceptions during these operations.
    """
    # Check for the required method
    if not hasattr(client, 'get'):
        return False

    try:
        # --- Test 1: Timeout Behavior ---
        # Use a public API that is known to be slow to test timeouts.
        try:
            client.get("https://httpbin.org/delay/5", timeout=0.1)
            # If it *doesn't* time out, it's not respecting the parameter.
            return False
        except requests.exceptions.Timeout:
            # This is the expected, correct behavior.
            pass
        except Exception:
            # Any other exception is a failure.
            return False

        # --- Test 2: Success Behavior ---
        # Use a reliable, fast public API for this test.
        success_response = client.get("https://httpbin.org/json")
        if not isinstance(success_response, dict):
            return False

        # --- Test 3: Error Handling Behavior ---
        error_response = client.get("https://httpbin.org/status/404")
        if error_response is not None:
            return False

    except Exception:
        # If any unexpected exception occurs during these tests, the client is not well-behaved.
        return False

    # If all checks pass, the client is considered well-behaved.
    return True


# --- 2. Define the Principia Contract ---

NETWORK_CLIENT_CONTRACT = principia.AssumptionContract(
    preconditions={
        'http_client': principia.AssuranceMatcher(None, name="HTTP Client")
            .must(principia.be_callable, principia.PreconditionError, "{name} must be a callable object or module.")
            .must(is_well_behaved_http_client, principia.InvalidArgumentError, "{name} does not meet the behavioral contract for a safe HTTP client.")
    },
    on_success="[Principia] ✅ HTTP client behavioral contract passed."
)


# --- 3. Define the Business Logic with the Contract ---

@principia.contract(NETWORK_CLIENT_CONTRACT)
def get_user_profile(user_id: int, http_client):
    """
    Fetches a user's profile from a remote API.

    This function is protected by a contract that guarantees the provided
    `http_client` is reliable, handles timeouts, and returns data in the
    expected format, preventing common network-related runtime errors.
    """
    print(f"--> Core Logic: Fetching profile for user {user_id}...")
    url = f"https://api.example.com/users/{user_id}" # A dummy URL
    
    # Thanks to the contract, we can call this with high confidence.
    # We'll use a mock client for this example to avoid real network calls in the main logic.
    profile_data = http_client.get(url)

    if profile_data:
        print(f"--> Core Logic: Successfully retrieved profile for {profile_data.get('name')}.")
        return profile_data
    else:
        print("--> Core Logic: Failed to retrieve profile.")
        return None


# --- 4. Define Compliant and Non-Compliant Clients ---

class CompliantHttpClient:
    """This client correctly implements the expected behavior."""
    def get(self, url, timeout=5):
        try:
            response = requests.get(url, timeout=timeout)
            if response.status_code == 200:
                return response.json()
            else:
                return None
        except requests.exceptions.Timeout:
            # Re-raising is important for the test to catch.
            raise
        except Exception:
            return None

class BadHttpClient_NoTimeout:
    """This client IGNORES the timeout parameter."""
    def get(self, url, timeout=5): # Ignores timeout
        response = requests.get(url) # No timeout passed to requests
        return response.json() if response.status_code == 200 else None

class BadHttpClient_ReturnsText:
    """This client returns raw text instead of a dictionary."""
    def get(self, url, timeout=5):
        try:
            response = requests.get(url, timeout=timeout)
            return response.text # Should be response.json()
        except requests.exceptions.Timeout:
            raise

# --- 5. Execute and Observe ---

if __name__ == "__main__":
    # We need to mock the final call inside get_user_profile to avoid hitting a fake URL.
    # The contract check, however, uses real URLs to test behavior.
    class MockCompliantClient(CompliantHttpClient):
        def get(self, url, timeout=5):
            if "api.example.com" in url:
                return {"id": 123, "name": "Alice"}
            return super().get(url, timeout)

    print("--- 1. Testing with a well-behaved (compliant) HTTP client ---")
    try:
        get_user_profile(123, http_client=MockCompliantClient())
    except principia.PrincipiaError as e:
        print(f"--> This should not happen. Caught error: {e}")

    print("\n--- 2. Testing with a client that ignores timeouts ---")
    try:
        get_user_profile(123, http_client=BadHttpClient_NoTimeout())
    except principia.InvalidArgumentError as e:
        print(f"--> Caught expected error: {e}")

    print("\n--- 3. Testing with a client that returns the wrong data format ---")
    try:
        get_user_profile(123, http_client=BadHttpClient_ReturnsText())
    except principia.InvalidArgumentError as e:
        print(f"--> Caught expected error: {e}")
