# MyRich
[![PyPI version](https://badge.fury.io/py/myrich.svg)](https://badge.fury.io/py/myrich)
![Tests](https://github.com/oleksis/myrich/workflows/Tests/badge.svg)

Shell-like using [Rich](https://rich.readthedocs.io/en/latest/) for render rich text content

## Installing
Install with pip
```bash
$ pip install myrich
```

## Use
Execute the command `myrich`
```bash
$ myrich
(rich) /home/user $ 
```

You use the internal command `markdown` for render a Markdown file
```bash
$ myrich
(rich) /home/user $ markdown -y README.md
```

You use the internal command `syntax` for render a file using syntax highlighting
```bash
$ myrich
(rich) /home/user $ syntax -l code.py
```

### Using the Console
You can render the ouput the any command over rich terminal content
```bash
$ myrich
(rich) /home/user $ cat code.py
```

You can run several commands through pipes
```bash
$ myrich
(rich) /home/user $ python -m myrich -S -l --path code.py | cat
```

### Using Emoji
You can render the ouput with Emojis
```bash
$ myrich
(rich) /home/user $ echo :smiley:
```

# License
[MIT](LICENSE)
