# import pure_python_random_library as py_random
import py_random_source_code as py_random
from typing import List
import lcg  # Import the lcg.py module
import random
import time
import memory_profiler
from matplotlib import pyplot as plt
from scipy import stats
import numpy as np

def print_statistics(case_name, time_taken, memory_used, chi_stat, chi_p, auto_corr):
    print(f"{case_name} Test Case:")
    print(f"  Time taken: {time_taken:.6f}s")
    print(f"  Memory used: {memory_used:.6f} MiB")
    print(f"  Statistics Results:")
    print(f"    Chi-Squared Statistic: {chi_stat}")
    print(f"    P-Value: {chi_p}")
    print(f"    Autocorrelation Coefficient: {auto_corr}\n")

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
    seed = 123456789
    
    # Initialize the Mersenne Twister with a random seed
    mt = MersenneTwister(seed)
    
    test_cases = [
        {"n_numbers": 1000, "range": (1, 1000000)},
        {"n_numbers": 100000, "range": (1, 1000000)},
        {"n_numbers": 1000000, "range": (1, 1000000)},
        {"n_numbers": 10000000, "range": (1, 100000000)},
    ]
    
    for case in test_cases:
        # Memory and time measurement start for LCG
        start_time_lcg = time.perf_counter()
        mem_usage_start_lcg = memory_profiler.memory_usage()
        
        # Generating LCG numbers
        lcg_raw_floats = lcg.rand_float_samples(case["n_numbers"], m, a, c, seed)
        lcg_numbers = [int(num * (case["range"][1] - case["range"][0])) + case["range"][0]
                       for num in lcg_raw_floats]
        
        # Memory and time measurement end for LCG
        mem_usage_end_lcg = memory_profiler.memory_usage()
        end_time_lcg = time.perf_counter()
        
        # Memory and time measurement start for MT
        start_time_mt = time.perf_counter()
        mem_usage_start_mt = memory_profiler.memory_usage()
        
        # Generating MT numbers
        mt_raw_floats = mt.generate_sequence(case["n_numbers"])
        mt_numbers = [int(num * (case["range"][1] - case["range"][0])) + case["range"][0]
                      for num in mt_raw_floats]
        
        # Memory and time measurement end for MT
        mem_usage_end_mt = memory_profiler.memory_usage()
        end_time_mt = time.perf_counter()
        
        # Calculate performance metrics
        time_taken_lcg = end_time_lcg - start_time_lcg
        mem_used_lcg = max(mem_usage_end_lcg) - min(mem_usage_start_lcg)
        
        time_taken_mt = end_time_mt - start_time_mt
        mem_used_mt = max(mem_usage_end_mt) - min(mem_usage_start_mt)

        # Chi-squared test for uniformity for LCG
        observed_frequencies, _ = np.histogram(lcg_numbers, bins=50)
        expected_frequencies = np.full_like(observed_frequencies, len(lcg_numbers)/50)
        chi_square_statistic_lcg, p_value_lcg = stats.chisquare(observed_frequencies, expected_frequencies)
        autocorr_coefficient_lcg = np.corrcoef(lcg_numbers[:-1], lcg_numbers[1:])[0, 1]

        # Chi-squared test for uniformity for MT
        observed_frequencies, _ = np.histogram(mt_numbers, bins=50)
        expected_frequencies = np.full_like(observed_frequencies, len(mt_numbers)/50)
        chi_square_statistic_mt, p_value_mt = stats.chisquare(observed_frequencies, expected_frequencies)
        autocorr_coefficient_mt = np.corrcoef(mt_numbers[:-1], mt_numbers[1:])[0, 1]

        # Print results
        print_statistics('LCG', time_taken_lcg, mem_used_lcg, chi_square_statistic_lcg, p_value_lcg, autocorr_coefficient_lcg)
        print_statistics('MT', time_taken_mt, mem_used_mt, chi_square_statistic_mt, p_value_mt, autocorr_coefficient_mt)
        print('-' * 50)
        
        # Plotting the results for visual comparison
        plt.figure(figsize=(12, 6))

        plt.subplot(1, 2, 1)
        plt.hist(lcg_numbers, bins=50, alpha=0.7, label='LCG')  # Increased number of bins to 100
        plt.title('LCG Distribution')
        plt.xlabel('Number')
        plt.ylabel('Frequency')

        plt.subplot(1, 2, 2)
        plt.hist(mt_numbers, bins=50, alpha=0.7, label='Mersenne Twister')  # Increased number of bins to 100
        plt.title('Mersenne Twister Distribution')
        plt.xlabel('Number')
        plt.ylabel('Frequency')

        plt.tight_layout()
        plt.savefig(f"plots/{case['n_numbers']}_numbers.png")

if __name__ == "__main__":
    run_test_cases()