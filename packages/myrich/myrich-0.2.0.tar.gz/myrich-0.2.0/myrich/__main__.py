#!/usr/bin/env python
# coding: utf-8

from argparse import ArgumentParser, REMAINDER
import os
import sys

from rich.color import ColorParseError

if __package__ is None and not hasattr(sys, "frozen"):
    # direct call of __main__.py
    path = os.path.realpath(os.path.abspath(__file__))
    sys.path.insert(0, os.path.dirname(os.path.dirname(path)))

from myrich import __package_name__, __description__, __version__
from myrich.shell import (
    console,
    print_error,
    render2markdown,
    render2syntax,
    run_command,
    start_shell,
)


def main():
    # Argument Parser
    my_parser = ArgumentParser(
        prog=__package_name__,
        allow_abbrev=False,
        usage="%(prog)s [options] commands",
        description=__description__,
    )

    # Add arguments
    my_parser.version = __version__
    my_parser.add_argument(
        "commands",
        action="store",
        nargs=REMAINDER,
        default=[],
        help="Commands to be executed",
    )
    my_parser.add_argument(
        "-c",
        "--force-color",
        dest="force_color",
        action="store_true",
        default=None,
        help="force color for non-terminals",
    )
    my_parser.add_argument(
        "-M",
        "--markdown",
        action="store_true",
        default=None,
        help="Render Markdown to the console with Rich",
    )
    my_parser.add_argument(
        "-w",
        "--width",
        type=int,
        dest="width",
        default=None,
        help="width of output (default will auto-detect)",
    )
    my_parser.add_argument(
        "-i",
        "--inline-code-lexer",
        dest="inline_code_lexer",
        default=None,
        help="inline_code_lexer",
    )
    my_parser.add_argument(
        "-t",
        "--code-theme",
        dest="code_theme",
        default="monokai",
        help="pygments code theme",
    )
    my_parser.add_argument(
        "-y",
        "--hyperlinks",
        dest="hyperlinks",
        action="store_true",
        help="enable hyperlinks",
    )
    my_parser.add_argument(
        "-j",
        "--justify",
        dest="justify",
        action="store_true",
        help="enable full text justify",
    )
    my_parser.add_argument(
        "-p",
        "--page",
        dest="page",
        action="store_true",
        help="use pager to scroll output",
    )
    my_parser.add_argument(
        "-S",
        "--syntax",
        action="store_true",
        default=None,
        help="Render Syntax from file",
    )
    my_parser.add_argument("--path", metavar="PATH", default=None, help="path to file")
    my_parser.add_argument(
        "-l",
        "--line-numbers",
        dest="line_numbers",
        action="store_true",
        help="render line numbers",
    )
    my_parser.add_argument(
        "-r",
        "--wrap",
        dest="word_wrap",
        action="store_true",
        default=False,
        help="word wrap long lines",
    )
    my_parser.add_argument(
        "-s",
        "--soft-wrap",
        action="store_true",
        dest="soft_wrap",
        default=False,
        help="enable soft wrapping mode",
    )
    my_parser.add_argument(
        "-b",
        "--background-color",
        dest="background_color",
        default=None,
        help="Overide background color",
    )
    my_parser.add_argument("-V", "--version", action="version")

    args = my_parser.parse_args()
    cwd = os.getcwd()

    if args.width:
        console._width = args.width

    if args.force_color:
        console._force_terminal = args.force_color

    if args.syntax:
        if args.path:
            try:
                render2syntax(args.path, vars(args))
            except ColorParseError as err:
                print_error(str(err))
        else:
            print_error("Syntax require --path to fille")
            sys.exit(1)
    elif args.markdown:
        render2markdown(" ".join(args.commands), vars(args))
    elif args.commands:
        c = run_command(args.commands, cwd)
        retcode = c.return_code
    else:
        start_shell(cwd)


if __name__ == "__main__":
    main()
