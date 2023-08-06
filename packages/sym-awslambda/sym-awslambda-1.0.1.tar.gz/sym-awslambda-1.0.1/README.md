# sym-awslambda-py

Python modules to simplify Sym lambda integrations.

## Dispatch Configuration

Sym provides a standard dispatch handler that you can use to automatically route Sym messages to the right handler.

First import the dispatch function in your main `handler.py` file:

```python
from sym.awslambda.dispatch import dispatch
```

Then in your Terraform lambda declaration, set `handler.dispatch` as your `handler` value:

```terraform
resource "aws_lambda_function" "sym" {

  ...

  handler = "handler.dispatch"

  ...
}
```

## sym_action decorator

The Sym dispatcher will delegate incoming messages to the appropriate handler based on the `sym_action` decorator:

```python
from sym.awslambda.decorators import sym_action


@sym_action("approve")
def approve(approval, context):

    print("Target reason:", approval.request.meta.reason)
    ....
```

## Message types

The messages that sym actions receive are defined as protobufs in the [Sym Types](https://github.com/symopsio/types/) repo.
