# train.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pandas as pd
import numpy as np
from principia import contract
from data_science_contracts import STATISTICAL_PROPERTIES_CONTRACT

@contract(STATISTICAL_PROPERTIES_CONTRACT)
def train_forecasting_model(raw_data: pd.DataFrame):
    """
    This expensive training function is protected by a Data Contract.
    It will refuse to run on data that isn't statistically sound.
    """
    print("--> Core Logic: Data contract satisfied. Starting training run...")
    # ... your expensive model.fit() logic would go here ...
    print("--> Core Logic: Training complete.")

# --- Run it ---
# Create a "good" stationary dataset and a "bad" trending one.
np.random.seed(42)
good_data = pd.DataFrame({
    'timestamp': pd.to_datetime(pd.date_range('2025-01-01', periods=100)),
    'sales': 100 + np.random.randn(100)
})
bad_data = pd.DataFrame({
    'timestamp': pd.to_datetime(pd.date_range('2025-01-01', periods=100)),
    'sales': 100 + np.random.randn(100).cumsum()
})

try:
    print("--- Testing with valid, stationary data ---")
    train_forecasting_model(good_data)

    print("\n--- Testing with invalid, non-stationary data ---")
    train_forecasting_model(bad_data)
except Exception as e:
    print(f"\n--> FAILED AS EXPECTED! The contract prevented a wasted training run.")
    print(f"    Reason: {e}")
