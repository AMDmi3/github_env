#!/usr/bin/env python3
#
# Copyright (c) 2022 Dmitry Marakasov <amdmi3@amdmi3.ru>
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from __future__ import annotations

import argparse
import os
import sys
from typing import TextIO

__version__ = '0.0.1'


class IncorrectInvocation(RuntimeError):
    pass


def parse_arguments(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        formatter_class=lambda prog: argparse.HelpFormatter(prog, width=78),
        description="""
        Modify GITHUB_ENV file in a flexible way.
        """
    )

    parser.add_argument(
        '-f',
        '--file',
        type=str,
        metavar='PATH',
        default=os.environ.get('GITHUB_ENV'),
        help='Path to variables file (by default take from $GITHUB_ENV)'
    )
    parser.add_argument(
        '-i',
        '--if',
        type=str,
        metavar='COND',
        dest='cond',
        help='Apply condition: only run if argument is "true"'
    )
    parser.add_argument(
        '-v',
        '--verbose',
        action='store_true',
        help='Be verbose, show changes done to env file'
    )
    parser.add_argument(
        'modifications',
        metavar='EXPR',
        nargs='+',
        default=[],
        help="""
        Variable modification expressions:
        VAR=value to add or rewrite a variable,
        VAR+=value to append a value to a variable,
        VAR++=value to prepend a value to a variable,
        VAR-=value to remove a value from a variable,
        !VAR to undefine a variable.
        """
    )

    args = parser.parse_args(argv)

    if args.file is None:
        raise IncorrectInvocation('Path to GITHUB_ENV file not defined')

    return args


class Vars:
    _vars: dict[str, str]
    _orig_vars: dict[str, str]

    def __init__(self) -> None:
        self._vars = {}
        self._orig_vars = {}

    def load(self, path: str) -> None:
        with open(path) as fd:
            for line in fd:
                line = line.strip()
                kv = line.split('=', 1)
                if len(kv) == 2:
                    self._vars[kv[0]] = kv[1]
                else:
                    print(f'WARNING: stray line in GITHUB_ENV file: "{line}"', file=sys.stderr)

        self._orig_vars = {key: value for key, value in self._vars.items()}

    def dump(self, path: str) -> None:
        with open(path, 'w') as fd:
            for key, value in sorted(self._vars.items()):
                print(f'{key}={value}', file=fd)

    def set(self, key: str, value: str) -> None:
        self._vars[key] = value

    def append(self, key: str, value: str) -> None:
        if key in self._vars and self._vars[key]:
            self._vars[key] = f'{self._vars[key]} {value}'
        else:
            self._vars[key] = value

    def prepend(self, key: str, value: str) -> None:
        if key in self._vars and self._vars[key]:
            self._vars[key] = f'{value} {self._vars[key]}'
        else:
            self._vars[key] = value

    def remove_var(self, key: str) -> None:
        del self._vars[key]

    def remove_value(self, key: str, removed: str) -> None:
        if key in self._vars and self._vars[key]:
            values = self._vars[key].split()
            self._vars[key] = ' '.join(
                value for value in values if value != removed
            )

    def print_diff(self, f: TextIO) -> None:
        keys = set(self._vars.keys()) | set(self._orig_vars.keys())

        for key in sorted(keys):
            if self._vars.get(key) != self._orig_vars.get(key):
                if key in self._orig_vars:
                    print(f'-{key}={self._orig_vars[key]}', file=f)
                if key in self._vars:
                    print(f'+{key}={self._vars[key]}', file=f)


def apply_modification(variables: Vars, mod: str) -> None:
    if mod.startswith('!') and '=' not in mod:
        variables.remove_var(mod[1:])
        return

    if '=' not in mod:
        raise IncorrectInvocation(f'Unexpected modification expression "{mod}"')

    key, value = mod.split('=', 1)

    if key.endswith('-'):
        variables.remove_value(key[:-1], value)
    elif key.endswith('++'):
        variables.prepend(key[:-2], value)
    elif key.endswith('+'):
        variables.append(key[:-1], value)
    else:
        variables.set(key, value)


def main(argv: list[str] | None = None) -> None:
    args = parse_arguments(argv)

    if args.cond is not None and args.cond != 'true':
        return

    variables = Vars()

    if os.path.exists(args.file):
        variables.load(args.file)

    for mod in args.modifications:
        apply_modification(variables, mod)

    if args.verbose:
        variables.print_diff(sys.stderr)

    variables.dump(args.file)


if __name__ == '__main__':
    try:
        main()
    except IncorrectInvocation as e:
        print(f'FATAL: {e}', file=sys.stderr)
