# Pybashrc file. Create your command-line accessible python functions here.
def _hidden_print_function(*args):
    """This function will be ignored by pybashrc, and will not be available from the
    command line.

    However, other functions can still use it.
    """
    print(*args)


def test_pybashrc(first_argument: str, second_argument: str = "second_argument"):
    """Default test function that simply prints its input arguments. This only serves as
    an example of how to define pybashrc functions.

    Arguments:
        - first_argument (str): The first argument.
        - second_argument (str): The second argument, which has a default value.
    """
    _hidden_print_function("This is the pybash default test function.")
    _hidden_print_function(f"Provided arguments: {first_argument}, {second_argument}")
