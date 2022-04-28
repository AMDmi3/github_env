[![CI](https://github.com/AMDmi3/github_env/actions/workflows/ci.yml/badge.svg)](https://github.com/AMDmi3/github_env/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/AMDmi3/github_env/branch/master/graph/badge.svg?token=87aZsxlja2)](https://codecov.io/gh/AMDmi3/github_env)
[![Github commits (since latest release)](https://img.shields.io/github/commits-since/AMDmi3/github_env/latest.svg)](https://github.com/AMDmi3/github_env)

# github_env

When using GitHub actions, [environment
variables](https://docs.github.com/en/actions/learn-github-actions/environment-variables)
are often used. In complex scenarios, variables are stored in
[`$GITHUB_ENV`](https://docs.github.com/en/actions/using-workflows/workflow-commands-for-github-actions#setting-an-environment-variable)
file. However, this file does not allow appending variables which
is often needed. This small script simplifies this task.

## Usage

```shell
github_env.py FOO=bar    # add or rewrite a variable 
github_env.py FOO+=bar   # append to a variable
github_env.py FOO++=bar  # prepend to a variable
github_env.py FOO-=bar   # remove value from a variable
github_env.py !FOO       # undefine a variable

# explicitly pass path to env file, but you don't need it
# because it's retrieved from $GITHUB_ENV automatically
github_env.py --file env

# conditional execution to use with GitHub actions expressions
github_env.py --if ${{ matrix.compiler == 'clang' }} CFLAGS+=-Werror
```

## Example

It's pretty common to have a logic like this which tunes environment
based on settings from matrix:

```yaml
jobs:
  build:
    stragegy:
      matrix:
        include
          - { cxx: g++, coverage: true }
          - { cxx: clang++, coverage: false }
    steps:
      ...
      - name: Set up environment
        run: |
          echo 'CXX=${{ matrix.cxx }}' >> $GITHUB_ENV
          echo 'CXXFLAGS=-Wall -Wextra -pedantic' >> $GITHUB_ENV
      - name: Set up environment (compiler-specific flags)
        if: ${{ matrix.cxx == 'clang++' }}
        run: echo "CXXFLAGS=$CXXFLAGS -Wno-self-assign-overloaded" >> $GITHUB_ENV
      - name: Set up environment (coverage)
        if: ${{ matrix.coverage }}
        run: |
          echo "CXXFLAGS=$CXXFLAGS --coverage" >> $GITHUB_ENV
          echo "LDFLAGS=$LDFLAGS --coverage" >> $GITHUB_ENV
```

And here's how it's simplified with `github_env.py` script:

```yaml
      - name: Set up environment
        run: |
          curl -s https://raw.githubusercontent.com/AMDmi3/github_env/master/github_env.py > e; chmod 755 e
          ./e 'CXX=${{ matrix.cxx }}'
          ./e 'CXXFLAGS=-Wall -Wextra -pedantic'
          ./e --if ${{ matrix.cxx == 'clang++' }} 'CXXFLAGS+=-Wno-self-assign-overloaded'
          ./e --if ${{ matrix.coverage }} 'CXXFLAGS+=--coverage' 'LDFLAGS+=--coverage'
```

## Author

- [Dmitry Marakasov](https://github.com/AMDmi3) <amdmi3@amdmi3.ru>

## License

MIT, see [COPYING](COPYING).
