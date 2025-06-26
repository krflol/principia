# data_science_contracts.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pandas as pd
from statsmodels.tsa.stattools import adfuller
from typing import Callable, List
from principia import AssumptionContract, AssuranceMatcher, InvalidArgumentError, be_a

# --- Custom Semantic Checks for Data Science ---
def be_stationary(p_value_thresh: float = 0.05) -> Callable[[pd.Series], bool]:
    """Ensures a time-series is stationary via ADF test."""
    return lambda series: adfuller(series)[1] < p_value_thresh

def have_columns(cols: List[str]) -> Callable[[pd.DataFrame], bool]:
    """Ensures a DataFrame contains required columns."""
    return lambda df: all(c in df.columns for c in cols)

# --- The Contract ---
STATISTICAL_PROPERTIES_CONTRACT = AssumptionContract(
    preconditions={
        'raw_data': AssuranceMatcher(None, name="Time-Series Data")
            .must(be_a(pd.DataFrame), InvalidArgumentError, "{name} must be a pandas DataFrame.")
            .must(have_columns(['timestamp', 'sales']), InvalidArgumentError, "{name} is missing required columns.")
            .must(lambda df: be_stationary()(df['sales']), InvalidArgumentError, "Target variable 'sales' is not stationary.")
    },
    on_success="[Principia] ✅ Data statistical properties validated."
)
