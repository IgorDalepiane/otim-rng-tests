import py_random_source_code as py_random
from typing import List
import lcg  # Import the lcg.py module

# Mersenne Twister Implementation
class MersenneTwister:
    def __init__(self, seed=None):
        self.random_instance = py_random.Random(seed)
    
    def generate_sequence(self, n_samples: int) -> List[float]:
        return [self.random_instance.random() for _ in range(n_samples)]

def run_test_cases():
    # Parameters for the LCG algorithm
    m = 2**32
    a = 1664525
    c = 1013904223
    # seed = 1
    
    # Initialize the Mersenne Twister with the seed
    mt = MersenneTwister()
    
    test_cases = [
        {"n_numbers": 1000, "range": (1, 100)},
        {"n_numbers": 100000, "range": (1, 10000)},
        {"n_numbers": 1000000, "range": (1, 1000000)}
    ]
    
    for case in test_cases:
        # Generating LCG numbers using the rand_float_samples function from lcg.py
        lcg_raw_floats = lcg.rand_float_samples(case["n_numbers"], m, a, c)
        lcg_numbers = []
        for num in lcg_raw_floats:
            scaled_num = num * (case["range"][1] - case["range"][0])
            int_num = int(scaled_num) + case["range"][0]
            lcg_numbers.append(int_num)
        
        # Generating MT numbers using the generate_sequence function
        mt_raw_floats = mt.generate_sequence(case["n_numbers"])
        mt_numbers = []
        for num in mt_raw_floats:
            scaled_num = num * (case["range"][1] - case["range"][0])
            int_num = int(scaled_num) + case["range"][0]
            mt_numbers.append(int_num)
        
        print(f"LCG Test Case: {case['n_numbers']} numbers in range {case['range']}")
        print(f"First 10 LCG Numbers: {lcg_numbers[:10]}")
        print(f"MT Test Case: {case['n_numbers']} numbers in range {case['range']}")
        print(f"First 10 MT Numbers: {mt_numbers[:10]}")
        print("-" * 50)

# Execute test cases if this script is the main program being run
if __name__ == "__main__":
    run_test_cases()