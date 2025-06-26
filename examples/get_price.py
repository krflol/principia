# get_price.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import requests
from principia import contract
from network_contracts import NETWORK_ENVIRONMENT_CONTRACT, API_POSTCONDITION_CONTRACT

@contract(NETWORK_ENVIRONMENT_CONTRACT, API_POSTCONDITION_CONTRACT)
def fetch_bitcoin_price() -> requests.Response:
    """
    Performs an API call sandboxed by Principia contracts. The rest of your
    application can trust the Response object this function returns.
    """
    print("--> Core Logic: All contracts satisfied. Making API call...")
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    return requests.get(url, timeout=5)

# --- Run it ---
try:
    response = fetch_bitcoin_price()
    price = response.json()["bitcoin"]["usd"]
    print(f"\n--> SUCCESS! Bitcoin price: ${price:,.2f}")
except Exception as e:
    print(f"\n--> FAILED AS EXPECTED! Reason: {e}")
