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

    # Performance Test 1
    pal_3 = dvfa_generator.create_3PAL_DVFA()
    dvfa_name.append(pal_3.name)
    num_of_states.append(len(pal_3.state_set))

    run = DVFApy.run.Run(pal_3, word)

    # word_length.append(word.get_word_length())
    accepted_arr.append(analyse_run(run))
    run_time_arr.append(run_time)

    # Performance Test 2
    longer_than_one = dvfa_generator.create_word_longer_than_1()
    dvfa_name.append(longer_than_one.name)
    num_of_states.append(len(longer_than_one.state_set))

    run = DVFApy.run.Run(longer_than_one, word)

    # word_length.append(word.get_word_length())
    accepted_arr.append(analyse_run(run))
    run_time_arr.append(run_time)

    # Performance Test 3
    longer_than_one_join_pal_3 = DVFApy.dvfa.DVFA.union(longer_than_one, pal_3)
    dvfa_name.append(longer_than_one_join_pal_3.name)
    num_of_states.append(len(longer_than_one_join_pal_3.state_set))

    run = DVFApy.run.Run(longer_than_one_join_pal_3, word)

    # word_length.append(word.get_word_length())
    accepted_arr.append(analyse_run(run))
    run_time_arr.append(run_time)

    # Performance Test 4
    C_longer_than_one_join_pal_3 = DVFApy.dvfa.DVFA.complement(longer_than_one_join_pal_3)
    dvfa_name.append(C_longer_than_one_join_pal_3.name)
    num_of_states.append(len(C_longer_than_one_join_pal_3.state_set))

    run = DVFApy.run.Run(C_longer_than_one_join_pal_3, word)
    # word_length.append(word.get_word_length())

    accepted_arr.append(analyse_run(run))
    run_time_arr.append(run_time)

    desired_pal_len = 6
    palindromes = word_generator.palin_generator(desired_pal_len)  # Create all palindromes with desired length.
    # Split a palindrome to its letters
    a_palindrome = [letter for letter in palindromes[9]]  # some palindrome
    # Create the Word representing this palindrome
    a_palindrome = DVFApy.word.Word([int(d) for d in a_palindrome])

    # Graph preparations
    bar = go.Bar(x=num_of_states, y=run_time_arr, text=dvfa_name)

    layout = go.Layout(
        title=go.layout.Title(text="Runtime analysis, on word length: {}".format(word.get_word_length())),
        xaxis_title="Number of states",
        yaxis_title="Run time",
    )

    fig = go.Figure(
        data=[bar],
        layout=layout
    )

    fig.show()
