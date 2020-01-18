from Utils import dvfa_saver
from Utils import logger
from Utils import dvfa_generator
import DVFApy

from timeit import default_timer as timer
from functools import wraps

import os
import plotly.graph_objects as go
import resource
import sys

print(resource.getrlimit(resource.RLIMIT_STACK))
print(sys.getrecursionlimit())

max_rec = 0x10000

# May segfault without this line. 0x100 is a guess at the size of each stack frame.
resource.setrlimit(resource.RLIMIT_STACK, [0x100 * max_rec, resource.RLIM_INFINITY])
sys.setrecursionlimit(max_rec)


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

    # Performance Test 0
    n_1 = 5
    i_1 = 3
    i_n_1_dvfa = dvfa_generator.create_symmetrical_i_n_minus_i(n_1, i_1)

    dvfa_saver.save(i_n_1_dvfa, path_to_dvfa, i_n_1_dvfa.name)
    size_in_bytes = os.path.getsize(path_to_dvfa + i_n_1_dvfa.name + ".pickle")
    size_in_bites_y.append(size_in_bytes)
    size_in_bites_x.append(len(i_n_1_dvfa.state_set))
    dvfa_name.append(i_n_1_dvfa.name)

    n_2 = 600
    i_2 = 199
    i_n_2_dvfa = dvfa_generator.create_symmetrical_i_n_minus_i(n_2, i_2)
    dvfa_saver.save(i_n_2_dvfa, path_to_dvfa, i_n_2_dvfa.name)
    size_in_bytes = os.path.getsize(path_to_dvfa + i_n_2_dvfa.name + ".pickle")
    size_in_bites_y.append(size_in_bytes)
    size_in_bites_x.append(len(i_n_2_dvfa.state_set))
    dvfa_name.append(i_n_2_dvfa.name)

    # Performance Test 1
    n_1 = 5
    i_1 = 3
    i_n_1_dvfa = dvfa_generator.create_symmetrical_i_n_minus_i(n_1, i_1)

    n_2 = 50
    i_2 = 3
    i_n_2_dvfa = dvfa_generator.create_symmetrical_i_n_minus_i(n_2, i_2)

    intersected = analyse_intersect(i_n_1_dvfa, i_n_2_dvfa)

    dvfa_saver.save(intersected, path_to_dvfa, intersected.name)
    size_in_bytes = os.path.getsize(path_to_dvfa + intersected.name + ".pickle")
    size_in_bites_y.append(size_in_bytes)
    size_in_bites_x.append(len(intersected.state_set))
    dvfa_name.append(intersected.name)

    unioned = analyse_union(i_n_1_dvfa, i_n_2_dvfa)
    dvfa_saver.save(unioned, path_to_dvfa, unioned.name)
    size_in_bytes = os.path.getsize(path_to_dvfa + unioned.name + ".pickle")
    size_in_bites_y.append(size_in_bytes)
    size_in_bites_x.append(len(unioned.state_set))
    dvfa_name.append(unioned.name)

    # Performance Test 2
    n_1 = 50
    i_1 = 10
    i_n_1_dvfa = dvfa_generator.create_symmetrical_i_n_minus_i(n_1, i_1)

    n_2 = 500
    i_2 = 10
    i_n_2_dvfa = dvfa_generator.create_symmetrical_i_n_minus_i(n_2, i_2)

    intersected = analyse_intersect(i_n_1_dvfa, i_n_2_dvfa)

    try:
        dvfa_saver.save(intersected, path_to_dvfa, intersected.name)
    except RecursionError as e:
        print(e)
        print("For {}. with {} states".format(intersected.name,len(intersected.state_set)))

    size_in_bytes = os.path.getsize(path_to_dvfa + intersected.name + ".pickle")
    size_in_bites_y.append(size_in_bytes)
    size_in_bites_x.append(len(intersected.state_set))
    dvfa_name.append(intersected.name)

    unioned = analyse_union(i_n_1_dvfa, i_n_2_dvfa)
    try:
        dvfa_saver.save(unioned, path_to_dvfa, unioned.name)
    except RecursionError as e:
        print(e)
        print("For {}. with {} states".format(unioned.name, len(unioned.state_set)))
    size_in_bytes = os.path.getsize(path_to_dvfa + unioned.name + ".pickle")
    size_in_bites_y.append(size_in_bytes)
    size_in_bites_x.append(len(unioned.state_set))
    dvfa_name.append(unioned.name)

    # # Performance Test 3
    n_1 = 65
    i_1 = 45
    i_n_1_dvfa = dvfa_generator.create_symmetrical_i_n_minus_i(n_1, i_1)

    n_2 = 600
    i_2 = 199
    i_n_2_dvfa = dvfa_generator.create_symmetrical_i_n_minus_i(n_2, i_2)

    intersected = analyse_intersect(i_n_1_dvfa, i_n_2_dvfa)

    try:
        dvfa_saver.save(intersected, path_to_dvfa, intersected.name)
    except RecursionError as e:
        print(e)
        print("For {}. with {} states".format(intersected.name, len(intersected.state_set)))

    size_in_bytes = os.path.getsize(path_to_dvfa + intersected.name + ".pickle")
    size_in_bites_y.append(size_in_bytes)
    size_in_bites_x.append(len(intersected.state_set))
    dvfa_name.append(intersected.name)

    unioned = analyse_union(i_n_1_dvfa, i_n_2_dvfa)
    try:
        dvfa_saver.save(intersected, path_to_dvfa, unioned.name)
    except RecursionError as e:
        print(e)
        print("For {}. with {} states".format(unioned.name, len(unioned.state_set)))
    size_in_bytes = os.path.getsize(path_to_dvfa + unioned.name + ".pickle")
    size_in_bites_y.append(size_in_bytes)
    size_in_bites_x.append(len(unioned.state_set))
    dvfa_name.append(unioned.name)

    # Performance Test 4
    n_1 = 80
    i_1 = 45
    i_n_1_dvfa = dvfa_generator.create_symmetrical_i_n_minus_i(n_1, i_1)

    n_2 = 650
    i_2 = 19
    i_n_2_dvfa = dvfa_generator.create_symmetrical_i_n_minus_i(n_2, i_2)

    intersected = analyse_intersect(i_n_1_dvfa, i_n_2_dvfa)

    try:
        dvfa_saver.save(intersected, path_to_dvfa, intersected.name)
    except RecursionError as e:
        print(e)
        print("For {}. with {} states".format(intersected.name, len(intersected.state_set)))

    size_in_bytes = os.path.getsize(path_to_dvfa + intersected.name + ".pickle")
    size_in_bites_y.append(size_in_bytes)
    size_in_bites_x.append(len(intersected.state_set))
    dvfa_name.append(intersected.name)

    unioned = analyse_union(i_n_1_dvfa, i_n_2_dvfa)
    try:
        dvfa_saver.save(intersected, path_to_dvfa, unioned.name)
    except RecursionError as e:
        print(e)
        print("For {}. with {} states".format(unioned.name, len(unioned.state_set)))
    size_in_bytes = os.path.getsize(path_to_dvfa + unioned.name + ".pickle")
    size_in_bites_y.append(size_in_bytes)
    size_in_bites_x.append(len(unioned.state_set))
    dvfa_name.append(unioned.name)

    # Graph preparations
    pickle_size_scatter = go.Scatter(
        x=size_in_bites_x,
        y=[size / 1000.0 for size in size_in_bites_y],
        text=dvfa_name,
        mode='markers',
        marker=dict(size=40,
                    color=[color for color in range(len(size_in_bites_x) + 1)])
    )
    pickle_size_layout = go.Layout(
        title=go.layout.Title(
            text="Pickled file size analysis"),  # on word {}, [length: {}]".format(word.word, word.get_word_length())
        xaxis_title="Number of states",
        yaxis_title="Pickl size [KB]",
    )

    pickle_size_fig = go.Figure(
        data=pickle_size_scatter,
        layout=pickle_size_layout
    )
    pickle_size_fig.show()
