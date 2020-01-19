from Utils import dvfa_saver
from Utils import logger
from Utils import dvfa_generator
import DVFApy

from timeit import default_timer as timer
from functools import wraps

import resource
import sys

def timeit_wrapper(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        global run_time
        start = timer()
        func_return_val = func(*args, **kwargs)
        end = timer()
        run_time = end - start
        logger.log_print('Run time: {0:<8} sec'.format(run_time))
        return func_return_val

    return wrapper


@timeit_wrapper
def analyse_run(run: DVFApy.run.Run) -> bool:
    return run.run()


@timeit_wrapper
def analyse_intersect(A: DVFApy.dvfa.DVFA, B: DVFApy.dvfa.DVFA) -> DVFApy.dvfa.DVFA:
    return DVFApy.dvfa.DVFA.intersect(A, B)


@timeit_wrapper
def analyse_union(A: DVFApy.dvfa.DVFA, B: DVFApy.dvfa.DVFA) -> DVFApy.dvfa.DVFA:
    return DVFApy.dvfa.DVFA.union(A, B)


# Performance Analysis
if __name__ == "__main__":
    path_to_dvfa = "/media/gal/DATA/Documents/projects/VFA/Docs/PicleSizeAnalysis/"  # Hard coded path.

    size_in_bites_x = []
    size_in_bites_y = []
    dvfa_name = []

    # Performance Test 1
    n_1 = 80
    i_1 = 45
    i_n_1_dvfa = dvfa_generator.create_symmetrical_i_n_minus_i(n_1, i_1)

    n_2 = 650
    i_2 = 19
    i_n_2_dvfa = dvfa_generator.create_symmetrical_i_n_minus_i(n_2, i_2)

    intersected = analyse_intersect(i_n_1_dvfa, i_n_2_dvfa)

    print("Default recursionlimit: {}".format(resource.getrlimit(resource.RLIMIT_STACK)))
    print(sys.getrecursionlimit())

    max_rec = 0x100
    keep_testing = True
    while keep_testing:
        try:
            dvfa_saver.save(intersected, path_to_dvfa, intersected.name)
            print("*"*10+" Found recursoinlimit setting deep enough! "+"*"*10)
            print("Recursoinlimit setting: {}".format(sys.getrecursionlimit()))
            keep_testing = False
        except RecursionError as e:

            # May segfault without this line. 0x100 is a guess at the size of each stack frame.
            resource.setrlimit(resource.RLIMIT_STACK, [0x100 * max_rec, resource.RLIM_INFINITY])
            sys.setrecursionlimit(max_rec)

            print(resource.getrlimit(resource.RLIMIT_STACK))
            print(sys.getrecursionlimit())
            print(e)
            print("For {}. with {} states".format(intersected.name, len(intersected.state_set)))

            max_rec = max_rec + 100
