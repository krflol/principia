# your_app.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from principia import (
    AssumptionContract, AssuranceMatcher, contract, PreconditionError,
    InvalidArgumentError, be_a, be_in_range, not_be_empty
)

# 1. Define the "contract" for what a valid user is.
USER_CONTRACT = AssumptionContract(
    preconditions={
        'username': AssuranceMatcher(None, name="Username")
            .must(be_a(str), PreconditionError, "{name} must be a string.")
            .must(not_be_empty(), InvalidArgumentError, "{name} cannot be empty."),

        'age': AssuranceMatcher(None, name="Age")
            .must(be_a(int), PreconditionError, "{name} must be an integer.")
            .must(be_in_range(18, 120), InvalidArgumentError, "{name} must be between 18 and 120.")
    },
    on_success="[Principia] ✅ User contract validated."
)

# 2. Apply the contract to your function.
@contract(USER_CONTRACT)
def create_user(username: str, age: int):
    """
    This function's logic is now protected. It will only execute if the
    username and age are valid according to the contract.
    """
    print(f"--> Core Logic: Creating user '{username}' (age {age}).")

# 3. Run it and observe!
if __name__ == "__main__":
    # --- The Happy Path ---
    print("--- Testing with valid data ---")
    create_user(username="Alice", age=30)

    # --- The Failure Path ---
    print("\n--- Testing with invalid data ---")
    try:
        create_user(username="Bob", age=17)
    except InvalidArgumentError as e:
        print(f"Caught expected error: {e}")
