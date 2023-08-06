# First-Python-Package
A simple pyhton package to say messages



Build the solution

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