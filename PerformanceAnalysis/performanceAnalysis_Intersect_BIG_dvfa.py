from Utils import logger
from Utils import word_generator
from Utils import dvfa_generator
import DVFApy
import numpy as np
from timeit import default_timer as timer
from functools import wraps

import plotly.graph_objects as go


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
    union_graph_bars = []
    intersection_graph_bars = []
    run_graph_bars = []

    desired_pal_len = 6
    palindromes = word_generator.palin_generator(desired_pal_len)  # Create all palindromes with desired length.
    a_palindrome = [letter for letter in
                    palindromes[np.random.randint(len(palindromes))]]  # Split a palindrome to its letters
    word = DVFApy.word.Word([int(d) for d in a_palindrome])  # Create the Word representing this palindrome

    # Performance Test 1
    n_1 = 5
    i_1 = 3
    i_n__dvfa = dvfa_generator.create_symmetrical_i_n_minus_i(n_1, i_1)

    n_2 = 50
    i_2 = 3
    i_n_2_dvfa = dvfa_generator.create_symmetrical_i_n_minus_i(n_2, i_2)

    intersected = analyse_intersect(i_n__dvfa, i_n_2_dvfa)
    intersection_graph_bars.append(
        go.Scatter(x=[len(intersected.state_set)], y=[run_time], name=intersected.name))  # text="accepted: {}".format(None)

    unioned = analyse_union(i_n__dvfa, i_n_2_dvfa)
    union_graph_bars.append(
        go.Scatter(x=[len(unioned.state_set)], y=[run_time], name=unioned.name))  # text="accepted: {}".format(None)

    run = DVFApy.run.Run(intersected, word)
    accepted = analyse_run(run)
    run_graph_bars.append(go.Scatter(x=[len(intersected.state_set)], y=[run_time], name=intersected.name,
                                 text="accepted: {}".format(accepted)))
    run = DVFApy.run.Run(unioned, word)
    accepted = analyse_run(run)
    run_graph_bars.append(go.Scatter(x=[len(unioned.state_set)], y=[run_time], name=unioned.name,
                                 text="accepted: {}".format(accepted)))

    # Performance Test 2
    n_1 = 50
    i_1 = 10
    i_n_10_50_dvfa = dvfa_generator.create_symmetrical_i_n_minus_i(n_1, i_1)

    n_2 = 500
    i_2 = 10
    i_n_10_500_dvfa = dvfa_generator.create_symmetrical_i_n_minus_i(n_2, i_2)

    intersected = analyse_intersect(i_n_10_50_dvfa, i_n_10_500_dvfa)
    intersection_graph_bars.append(
        go.Scatter(x=[len(intersected.state_set)], y=[run_time], name=intersected.name))  # text="accepted: {}".format(None)

    unioned = analyse_union(i_n_10_50_dvfa, i_n_10_500_dvfa)
    union_graph_bars.append(
        go.Scatter(x=[len(unioned.state_set)], y=[run_time], name=unioned.name))  # text="accepted: {}".format(None)

    run = DVFApy.run.Run(intersected, word)
    accepted = analyse_run(run)
    run_graph_bars.append(go.Scatter(x=[len(intersected.state_set)], y=[run_time], name=intersected.name,
                                 text="accepted: {}".format(accepted)))
    run = DVFApy.run.Run(unioned, word)
    accepted = analyse_run(run)
    run_graph_bars.append(go.Scatter(x=[len(unioned.state_set)], y=[run_time], name=unioned.name,
                                 text="accepted: {}".format(accepted)))

    # Performance Test 2
    n_1 = 65
    i_1 = 45
    i_n_10_50_dvfa = dvfa_generator.create_symmetrical_i_n_minus_i(n_1, i_1)

    n_2 = 600
    i_2 = 199
    i_n_10_500_dvfa = dvfa_generator.create_symmetrical_i_n_minus_i(n_2, i_2)

    intersected = analyse_intersect(i_n_10_50_dvfa, i_n_10_500_dvfa)
    intersection_graph_bars.append(
        go.Scatter(x=[len(intersected.state_set)], y=[run_time], name=intersected.name))  # text="accepted: {}".format(None)

    unioned = analyse_union(i_n_10_50_dvfa, i_n_10_500_dvfa)
    union_graph_bars.append(
        go.Scatter(x=[len(unioned.state_set)], y=[run_time], name=unioned.name))  # text="accepted: {}".format(None)

    run = DVFApy.run.Run(intersected, word)
    accepted = analyse_run(run)
    run_graph_bars.append(go.Scatter(x=[len(intersected.state_set)], y=[run_time], name=intersected.name,
                                 text="accepted: {}".format(accepted)))
    run = DVFApy.run.Run(unioned, word)
    accepted = analyse_run(run)
    run_graph_bars.append(go.Scatter(x=[len(unioned.state_set)], y=[run_time], name=unioned.name,
                                 text="accepted: {}".format(accepted)))

    # Performance Test 3
    n_1 = 80
    i_1 = 45
    i_n_10_50_dvfa = dvfa_generator.create_symmetrical_i_n_minus_i(n_1, i_1)

    n_2 = 650
    i_2 = 19
    i_n_10_500_dvfa = dvfa_generator.create_symmetrical_i_n_minus_i(n_2, i_2)

    intersected = analyse_intersect(i_n_10_50_dvfa, i_n_10_500_dvfa)
    intersection_graph_bars.append(
        go.Scatter(x=[len(intersected.state_set)], y=[run_time], name=intersected.name))  # text="accepted: {}".format(None)

    unioned = analyse_union(i_n_10_50_dvfa, i_n_10_500_dvfa)
    union_graph_bars.append(
        go.Scatter(x=[len(unioned.state_set)], y=[run_time], name=unioned.name))  # text="accepted: {}".format(None)

    run = DVFApy.run.Run(intersected, word)
    accepted = analyse_run(run)
    run_graph_bars.append(go.Scatter(x=[len(intersected.state_set)], y=[run_time], name=intersected.name,
                                 text="accepted: {}".format(accepted)))
    run = DVFApy.run.Run(unioned, word)
    accepted = analyse_run(run)
    run_graph_bars.append(go.Scatter(x=[len(unioned.state_set)], y=[run_time], name=unioned.name,
                                 text="accepted: {}".format(accepted)))

    # Graph preparations
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

    intersection_layout = go.Layout(
        title=go.layout.Title(text="Runtime analysis: INTERSECTION"),
        xaxis_title="Number of states",
        yaxis_title="Run time [sec]",
    )

    intersetion_fig = go.Figure(
        data=intersection_graph_bars,
        layout=intersection_layout
    )
    intersetion_fig.update_layout(barmode='group')
    intersetion_fig.show()

    run_on_word_layout = go.Layout(
        title=go.layout.Title(text="Runtime analysis, on word {}, [length: {}]".format(word.word,word.get_word_length())),
        xaxis_title="Number of states",
        yaxis_title="Run time [sec]",
    )

    run_on_word_fig = go.Figure(
        data=run_graph_bars,
        layout=run_on_word_layout
    )
    run_on_word_fig.update_layout(barmode='group')
    run_on_word_fig.show()
