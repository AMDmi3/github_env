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

## Synopsis

First, let's convert basic variable setting to the script. Your
step which sets the environment probably looks like this:
```yaml
echo 'CXX=${{ matrix.cxx }}' >> $GITHUB_ENV
echo 'CXXFLAGS=-Wall -Wextra -pedantic' >> $GITHUB_ENV
```

Here's how it looks like with `github_env`:
```yaml
curl -s https://raw.githubusercontent.com/AMDmi3/github_env/master/github_env.py > e; chmod 755 e
./e 'CXX=${{ matrix.cxx }}'
./e 'CXXFLAGS=-Wall -Wextra -pedantic"'
```

One extra line for getting the script, but cleaner syntax already.

Now you can use additional features.

### Append variables

```yaml
./e 'CXXFLAGS+=-Werror'  # CXXFLAGS=-Wall -Wextra -pedantic -Werror
```

### Prepend variables

```yaml
./e 'CXXFLAGS++=-Werror'  # CXXFLAGS=-Werror -Wall -Wextra -pedantic
```

### Reset variables

```yaml
./e '!CXXFLAGS'  # CXXFLAGS is removed from env
```

### Remove values from variables

```yaml
./e 'CXXFLAGS-=-Wall'  # CXXFLAGS=-Wextra -pedantic
```

## Author

- [Dmitry Marakasov](https://github.com/AMDmi3) <amdmi3@amdmi3.ru>

## License

MIT, see [COPYING](COPYING).
