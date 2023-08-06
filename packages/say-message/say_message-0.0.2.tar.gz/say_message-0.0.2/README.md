# First-Python-Package
A simple pyhton package to say messages

# Basic Usage

```sh
from say_message.say_message import say_message

if __name__ == "__main__":
    say_message('Hi')
```

# Build the solution

```sh
python -m pip install --user --upgrade setuptools wheel
python setup.py sdist bdist_wheel
python -m pip install --user --upgrade twine
python -m twine upload dist/*
```

# Run test

```sh
python -m unittest
```