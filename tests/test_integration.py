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

import os
from pathlib import Path

import pytest

from github_env import IncorrectInvocation, main


def _read_lines(path: Path) -> list[str]:
    with open(path, 'r') as fd:
        return list(map(str.strip, fd))


@pytest.fixture
def envfile(tmp_path: Path) -> Path:
    return tmp_path / 'env'


@pytest.mark.skipif('GITHUB_ENV' in os.environ, reason='GITHUB_ENV must not be defined')
def test_no_path():
    with pytest.raises(IncorrectInvocation):
        main(['FOO=bar'])


def test_set(envfile):
    main(['-f', str(envfile), 'FOO=1', 'BAR=2'])
    assert _read_lines(envfile) == ['BAR=2', 'FOO=1']
    main(['-f', str(envfile), 'BAZ=3'])
    assert _read_lines(envfile) == ['BAR=2', 'BAZ=3', 'FOO=1']


def test_rewrite(envfile):
    main(['-f', str(envfile), 'FOO=1', 'FOO=2'])
    assert _read_lines(envfile) == ['FOO=2']
    main(['-f', str(envfile), 'FOO=3'])
    assert _read_lines(envfile) == ['FOO=3']


def test_append(envfile):
    main(['-f', str(envfile), 'FOO=1', 'FOO+=2'])
    assert _read_lines(envfile) == ['FOO=1 2']
    main(['-f', str(envfile), 'FOO+=3'])
    assert _read_lines(envfile) == ['FOO=1 2 3']


def test_prepend(envfile):
    main(['-f', str(envfile), 'FOO=1', 'FOO++=2'])
    assert _read_lines(envfile) == ['FOO=2 1']
    main(['-f', str(envfile), 'FOO++=3'])
    assert _read_lines(envfile) == ['FOO=3 2 1']


def test_remove_var(envfile):
    main(['-f', str(envfile), 'FOO=1', 'BAR=2', '!FOO'])
    assert _read_lines(envfile) == ['BAR=2']
    main(['-f', str(envfile), '!BAR'])
    assert _read_lines(envfile) == []


def test_remove_value(envfile):
    main(['-f', str(envfile), 'FOO=1 2 3', 'FOO-=1'])
    assert _read_lines(envfile) == ['FOO=2 3']
    main(['-f', str(envfile), 'FOO-=2'])
    assert _read_lines(envfile) == ['FOO=3']


def test_if(envfile):
    main(['-f', str(envfile), 'FOO=1'])
    main(['-f', str(envfile), '--if', 'true', 'FOO=2'])
    assert _read_lines(envfile) == ['FOO=2']
    main(['-f', str(envfile), '--if', 'false', 'FOO=3'])
    assert _read_lines(envfile) == ['FOO=2']
