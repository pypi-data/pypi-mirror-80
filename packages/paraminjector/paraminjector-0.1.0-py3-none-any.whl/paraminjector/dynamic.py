import inspect
from typing import Any, Callable, Type, TypeVar, Union, Dict, Tuple
from typing import Awaitable

from paraminjector.typed_callable import TypedCallable
from paraminjector._injector import analyze_signature


def call_with_args(
    func: Callable,
    available_args: Dict[Type, object],
    fixed_pos_args: Tuple = None,
    follow_wrapped: bool = True,  # TODO: implement
) -> Any:
    kwargs = analyze_signature(
        func=TypedCallable(func),
        available_args=available_args,
        fixed_pos_args=fixed_pos_args,
        follow_wrapped=follow_wrapped,
    )

    if fixed_pos_args:
        return func(*fixed_pos_args, **kwargs)
    else:
        return func(**kwargs)


async def call_with_args_maybe_async(
    func: Callable,
    available_args: Dict[Type, object],
    fixed_pos_args: Tuple = None,
    follow_wrapped: bool = True,  # TODO: implement
) -> Any:
    result = call_with_args(
        func, available_args, fixed_pos_args=fixed_pos_args, follow_wrapped=follow_wrapped
    )
    if inspect.isawaitable(result):
        return await result
    return result


async def call_with_args_async(
    func: Callable[[], Awaitable],
    available_args: Dict[Type, object],
    fixed_pos_args: Tuple = None,
    follow_wrapped: bool = True,  # TODO: implement
) -> Any:
    return await call_with_args(
        func, available_args, fixed_pos_args=fixed_pos_args, follow_wrapped=follow_wrapped
    )
