"""
Functions for generating code badges
"""

__all__ = [
    "print_pylint_badge",
]

import pkgutil
from collections import OrderedDict
import sys

try:
    from pylint.lint import Run
    import enchant
    from lyncs_utils import redirect_stdout
except ModuleNotFoundError:
    raise ModuleNotFoundError("Please install lyncs_setuptools[pylint]")

from .setup import get_kwargs
from . import __path__


def print_pylint_badge(do_exit=True, spelling=True):
    "Runs the pylint executable and prints the badge with the score"

    if "." in sys.argv:
        sys.argv.remove(".")
        sys.argv += get_kwargs()["packages"]

    if spelling and "spelling" not in sys.argv and enchant.dict_exists("en"):
        sys.argv += [
            "--enable",
            "spelling",
            "--spelling-dict",
            "en",
            "--spelling-ignore-words",
            ",".join(ignore_words),
        ]

    with redirect_stdout(sys.stderr):
        results = Run(sys.argv[1:], do_exit=False)

    score = results.linter.stats["global_note"]
    colors = OrderedDict(
        {
            9.95: "brightgreen",
            8.95: "green",
            7.95: "yellowgreen",
            6.95: "yellow",
            5.95: "orange",
            0.00: "red",
        }
    )

    color = "brightgreen"
    for val, color in colors.items():
        if score >= val:
            break

    print(
        "[![pylint](https://img.shields.io/badge/pylint%%20score-%.1f%%2F10-%s?logo=python&logoColor=white)](http://pylint.pycqa.org/)"
        % (score, color)
    )

    if not do_exit:
        return
    if results.linter.config.exit_zero:
        sys.exit(0)
    if score > results.linter.config.fail_under:
        sys.exit(0)
    sys.exit(results.linter.msg_status)


ignore_words = sorted(
    [
        "anymore",
        "args",
        "argv",
        "bool",
        "cartesian",
        "cls",
        "config",
        "coord",
        "coords",
        "cwd",
        "dict",
        "dtype",
        "etc",
        "func",
        "i",
        "idxs",
        "int",
        "iterable",
        "itertools",
        "kwargs",
        "lyncs",
        "metaclass",
        "mpi",
        "mpirun",
        "params",
        "procs",
        "stdout",
        "str",
        "sys",
        "tuple",
        "url",
        "utils",
        "vals",
        "varnames",
    ]
    + list(mod.name for mod in pkgutil.iter_modules(None))
)
