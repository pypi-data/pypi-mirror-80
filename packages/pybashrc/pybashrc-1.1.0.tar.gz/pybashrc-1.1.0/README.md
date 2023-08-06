# `pybashrc`: Automatically register python functions as bash commands
This is a very simple utility that will create a `~/.pybashrc.py` file, and the functions it contains will be made accessible as bash commands.

By default, `pybashrc` aliases all functions that do not start with an underscore and were created in `~/.pybashrc.py` (i.e. they must not be imported). For example, this is the default template file:
```python
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
```

When running `pybash`, you'll see the available functions:
```
$ pybash
Available functions:
- test_pybashrc(first_argument: str, second_argument: str = 'second_argument')
	Default test function that simply prints its input arguments. This only serves as an example of how to define pybashrc functions.

	Arguments:
		- first_argument (str): The first argument.
		- second_argument (str): The second argument, which has a default value.
	
```

And you can now execute `test_pybashrc` directly from the command line:
```
$ test_pybashrc arg1 arg2
This is the pybash default test function.
Provided arguments: arg1, arg2
```

## Installation
Simply run `pip install pybashrc`, and then run `pybash-configure` once to set up the bash alias files etc. After that, you're ready to go! Any time you update your `.pybashrc.py`, your shell functions will also be updated (note that you'll need to restart the shell for a new alias to become available). If you forget which functions are available or what their usage is, simply run `pybash` to get an overview.

## Click functions
`pybashrc` also supports [click functions](https://click.palletsprojects.com/en/7.x/):
```python
import click

@click.command(
    help="A click command rather than a default python function."
    + " It has one argument with several options and a flag that can be toggled."
)
@click.argument(
    "first_arg",
    type=click.Choice(["option1", "option2", "option3"], case_sensitive=False),
)
@click.option(
    "-f",
    "--flag",
    is_flag=True,
    default=False,
    show_default=True,
    help="A command-line flag",
)
def click_function(first_arg, flag):
    print(f"Click function first arg: {first_arg}, flag: {flag}")
```

```
$ pybash
Available functions:
- click_function(first_arg, flag)
    Usage:  [OPTIONS] [option1|option2|option3]
    
      A click command rather than a default python function. It has one argument
      with several options and a flag that can be toggled.
    
    Options:
      -f, --flag  A command-line flag  [default: False]
      --help      Show this message and exit.

```

## Exporting external functions
You may want to make a CLI function available that is not part of your `.pybashrc.py` file. For example, let's say you want to make [`re.sub`](https://docs.python.org/3/library/re.html#re.sub) command-line accessible. This can be done very easily by simply importing it, and then specifying it in `__all__`:

```python
from re import sub

__all__ = ["sub"]
```

Whenever an `__all__` is specified, `pybashrc` will alias those functions regardless of whether they were defined in your `.pybashrc.py` or imported from elsewhere. If you now run `pybash` to see the available commands:
```
$ pybash
Available functions:
- sub(pattern, repl, string, count=0, flags=0)
    Return the string obtained by replacing the leftmost
    non-overlapping occurrences of the pattern in string by the
    replacement repl.  repl can be either a string or a callable;
    if a string, backslash escapes in it are processed.  If it is
    a callable, it's passed the Match object and must return
    a replacement string to be used.
```

So you can now call `sub <pattern> <replacement> <string>` directly from the command line!
```
$ sub "\s" "_" "some test string"
some_test_string
```

## Running from a different virtual environment
To run your pybash scripts from a different virtual environment, simply make sure that that environment has `pybashrc` installed and `pybash-configure` has been run from there once. Once that is done, `pybashrc` will simply execute your scripts with the currently active virtual environment!
