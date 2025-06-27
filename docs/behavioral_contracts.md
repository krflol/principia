# Advanced Guide: Behavioral Contracts

The true power of Principia is realized when you move beyond simple data validation to **behavioral validation**. A behavioral contract verifies not just the *state* of a dependency, but its *behavior* when called.

This is critical for ensuring the reliability of complex systems where functions depend on other services, clients, or functions.

### The Problem: Unreliable Dependencies

Imagine a function that needs to fetch data from a network. Your function assumes the network client will:
*   Time out correctly if the network is slow.
*   Return data in a specific format (e.g., a dictionary).
*   Handle server errors gracefully instead of crashing.

A simple type check (`isinstance(client, HttpClient)`) tells you nothing about these crucial behaviors.

### The Solution: Behavioral Assertion

With Principia, you can write a custom check function that asserts the behavior of the dependency.

#### Step 1: Write a Behavioral Check Function

This is a regular Python function that takes the dependency as an argument and returns `True` only if it behaves as expected. It should test the dependency by calling it with controlled inputs.

```python
import requests

def is_well_behaved_http_client(client):
    """
    Asserts that a client handles timeouts, success, and errors correctly.
    """
    try:
        # Test 1: Does it time out?
        client.get("https://httpbin.org/delay/5", timeout=0.1)
        return False # Should have timed out
    except requests.exceptions.Timeout:
        pass # Correct behavior
    except Exception:
        return False # Wrong exception

    # Test 2: Does it return a dict on success?
    if not isinstance(client.get("https://httpbin.org/json"), dict):
        return False

    # Test 3: Does it return None on error?
    if client.get("https://httpbin.org/status/404") is not None:
        return False
        
    return True # All behavioral checks passed
```

#### Step 2: Use the Check in a Contract

Now, use this function directly in your `AssumptionContract`.

```python
from src.principia import principia

NETWORK_CLIENT_CONTRACT = principia.AssumptionContract(
    preconditions={
        'http_client': principia.AssuranceMatcher(None, name="HTTP Client")
            .must(principia.be_callable, principia.PreconditionError, "{name} must be a callable object.")
            .must(is_well_behaved_http_client, principia.InvalidArgumentError, "{name} does not meet the behavioral contract for a safe HTTP client.")
    }
)
```

#### Step 3: Apply the Contract

```python
@principia.contract(NETWORK_CLIENT_CONTRACT)
def get_user_profile(user_id: int, http_client):
    # ...
```

By applying this contract, you guarantee that `get_user_profile` will never be executed with a misbehaving HTTP client. You have successfully moved the responsibility of handling a complex dependency from runtime error handling to a single, clear, and verifiable assertion.
