# Principia: The Art of Building Self-Verifying Software

A lightweight, powerful Python framework for building self-verifying, robust, and elegant software by making all implicit assumptions explicit and verifiable at runtime.

**Principia is a paradigm shift in writing reliable code.** It moves validation from cluttered `if/else` blocks and `try/except` statements into clean, declarative, and reusable "Assumption Contracts" that are applied directly to your functions. This allows you to build systems that are correct by construction, where errors are prevented, not just handled.

This library is designed to be a perfect co-pilot for both **human developers** and **AI code generators (LLMs)**, providing a semantic vocabulary that enforces correctness by construction.

-----

## The Philosophy

Runtime errors are rarely caused by faulty logic. They are caused by faulty *assumptions*—about input data, external APIs, or the state of an object. Principia makes these assumptions an explicit, executable part of your code. It separates the *what* (the validation intent) from the *how* (the business logic), leading to code that is not just safer, but dramatically cleaner and more readable.

## Key Features

  * **Declarative Contracts:** Use the elegant `@principia.contract` decorator to apply validation rules to functions, cleanly separating validation from business logic.
  * **Behavioral Contracts:** Go beyond simple state checking to verify the *behavior* of your objects (e.g., ensuring a function is idempotent or a data source is immutable).
  * **Rich Semantic Vocabulary:** A library of readable, pre-built checks like `be_a(int)`, `be_in_range(...)`, and `be_online()` that allow you to describe your intent in plain English.
  * **Extensible by Design:** Easily write your own custom semantic checks and contracts for your specific domain.

## Installation

```bash
pip install principia
```

## Showcase: Verifying Dependency Behavior

A common source of bugs is when a dependency, like a notification function, behaves in an unexpected way—it might crash, or return an unexpected value. Principia can prevent this by enforcing a **behavioral contract** that guarantees the dependency is safe to use before the core logic ever runs.

```python
# examples/behavior_contracts.py
from principia import AssumptionContract, AssuranceMatcher, contract, InvalidArgumentError, PreconditionError, be_callable

# --- A Custom Behavioral Check ---
def is_safe_notifier(notifier_func):
    """
    A behavioral check. It verifies that a given notifier function can be
    executed with a sample message without raising an exception and that it
    returns True on success.
    """
    if not callable(notifier_func):
        return False
    try:
        return notifier_func("Test notification: System is stable.") is True
    except Exception:
        return False

# --- The Contract ---
BEHAVIORAL_CONTRACT = AssumptionContract(
    preconditions={
        'notifier': AssuranceMatcher(None, name="Notifier Function")
            .must(be_callable(), PreconditionError, "{name} must be a callable function.")
            .must(is_safe_notifier, InvalidArgumentError, "{name} failed its safety check. It must not raise exceptions and must return True.")
    },
    on_success="[Principia] ✅ Behavioral contract for notifier passed."
)

# --- The Business Logic ---
@contract(BEHAVIORAL_CONTRACT)
def process_critical_data(data: dict, notifier):
    """
    This function is protected. It will only execute if the notifier
    is guaranteed to be safe to use.
    """
    print(f"--> Core Logic: Processing data: {data}")
    # ... core data processing logic ...
    print("--> Core Logic: Data processing complete.")
    notifier("Data processing successful.")
    return "OK"

# --- A Compliant Dependency ---
def good_notifier(message: str):
    """A well-behaved notifier that meets the contract's expectations."""
    print(f"[Good Notifier]: {message}")
    return True

# --- Execute the "Happy Path" ---
# This code runs without issue because good_notifier satisfies the contract.
# If we had passed a badly behaved notifier, Principia would have raised
# an InvalidArgumentError with a clear message, preventing the pipeline from
# ever running with unsafe code.
if __name__ == "__main__":
    process_critical_data({"value": 42}, notifier=good_notifier)
```

**Output:**

```
[Principia] ✅ Behavioral contract for notifier passed.
--> Core Logic: Processing data: {'value': 42}
--> Core Logic: Data processing complete.
[Good Notifier]: Data processing successful.
```

This example demonstrates the power of Principia. The `process_critical_data` function is clean of any validation logic. It can safely assume that any `notifier` it receives will behave correctly, because the contract has already verified it.

## Learn More

This is just a glimpse of what Principia can do. To learn more, explore the `/docs` directory for:

*   A full **API Reference**.
*   More **examples** and advanced use cases.
*   A deeper dive into the **philosophy** of Assertion/Error Driven Development.

## Contributing

Contributions are welcome! Please feel free to open an issue to discuss a new feature or submit a pull request.

## License

Distributed under the MIT License. See `LICENSE` for more information.
