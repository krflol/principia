# API Reference

This page provides a reference for the main components of the Principia library.

## Core Components

### `principia.contract(*contracts)`
A function decorator that applies one or more `AssumptionContract` objects to a function.

### `principia.AssumptionContract`
A dataclass that holds the assertions for a function.

**Parameters:**
*   `preconditions` (dict): A dictionary mapping argument names to `AssuranceMatcher` objects.
*   `postcondition` (AssuranceMatcher): An `AssuranceMatcher` for the function's return value.
*   `environment` (AssuranceMatcher): An `AssuranceMatcher` for checking the environment (e.g., dependencies, files).
*   `on_success` (str or callable): A message to print or a function to call if all checks pass.

### `principia.AssuranceMatcher`
A class for building a chain of assertions.

**Methods:**
*   `must(success_condition, then_raise, message)`: Adds a check that must pass.
*   `on(failure_condition, then_raise, message)`: Adds a check that must fail.

## Semantic Layer (Check Functions)

These functions are designed to be used as the `success_condition` in a `.must()` call.

### Type and Structure
*   `be_a(expected_type)`
*   `be_callable()`
*   `conform_to(protocol_class)`
*   `have_attribute(attr_name)`

### Identity
*   `be_the_same_as(identity)`
*   `be_unmodified_builtin(name_str)`

### Numeric
*   `be_greater_than(limit)`
*   `be_in_range(lower_bound, upper_bound)`

### String
*   `match_pattern(pattern)`

### Collection
*   `not_be_empty()`
*   `have_length(expected_len)`

### Filesystem
*   `be_existing_file()`

## Custom Exceptions

*   `PrincipiaError`: Base class for all library exceptions.
*   `PreconditionError`: For fundamental failures of type or protocol.
*   `InvalidArgumentError`: For arguments with incorrect values.
*   `IllegalStateError`: For operations in an improper state.
*   `ConfigurationError`: For environment-related failures.
