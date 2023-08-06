import inspect
import os
import sys
import traceback
from pathlib import Path

import click

import pybashrc.pybashrc_link as pybashrc_link

_INSTALL_DIR = Path(os.environ["PYBASHRC_INSTALL_DIR"])


# If pybashrc contains an __all__, simply import all functions from there
if hasattr(pybashrc_link, "__all__"):
    _FUNCTIONS = {}
    for name in getattr(pybashrc_link, "__all__"):
        object = getattr(pybashrc_link, name)
        if inspect.isfunction(object) or isinstance(object, click.Command):
            _FUNCTIONS[name] = object

# If not, import all functions that are in its scope that do not start with _ and
# actually originate from the file itself (i.e. they must not be imported)
else:
    _FUNCTIONS = {}
    for name in dir(pybashrc_link):
        if name.startswith("_"):
            continue

        object = getattr(pybashrc_link, name)
        if (
            isinstance(object, click.Command)
            # click commands are incompatible with inspect.getfile
            and inspect.getfile(object.callback) == pybashrc_link.__file__
        ):
            _FUNCTIONS[name] = object

        elif (
            inspect.isfunction(object)
            and inspect.getfile(object) == pybashrc_link.__file__
        ):
            _FUNCTIONS[name] = object


def _get_function_info(func):
    """Create a string containing the function name, its arguments and the docstring if
    there is any."""

    command = None
    # If this is a click command, use its wrapped function for the time being
    if isinstance(func, click.Command):
        command = func
        func = command.callback

    string = f"{func.__name__}{inspect.signature(func)}"
    if func.__doc__:
        string += f"\n    {func.__doc__}"

    # After printing the regular info, print the click help string if applicable
    if command:
        # Needs some extra indentation
        help_string = command.get_help(click.Context(command)).replace("\n", "\n    ")
        string += f"\n    {help_string}"

    return string


def _update_aliases():
    """Create a bash alias for all of the user-defined functions in ~/.pybashrc.py."""
    aliases = (_INSTALL_DIR / "templates" / ".pybashrc_aliases").read_text()
    for name in _FUNCTIONS.keys():
        aliases += f"alias {name}='pybash {name}'\n"

    (_INSTALL_DIR / ".pybashrc_aliases").write_text(aliases)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Available functions:")
        for function in _FUNCTIONS.values():
            print(f"- {_get_function_info(function)}\n")
        exit(0)

    name = sys.argv[1]

    # System command not intended to be accessed by the user
    if name == "_update_aliases":
        _update_aliases()
        exit(0)

    # Check if the function exists
    if name not in _FUNCTIONS.keys():
        raise ValueError(f"pybashrc received unknown function name {name}!")

    function = _FUNCTIONS[name]
    # If this is a click command, let click handle the rest
    if isinstance(function, click.Command):
        function.main(sys.argv[2:], prog_name=name)

    # Otherwise, parse arguments and keyword arguments
    args = []
    kwargs = {}
    for arg in sys.argv[2:]:
        if "=" in arg:
            key, value = arg.split("=")
            kwargs[key] = value
        else:
            args.append(arg)

    # Call function
    try:
        result = _FUNCTIONS[name](*args, **kwargs)
        if result is not None:
            print(result)
    except TypeError:
        # Print the exception without exiting
        traceback.print_exc()
        # Provide info on how the function should have been called instead
        print(f"\nFunction usage:\n{_get_function_info(_FUNCTIONS[name])}")
        sys.exit(1)
