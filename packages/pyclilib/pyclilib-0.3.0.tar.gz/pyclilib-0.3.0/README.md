# pyclilib
Python Library to create CLI tools using Subject-Verb-Object pattern
```
# [my-namespace] not yet implemented
my-cmd [my-namespace] my-action my-resource [pos_args] [--options]
```

# Quickstart 1: CLI without Namespaces
1. `pip install pyclilib`
2. Create a hello world CLI
```python
import clilib

@clilib.decorator.resource
class MyResource():
    @clilib.decorator.get
    def get(self):
        print "Hello world"

clilib.init("mycli")
clilib.run("mycli")
```
3. Run your program
```
$ python example.py get my-resource
Hello world
```

# Quickstart 2: CLI with Namespaces (not implemented yet)
1. `pip install clilib`
2. Create the runner, `example.py`
```python
import clilib

clilib.init("mycli")
clilib.run("mycli")
```
3. Namespaces are sub-packages of an expected local `namespace` package
```
$ mkdir -p namespace namespace/my-namespace
$ touch namespace/__init__.py namespace/my-namespace/__init__.py
```
```python
# namespace/my-namespace/__init__.py
import clilib

@clilib.decorator.resource
class MyResource():
    @clilib.decorator.verb
    def get(self):
        print("Hello World")
```
4. Run your program
```
$ python example.py my-namespace get my-resource
Hello World
```

# Notes
- You can either have `cli namespace action resource` **OR** `cli action resource` in the future

# Roadmap
- [ ] Global Config -- [Potential](https://docs.python.org/3.2/library/argparse.html#the-namespace-object)
- [ ] Namespace
- [ ] Conditional Args
- [ ] CLI without resource ex. `git init`

# TODO
- How to make log level configurable?
Since decorators run during "compile"(?) time, setting the level through `clilib.run("foo", logging.DEBUG)` will set the level after the decorators do their thing.
Same story with `clilib._log_level = logging.DEBUG`
