#!/usr/bin/env python
# Shell-like using Rich for render rich text content
# coding: utf-8

__package_name__ = "myrich"
__description__ = "Shell-like using Rich for render rich text content"
from ._version import version_info, __version__

from rich import get_console


__all__ = [
    "__description__",
    "__package_name__",
    "version_info",
    "__version__",
    "get_console",
]
