# network_contracts.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import socket
import json
import requests
from typing import Callable, Any
from principia import (
    AssumptionContract, AssuranceMatcher, ConfigurationError, PreconditionError,
    IllegalStateError, be_a
)

# --- Custom Semantic Checks for Networking ---
def be_online(check_host: str = "1.1.1.1", port: int = 53) -> Callable[[Any], bool]:
    """A coarse check for internet connectivity."""
    return lambda _: _is_online(check_host, port)

def be_a_resolvable_hostname() -> Callable[[str], bool]:
    """Ensures a hostname can be resolved by DNS."""
    return lambda hostname: _is_resolvable(hostname)

# --- The Contracts ---
NETWORK_ENVIRONMENT_CONTRACT = AssumptionContract(
    environment=AssuranceMatcher(None).must(be_online(), ConfigurationError, "No internet connectivity."),
    on_success="[Principia] ✅ Network connectivity verified."
)

API_POSTCONDITION_CONTRACT = AssumptionContract(
    postcondition=AssuranceMatcher(None, name="API Response")
        .must(lambda r: r.status_code == 200, IllegalStateError, "API did not return a 200 OK (got {value.status_code}).")
        .must(lambda r: "application/json" in r.headers.get('Content-Type', ''), IllegalStateError, "API response is not JSON.")
        .must(lambda r: "bitcoin" in r.json(), IllegalStateError, "API response JSON is missing required data."),
    on_success="[Principia] ✅ API response validated successfully."
)

# Helper functions for checks
def _is_online(host, port):
    try:
        socket.create_connection((host, port), timeout=1)
        return True
    except (socket.timeout, OSError):
        return False

def _is_resolvable(hostname):
    try:
        socket.gethostbyname(hostname)
        return True
    except socket.gaierror:
        return False
