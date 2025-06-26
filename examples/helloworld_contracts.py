# helloworld_contracts.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from io import TextIOBase
from principia import (
    AssumptionContract, AssuranceMatcher, ConfigurationError, PreconditionError,
    conform_to, be_unmodified_builtin
)

import builtins

# Contract 1: Guarantees the integrity of the built-in functions we rely on.
# This protects against global namespace pollution (e.g., `print = 42`).
BUILTIN_INTEGRITY_CONTRACT = AssumptionContract(
    environment=AssuranceMatcher(None, name="Built-in Namespace")
        .must(lambda _: hasattr(builtins, 'print'), PreconditionError, "Built-in 'print' function not found.")
        .must(lambda _: be_unmodified_builtin("print")(getattr(builtins, 'print')), PreconditionError, "'print' name has been dangerously shadowed.")
)

# Contract 2: Guarantees the environment is set up for visible terminal output.
TERMINAL_OUTPUT_CONTRACT = AssumptionContract(
    environment=AssuranceMatcher(sys.stdout, name="Output Stream")
        .must(conform_to(TextIOBase), ConfigurationError, "{name} does not behave like a text stream.")
        .must(lambda s: s.isatty(), ConfigurationError, "{name} is not an interactive terminal.")
        .must(lambda s: not s.closed, ConfigurationError, "{name} is closed."),
    on_success="[Principia] ✅ All environment and dependency contracts passed."
)
