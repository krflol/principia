# Core Philosophy: The Assumption-Assertion-Consequence Model

The design of Principia is centered around a simple but powerful idea: **every bug is the result of a violated assumption**. When your code receives data in an unexpected format or a dependency behaves in an unexpected way, errors occur.

Principia's goal is to eliminate these errors by making every assumption explicit and verifiable. This is achieved through the **Assumption-Assertion-Consequence** model.

### 1. Assumption (The "What Ifs")

Before you write a function, you make implicit assumptions. You assume:
*   An argument `user_id` will be a positive integer.
*   A `file_path` will point to a file that actually exists.
*   A `notifier` function will not crash when you call it.

Principia requires you to state these assumptions explicitly.

### 2. Assertion (The "Make Sures")

An assertion is the mechanism by which an assumption is verified. In Principia, this is done using an `AssumptionContract`.

You use the rich semantic layer (`be_a`, `be_in_range`, `is_safe_notifier`) to build a chain of checks that formally assert your assumptions.

### 3. Consequence (The "Or Elses")

If an assertion fails, there must be a clear and immediate consequence. Instead of letting the invalid data or behavior propagate through your system, Principia raises a specific, informative exception.

*   `InvalidArgumentError`: An argument's value is invalid.
*   `PreconditionError`: An argument's type is wrong.
*   `IllegalStateError`: A function is called at the wrong time or returns an invalid result.

By formalizing this model, Principia helps you build code that is not only more robust but also self-documenting. Your contracts become a clear, executable specification of your function's requirements.
