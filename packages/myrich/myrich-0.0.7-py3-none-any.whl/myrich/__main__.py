#!/usr/bin/env python
# coding: utf-8

from argparse import ArgumentParser, REMAINDER
import os
import sys

if __package__ is None and not hasattr(sys, "frozen"):
    # direct call of __main__.py
    path = os.path.realpath(os.path.abspath(__file__))
    sys.path.insert(0, os.path.dirname(os.path.dirname(path)))

from rich.console import Console
from rich.markdown import Markdown
from rich.syntax import Syntax

from myrich import __package_name__, __version__
from myrich.vendor.delegator import run


console = Console()


def print_error(message):
    console.print("ERROR: " + message, style="bold red")


def print_warning(message):
    console.print(message, style="bold yellow")


def print_output(message, soft_wrap=False, page=False):
    "Using Pydoc if page"

    if page:
        import pydoc
        import io

        console.file = io.StringIO()
        console.print(message)
        pydoc.pager(console.file.getvalue())  # type: ignore
    else:
        console.print(message, soft_wrap=soft_wrap)


def is_command_args(cmd):
    return len(cmd.split(" ", 1)) == 2


def change_directory(path_str):
    "Change to path directory"
    cwd = None
    try:
        os.chdir(path_str)
        cwd = os.getcwd()
    except FileNotFoundError as err:
        path_str = os.getcwd()
        print_error(err)

    return cwd or path_str


def render2markdown(file_string, options={}):
    "Render file or string to Markdown"
    file_string = file_string.strip()

    if os.path.isfile(file_string):
        with open(file_string) as md:
            markdown = md.read()
    else:
        markdown = file_string

    page = options.get("page", False)
    justify = options.get("justify", False)
    code_theme = options.get("code_theme", "monokai")
    hyperlinks = options.get("hyperlinks", False)
    inline_code_lexer = options.get("inline_code_lexer")

    print_output(
        Markdown(
            markdown,
            justify="full" if justify else "left",
            code_theme=code_theme,
            hyperlinks=hyperlinks,
            inline_code_lexer=inline_code_lexer,
        ),
        page,
    )


def render2syntax(file_path, options={}):
    "Render syntax to the console with Rich"
    line_numbers = options.get("line_numbers", False)
    word_wrap = options.get("word_wrap", False)
    soft_wrap = options.get("soft_wrap", False)
    code_theme = options.get("code_theme", "monokai")
    background_color = options.get("background_color")

    syntax = Syntax.from_path(
        file_path,
        line_numbers=line_numbers,
        word_wrap=word_wrap,
        theme=code_theme,
        background_color=background_color,
    )

    print_output(syntax, soft_wrap=soft_wrap)


def run_command(commands, path_str):
    "Run commands in the path using subprocess"
    c = run(commands, cwd=path_str)
    print_output(c.out)

    if c.err:
        print_error(c.err)

    return c


# TODO: Add Columns, Logging Handler


def start_shell(cwd=None):
    "Start Shell-like"
    if not cwd:
        cwd = os.getcwd()

    while True:
        try:
            prompt = (
                "[cyan](rich)[/cyan] [yellow]" + cwd + "[/yellow]" + "%s" % "> "
                if os.name == "nt"
                else "$ "
            )
            command_line = console.input(prompt)

            if command_line and command_line.strip() == "exit":
                break
            # TODO: Parse subcommands options
            if is_command_args(command_line):
                if command_line[:2] == "cd":
                    cwd = change_directory(command_line[3:])
                    continue
                elif command_line[:8] == "markdown":
                    render2markdown(command_line[9:])
                    continue
                elif command_line[:6] == "syntax":
                    render2syntax(command_line[7:])
                    continue
            elif command_line[:6] == "myrich":
                print_warning("No action taken to avoid nested environments")
                continue

            _ = run_command(command_line, cwd)
        except KeyboardInterrupt:
            print_error("Interrupted by user")
            sys.exit(1)

    print_output("Bye :waving_hand:")


def main():
    # Argument Parser
    my_parser = ArgumentParser(
        prog=__package_name__,
        allow_abbrev=False,
        usage="%(prog)s [options] commands",
        description="Shell-like using Rich for render rich text content",
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
            render2syntax(args.path, vars(args))
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
