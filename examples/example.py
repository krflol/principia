import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from principia import (AssumptionContract,
                       AssuranceMatcher,
                       be_a,
                       contract,
                       InvalidArgumentError,
                       be_greater_than,
                       be_in_range,
                       PreconditionError)



#ensure that user age is an int and over 18
age_conditions = {
    "user_age":AssuranceMatcher(None, name = "Age")
    .must(be_a(int), InvalidArgumentError,message= "{name} must be an integer")
    .must(be_greater_than(18),PreconditionError, message="{name} must be greater 18")
}

AGE_CONTRACT = AssumptionContract(preconditions= age_conditions, on_success= "LEGAL... ARGUMENTS")


@contract(AGE_CONTRACT)
def test_age(user_age:int):
    print(f"--> Core Logic: Fetching data for user...AGE: {user_age}...")
    return {"age": user_age, "name": "Alice"}

test = test_age(19)
