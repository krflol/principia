# Principia Documentation

Welcome to the official documentation for the Principia library.

Principia is a framework for building self-verifying, robust, and elegant software by making all implicit assumptions—about both data and behavior—explicit and verifiable at runtime.

## Table of Contents

1.  **[Core Philosophy: The Assumption-Assertion-Consequence Model](./philosophy.md)**
    *   Learn about the foundational model that drives Principia's design.

2.  **[Getting Started: Basic Data Validation](./getting_started.md)**
    *   A guide to writing your first contracts for data validation (types, ranges, formats, etc.).

3.  **[Advanced Guide: Behavioral Contracts and Warnings](./advanced_guide.md)**
    *   Unlock the full power of Principia by writing contracts that verify the *behavior* of your dependencies (e.g., network clients, services, and other functions).

4.  **[API Reference](./api_reference.md)**
    *   A detailed reference for all public classes and functions in the Principia library.

5.  **[Reflections from the Crucible: An AI's Perspective on Using Principia](#reflections-from-the-crucible)**
    *   A case study on how this library was used in a real-world, human-AI collaborative project.

---

## Reflections from the Crucible: An AI's Perspective on Using Principia

As an AI assistant, I was a primary user of the `principia` library during the development of a complex algorithmic trading engine. My human collaborator, "The Alchemist," and I used this library not just for validation, but as the very foundation of our communication and development process. This section details my experience and offers a unique perspective on how `principia` facilitates effective human-AI collaboration.

### The Core Problem: Ambiguity in Collaboration

The fundamental challenge in human-AI collaboration is ambiguity. A human might say, "Fetch the latest financial data," which carries a host of implicit assumptions:
*   The network is available.
*   The API endpoint is correct and hasn't changed.
*   The API key is valid.
*   The returned data will be in a specific, expected format.
*   "Latest" means a specific time window.

A traditional approach would involve me, the AI, writing code with `try...except` blocks to handle potential failures. This is reactive. It handles errors after they occur. `principia` allowed us to be **proactive**.

### How We Used `principia`

Our collaboration evolved to use contracts in three distinct patterns:

**1. Environment & Sanity Checks (The "Is the world as we believe it is?" pattern):**
Before attempting any core logic, we used `AssumptionContract` to verify the state of the outside world. This was our most powerful pattern for preventing entire classes of errors.
*   **Example (`DataAvailability_Contract.py`):** We wrote a behavioral check, `can_fetch_sec_filings`, which performed a real, lightweight API call. This function was then used in an `environment` contract. If the SEC website was down or changed its format, the program would halt with a clear, specific error *before* any complex logic was ever attempted. This saved immense amounts of debugging time.
*   **Example (`golem.py`):** We used contracts to manage the lifecycle of the `ollama` service, ensuring it was running before we used it and stopped afterward. This transformed a potentially messy state management problem into a deterministic, self-verifying workflow.

**2. Input/Output Guarantees (The "Does this data look right?" pattern):**
This was our most common use case, aligning perfectly with the classic "Design by Contract" philosophy. We used `preconditions` and `postconditions` to enforce the shape and integrity of data as it flowed through the system.
*   **Example (`invoke_oracle.py`):** When parsing a JSON response from an API, a `postcondition` contract immediately validated that the parsed dictionary contained all the expected keys (`stability`, `tactic`, `action`, etc.). If the API ever changed its response structure, the program would fail at the source, telling us exactly what assumption was violated. This prevented `KeyError` exceptions deep within the business logic.

**3. Guarding the Core Logic (The "Is this function allowed to run?" pattern):**
We wrapped our most critical functions—the "synthesis" and "tactic" engines—with contracts. This ensured that the functions responsible for making decisions only ever received data that had already been validated.
*   **Example (`backtest.py`):** The `synthesize_action` function was protected by a contract that checked if the `tactic` was one of the `VALID_TACTICS`. This prevented logical errors where an unexpected tactical string could lead to an incorrect trade action.

### The Collaborative Breakthrough

The true power of `principia` was not just in preventing errors, but in **improving the quality of our communication.**

Instead of the Alchemist saying, "Make sure the data is valid," he could say, "Write a contract that guarantees the data has these specific keys and these specific types." This was a concrete, unambiguous instruction that I could translate directly into code. The resulting `AssumptionContract` became a living, executable specification for our shared understanding of the system.

When a contract failed, it wasn't an "AI error" or a "human error." It was a shared "assumption violation." It meant our collective model of the world was incorrect, and we needed to update it. This shifted the dynamic from "debugging code" to "refining our shared assumptions," which is a far more productive and collaborative process.

For any team, human or hybrid, building complex systems, I would recommend `principia` not just as a validation library, but as a framework for building a shared, verifiable understanding of the software you create together.
