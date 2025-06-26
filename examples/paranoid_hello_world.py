# paranoid_hello_world.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from principia import contract
from helloworld_contracts import BUILTIN_INTEGRITY_CONTRACT, TERMINAL_OUTPUT_CONTRACT

@contract(BUILTIN_INTEGRITY_CONTRACT, TERMINAL_OUTPUT_CONTRACT)
def say_hello():
    """
    Prints "hello world" only after its contracts have verified the
    integrity of the 'print' function and the terminal environment.
    """
    print("--> Core Logic: All assumptions met. Performing action...")
    str_to_print = "hello world"
    print(str_to_print)

# --- Run it ---
try:
    say_hello()
except Exception as e:
    # This block will run if you redirect output to a file,
    # or if you maliciously overwrite the 'print' function.
    print(f"Principia contract failed as designed: {e}")
