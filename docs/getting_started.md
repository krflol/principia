# Getting Started: Basic Data Validation

Data validation is the most common use case for Principia and the best place to start. A data validation contract ensures that a function receives arguments of the correct type, format, and value.

### Step 1: Define an `AssumptionContract`

First, import `principia` and create an `AssumptionContract`. This object will hold all the rules for your function.

```python
from src.principia import principia

ID_CONTRACT = principia.AssumptionContract(...)
```

### Step 2: Define `preconditions`

The `preconditions` are a dictionary where each key is an argument name and each value is an `AssuranceMatcher` that defines the rules for that argument.

You can chain checks using the `.must()` method. Each `must()` call takes three arguments:
1.  A **semantic check** (e.g., `principia.be_a(int)`).
2.  A **consequence** (e.g., `principia.InvalidArgumentError`).
3.  An **error message** template.

```python
ID_CONTRACT = principia.AssumptionContract(
    preconditions={
        'user_id': principia.AssuranceMatcher(None, name="User ID")
            .must(principia.be_a(int), principia.InvalidArgumentError, "{name} must be an integer.")
            .must(principia.be_greater_than(0), principia.InvalidArgumentError, "{name} must be a positive integer."),
        
        'email': principia.AssuranceMatcher(None, name="Email")
            .must(principia.be_a(str), principia.InvalidArgumentError, "{name} must be a string.")
            .must(principia.match_pattern(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"),
                  principia.InvalidArgumentError, "{name} must be a valid email format.")
    }
)
```

### Step 3: Apply the Contract

Use the `@principia.contract()` decorator to apply your contract to a function.

```python
@principia.contract(ID_CONTRACT)
def create_user(user_id: int, email: str):
    print(f"Creating user {user_id} with email {email}...")
    # Your logic here
```

Now, if you try to call `create_user` with invalid data, Principia will immediately raise the specific exception you defined, preventing the error from ever reaching your core logic.

```python
# This will raise InvalidArgumentError: "User ID must be a positive integer."
create_user(user_id=-1, email="test@example.com") 
```
