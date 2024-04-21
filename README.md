# Pymand

Define functions as commands that can be run in the CLI.

## How to use

Define a context and functions to be registered in the `Pymand` instance.

```py
context = {
  "arg1": "val1",
  "arg2": "val2",
}


def function1(arg1):
  pass


def function2(arg2):
  pass


pymand = Pymand(
  context,
  function1,
  function2,
  # ...
)

pymand.run()
```

Key value pairs defined in context are used as default values in functions.

For example, in the function `function1`, the argument `arg1` is given the value in context, `"val1"`.
