#!/usr/bin/env python3

from os import path

from setuptools import find_packages, setup


def get_version():
    with open(path.join(path.abspath(path.dirname(__file__)), 'github_env.py')) as source:
        for line in source:
            if line.startswith('__version__'):
                return line.strip().split(' = ')[-1].strip("'")

    raise RuntimeError('Cannot determine package version from package source')


def get_long_description():
    try:
        return open(path.join(here, 'README.md')).read()
    except:
        return None


setup(
    name='github_env',
    version=get_version(),
    description='Simple tool to manage $GITHUB_ENV in GitHub actions',
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
    author='Dmitry Marakasov',
    author_email='amdmi3@amdmi3.ru',
    url='https://github.com/AMDmi3/github_env',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: Code Generators',
    ],
    python_requires='>=3.8',
    scripts=['github_env.py'],
)
