import time
import matplotlib.pyplot as plt


# 10000 elements => 4 numbers between 10000 => 0, [10000, 7500, 5000, 2500, 0]
def timeit(their_function, their_function_number_arg):
    time_array = {}
    # generate 5 times we should measure based on the max_size user put in
    for i in range(0, their_function_number_arg + 1, their_function_number_arg // 4):
        before = time.clock()
        their_function(i)
        time_array[i] = time.clock() - before
    return time_array


def graphit(their_function, their_function_number_arg):
    time_array = {}
    # generate 5 times we should measure based on the max_size user put in
    for i in range(0, their_function_number_arg + 1, their_function_number_arg // 4):
        before = time.clock()
        their_function(i)
        time_array[i] = time.clock() - before
    plt.clf()
    plt.plot(list(time_array.keys()), list(time_array.values()),
             label="custom_label")

    plt.show()
