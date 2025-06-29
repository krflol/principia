# -*- coding: utf-8 -*-
"""
behavior_contracts.py: Demonstrating Behavioral Contracts with Principia.

This example shows how to use Principia to verify not just the state of data,
but the *behavior* of dependencies (like functions or objects) passed into
your code.
"""

from principia import AssumptionContract, AssuranceMatcher, contract, InvalidArgumentError, PreconditionError, be_callable

# --- 1. Define Behavioral Check Functions ---

def is_safe_notifier(notifier_func):
    """
    A behavioral check. It verifies that a given notifier function:
    1. Is callable.
    2. Can be executed with a sample message without raising an exception.
    3. Returns a specific success value (e.g., True).

    This is far more powerful than a simple `isinstance(notifier_func, Callable)`.
    It tests the *contract* of the dependency's behavior.
    """
    if not callable(notifier_func):
        return False
    try:
        # Test the notifier with a sample call.
        result = notifier_func("Test notification: System is stable.")
        # We assume the notifier should return True on success.
        return result is True
    except Exception:
        # If the notifier raises any exception, it's considered unsafe.
        return False

# --- 2. Define the Principia Contract ---

# This contract ensures that any function passed as the 'notifier' argument
# adheres to the behavior defined in `is_safe_notifier`.
BEHAVIORAL_CONTRACT = AssumptionContract(
    preconditions={
        'notifier': AssuranceMatcher(None, name="Notifier Function")
            .must(be_callable(), PreconditionError, "{name} must be a callable function.")
            .must(is_safe_notifier, InvalidArgumentError, "{name} failed its safety check. It must not raise exceptions and must return True.")
    },
    on_success="[Principia] ✅ Behavioral contract for notifier passed."
)


# --- 3. Define the Business Logic with the Contract ---

@contract(BEHAVIORAL_CONTRACT)
def process_critical_data(data: dict, notifier):
    """
    Processes critical data and notifies a system of the outcome.
    This function is protected by a behavioral contract that ensures the
    notifier it is given is safe to use.
    """
    print(f"--> Core Logic: Processing data: {data}")
    # ... core data processing logic ...
    print("--> Core Logic: Data processing complete.")
    
    # Because of the contract, we can be confident this call is safe.
    notifier("Data processing successful.")
    return "OK"


# --- 4. Define Compliant and Non-Compliant Dependencies ---

def good_notifier(message: str):
    """A well-behaved notifier that meets the contract's expectations."""
    print(f"[Good Notifier]: {message}")
    return True

def bad_notifier_crashes(message: str):
    """A poorly-behaved notifier that raises an exception."""
    print(f"[Bad Notifier]: {message}")
    raise RuntimeError("Failed to connect to notification service!")

def bad_notifier_returns_wrong_value(message: str):
    """A poorly-behaved notifier that doesn't return the expected value."""
    print(f"[Bad Notifier]: {message}")
    return "Sent" # Should return True


# --- 5. Execute and Observe ---

if __name__ == "__main__":
    print("--- Testing with a well-behaved (compliant) notifier ---")
    process_critical_data({"value": 42}, notifier=good_notifier)

    print("\n--- Demonstrating contract failure (for documentation) ---")
    print("If you were to run `process_critical_data` with a misbehaving notifier,")
    print("Principia would raise an `InvalidArgumentError` before the core logic runs.")
    # Example of what would fail:
    # process_critical_data({"value": 99}, notifier=bad_notifier_crashes)
