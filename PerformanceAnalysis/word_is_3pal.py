from Utils import logger
from Utils import word_generator
from Utils import dvfa_generator
import DVFApy
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


# Performance Analysis
if __name__ == "__main__":
    dvfa_name = []
    num_of_states = []
    word_length = []
    accepted_arr = []
    run_time_arr = []

    word = word_generator.get_pal3_word()
    graph_bars = []

    # Performance Test 1
    pal_3 = dvfa_generator.create_3PAL_DVFA()
    dvfa_name.append(pal_3.name)
    num_of_states.append(len(pal_3.state_set))

    run = DVFApy.run.Run(pal_3, word)

    # word_length.append(word.get_word_length())
    accepted = analyse_run(run)
    accepted_arr.append(accepted)
    run_time_arr.append(run_time)
    graph_bars.append(
        go.Bar(x=[len(pal_3.state_set)], y=[run_time], name=pal_3.name, text="accepted: {}".format(accepted)))

    # Performance Test 2
    longer_than_one = dvfa_generator.create_word_longer_than_1()
    dvfa_name.append(longer_than_one.name)
    num_of_states.append(len(longer_than_one.state_set))

    run = DVFApy.run.Run(longer_than_one, word)
    accepted = analyse_run(run)
    accepted_arr.append(accepted)
    run_time_arr.append(run_time)
    graph_bars.append(go.Bar(x=[len(longer_than_one.state_set)], y=[run_time], name=longer_than_one.name,
                             text="accepted: {}".format(accepted)))

    # Performance Test 3
    longer_than_one_join_pal_3 = DVFApy.dvfa.DVFA.union(longer_than_one, pal_3)
    dvfa_name.append(longer_than_one_join_pal_3.name)
    num_of_states.append(len(longer_than_one_join_pal_3.state_set))

    run = DVFApy.run.Run(longer_than_one_join_pal_3, word)
    accepted = analyse_run(run)
    accepted_arr.append(accepted)
    run_time_arr.append(run_time)
    graph_bars.append(
        go.Bar(x=[len(longer_than_one_join_pal_3.state_set)], y=[run_time], name=longer_than_one_join_pal_3.name,
               text="accepted: {}".format(accepted)))

    # Performance Test 4
    C_longer_than_one_join_pal_3 = DVFApy.dvfa.DVFA.complement(longer_than_one_join_pal_3)
    dvfa_name.append(C_longer_than_one_join_pal_3.name)
    num_of_states.append(len(C_longer_than_one_join_pal_3.state_set))

    run = DVFApy.run.Run(C_longer_than_one_join_pal_3, word)
    accepted = analyse_run(run)
    accepted_arr.append(accepted)
    run_time_arr.append(run_time)
    graph_bars.append(
        go.Bar(x=[len(C_longer_than_one_join_pal_3.state_set)], y=[run_time], name=C_longer_than_one_join_pal_3.name,
               text="accepted: {}".format(accepted)))

    # Graph preparations
    layout = go.Layout(
        title=go.layout.Title(text="Runtime analysis, on word length: {}".format(word.get_word_length())),

        xaxis_title="Number of states",
        yaxis_title="Run time",

    )

    fig = go.Figure(
        data=graph_bars,
        layout=layout
    )
    fig.update_layout(barmode='group')
    fig.show()