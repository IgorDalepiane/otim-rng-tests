# import pure_python_random_library as py_random
import argparse
import py_random_source_code as py_random
from typing import List
import lcg  # Import the lcg.py module
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

def run_test_cases(lcg_multiplier, lcg_modulus, lcg_increment, seed, maxRange, count=None):
    # Initialize the Mersenne Twister with a random seed
    mt = MersenneTwister(seed)
    
    test_cases = [
        {"n_numbers": 1000, "range": (0, 100)},
        {"n_numbers": 100000, "range": (1, 10000)},
        {"n_numbers": 1000000, "range": (1, 1000000)},
    ]

    if count is not None:
        test_cases = [{"n_numbers": count, "range": (1, maxRange)}]
    
    for case in test_cases:
        # Memory and time measurement start for LCG
        start_time_lcg = time.perf_counter()
        mem_usage_start_lcg = memory_profiler.memory_usage()

        # Generating LCG numbers
        lcg_raw_floats = lcg.rand_float_samples(case["n_numbers"], lcg_modulus, lcg_multiplier, lcg_increment, seed)
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
        plt.hist(lcg_numbers, bins=50, alpha=0.7, label='LCG')
        plt.title('LCG Distribution')
        plt.xlabel('Number')
        plt.ylabel('Frequency')

        plt.subplot(1, 2, 2)
        plt.hist(mt_numbers, bins=50, alpha=0.7, label='Mersenne Twister')
        plt.title('Mersenne Twister Distribution')
        plt.xlabel('Number')
        plt.ylabel('Frequency')

        plt.tight_layout()
        plt.savefig(f"plots/{case['n_numbers']}_numbers.png")


def main():
    parser = argparse.ArgumentParser(description="RNG Test Cases comparing LCG and MT algorithms")

    parser.add_argument(
        "--lcg_modulus", type=int, default=2**32, help="Modulus 'm' in LCG"
    )
    parser.add_argument(
        "--lcg_multiplier", type=int, default=594_156_893, help="Multiplier 'a' in LCG"
    )
    parser.add_argument(
        "--lcg_increment", type=int, default=0, help="Increment 'c' in LCG"
    )
    parser.add_argument(
        "--seed", type=int, required=False, help="Initial seed for LCG and MT"
    )
    parser.add_argument(
        "--count", type=int, required=False, help="Number of random numbers to generate"
    )
    parser.add_argument(
        "--max_range", type=int, default=1000000, help="Range of the numbers to be generated"
    )

    args = parser.parse_args()

    if args.lcg_multiplier >= args.lcg_modulus or args.lcg_increment >= args.lcg_modulus:
        raise ValueError("Multiplier and increment must be less than modulus")

    # Access the LCG parameters from the args namespace
    lcg_multiplier = args.lcg_multiplier
    lcg_modulus = args.lcg_modulus
    lcg_increment = args.lcg_increment
    seed = args.seed or py_random.Random().randint(0, 2**32 - 1)
    count = args.count
    maxRange = args.max_range

    # log
    print(f"LCG Multiplier: {lcg_multiplier}")
    print(f"LCG Increment: {lcg_increment}")
    print(f"LCG Modulus: {lcg_modulus}")
    print(f"Seed: {seed}")
    if count is not None:
        print(f"Count: {count}")
        print(f"Range: 1 - {maxRange}")

    run_test_cases(lcg_multiplier, lcg_modulus, lcg_increment, seed, maxRange, count)
    
if __name__ == "__main__":
    main()