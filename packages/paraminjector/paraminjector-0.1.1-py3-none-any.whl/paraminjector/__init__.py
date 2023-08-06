from importlib.metadata import version

__version__ = version(__name__)


from .static import ParamInjector
from .dynamic import call_with_args_async, call_with_args, call_with_args_maybe_async
from .typed_callable import TypedCallable

__all__ = [
    # "ParamInjector",
    "call_with_args_async",
    "call_with_args",
    "call_with_args_maybe_async",
    "TypedCallable",
]
