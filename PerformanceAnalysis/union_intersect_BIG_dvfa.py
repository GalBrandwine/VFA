from functools import wraps
from timeit import default_timer as timer
from itertools import permutations
import numpy as np
import plotly.graph_objects as go

import DVFApy
from Utils import dvfa_generator
from Utils import logger
from Utils import word_generator


def timeit_wrapper(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        global run_time
        start = timer()
        func_return_val = func(*args, **kwargs)
        end = timer()
        # logger.log_print('Run time: {0:<10}.{1:<8} : {2:<8} sec'.format(func.__module__, func.__name__, end - start))
        run_time = end - start
        logger.log_print('Run time: {0:<8} sec'.format(run_time))
        # logger.log_print('Run time: {0:<8} sec'.format(end - start))
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
    intersection_name = []
    intersection_x = []
    intersection_y = []

    union_name = []
    union_x = []
    union_y = []

    run_x = []
    run_y = []

    desired_pal_len = 6
    palindromes = word_generator.palin_generator(desired_pal_len)  # Create all palindromes with desired length.
    a_palindrome = [letter for letter in
                    palindromes[np.random.randint(len(palindromes))]]  # Split a palindrome to its letters
    word = DVFApy.word.Word([int(d) for d in a_palindrome])  # Create the Word representing this palindrome

    # Performance Test 1
    dvfas = []
    for i in range(1, 50):
        for n in range(i, 250):
            n_1 = n
            i_1 = i
            i_n_1_dvfa = dvfa_generator.create_symmetrical_i_n_minus_i(n_1, i_1)
            dvfas.append(i_n_1_dvfa)

    # n_2 = 50
    # i_2 = 3
    # i_n_2_dvfa = dvfa_generator.create_symmetrical_i_n_minus_i(n_2, i_2)



    # Get all permutations of length 2
    # and length 2
    perm = permutations(dvfas, 2)

    # Print the obtained permutations
    for A, B in perm:
        intersected = analyse_intersect(A, B)
        intersection_x.append(len(intersected.state_set))
        intersection_y.append(run_time)
        intersection_name.append(intersected.name)

        unioned = analyse_union(A, B)
        union_x.append(len(unioned.state_set))
        union_y.append(run_time)
        union_name.append(unioned.name)

        run = DVFApy.run.Run(intersected, word)
        accepted = analyse_run(run)
        run_y.append(run_time)
        run = DVFApy.run.Run(unioned, word)
        accepted = analyse_run(run)
        run_y.append(run_time)
    #
    # # # Performance Test 2
    # n_1 = 50
    # i_1 = 10
    # i_n_1_dvfa = dvfa_generator.create_symmetrical_i_n_minus_i(n_1, i_1)
    #
    # n_2 = 500
    # i_2 = 10
    # i_n_2_dvfa = dvfa_generator.create_symmetrical_i_n_minus_i(n_2, i_2)
    #
    # intersected = analyse_intersect(i_n_1_dvfa, i_n_2_dvfa)
    # intersection_x.append(len(intersected.state_set))
    # intersection_y.append(run_time)
    # intersection_name.append(intersected.name)
    #
    # unioned = analyse_union(i_n_1_dvfa, i_n_2_dvfa)
    # union_x.append(len(unioned.state_set))
    # union_y.append(run_time)
    # union_name.append(unioned.name)
    #
    # run = DVFApy.run.Run(intersected, word)
    # accepted = analyse_run(run)
    # run_y.append(run_time)
    # run = DVFApy.run.Run(unioned, word)
    # accepted = analyse_run(run)
    # run_y.append(run_time)
    #
    # # Performance Test 3
    # n_1 = 65
    # i_1 = 45
    # i_n_1_dvfa = dvfa_generator.create_symmetrical_i_n_minus_i(n_1, i_1)
    #
    # n_2 = 600
    # i_2 = 199
    # i_n_2_dvfa = dvfa_generator.create_symmetrical_i_n_minus_i(n_2, i_2)
    #
    # intersected = analyse_intersect(i_n_1_dvfa, i_n_2_dvfa)
    # intersection_x.append(len(intersected.state_set))
    # intersection_y.append(run_time)
    # intersection_name.append(intersected.name)
    #
    # unioned = analyse_union(i_n_1_dvfa, i_n_2_dvfa)
    # union_x.append(len(unioned.state_set))
    # union_y.append(run_time)
    # union_name.append(unioned.name)
    #
    # run = DVFApy.run.Run(intersected, word)
    # accepted = analyse_run(run)
    # run_y.append(run_time)
    # run = DVFApy.run.Run(unioned, word)
    # accepted = analyse_run(run)
    # run_y.append(run_time)
    #
    # # Performance Test 4
    # n_1 = 80
    # i_1 = 45
    # i_n_1_dvfa = dvfa_generator.create_symmetrical_i_n_minus_i(n_1, i_1)
    #
    # n_2 = 650
    # i_2 = 19
    # i_n_2_dvfa = dvfa_generator.create_symmetrical_i_n_minus_i(n_2, i_2)
    #
    # intersected = analyse_intersect(i_n_1_dvfa, i_n_2_dvfa)
    # intersection_x.append(len(intersected.state_set))
    # intersection_y.append(run_time)
    # intersection_name.append(intersected.name)
    #
    # unioned = analyse_union(i_n_1_dvfa, i_n_2_dvfa)
    # union_x.append(len(unioned.state_set))
    # union_y.append(run_time)
    # union_name.append(unioned.name)
    #
    # run = DVFApy.run.Run(intersected, word)
    # accepted = analyse_run(run)
    # run_y.append(run_time)
    # run = DVFApy.run.Run(unioned, word)
    # accepted = analyse_run(run)
    # run_y.append(run_time)

    # Graph preparations

    union_graph_bars = go.Scatter(
        x=union_x,
        y=union_y,
        hovertext=union_name,
        mode='markers',
        marker=dict(size=20,
                    color=[color for color in range(len(union_x))])
    )
    union_layout = go.Layout(
        title=go.layout.Title(text="Runtime analysis: UNION"),
        xaxis_title="Number of states",
        yaxis_title="Run time [sec]",
    )

    union_fig = go.Figure(
        data=union_graph_bars,
        layout=union_layout
    )
    union_fig.update_layout(barmode='group')
    union_fig.show()

    intersected_graph_bars = go.Scatter(
        x=intersection_x,
        y=intersection_y,
        hovertext=intersection_name,
        mode='markers',
        marker=dict(size=40,
                    color=[color for color in range(len(intersection_x))])
    )
    intersection_layout = go.Layout(
        title=go.layout.Title(text="Runtime analysis: INTERSECTION"),
        xaxis_title="Number of states",
        yaxis_title="Run time [sec]",
    )

    intersetion_fig = go.Figure(
        data=intersected_graph_bars,
        layout=intersection_layout
    )

    intersetion_fig.show()

    run_x = union_x + intersection_x
    run_graph_bars = go.Scatter(
        x=run_x,
        y=run_y,
        hovertext=union_name + intersection_name,
        mode='markers',
        marker=dict(size=40,
                    color=[color for color in range(len(run_x))])
    )
    run_on_word_layout = go.Layout(
        title=go.layout.Title(
            text="Runtime analysis, on word {}, [length: {}]".format(word.word, word.get_word_length())),
        xaxis_title="Number of states",
        yaxis_title="Run time [sec]",
    )

    run_on_word_fig = go.Figure(
        data=run_graph_bars,
        layout=run_on_word_layout
    )
    run_on_word_fig.show()
