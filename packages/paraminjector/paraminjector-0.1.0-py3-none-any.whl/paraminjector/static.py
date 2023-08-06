import inspect
from typing import (
    Any,
    Callable,
    ClassVar,
    Generic,
    Optional,
    Tuple,
    Type,
    TypeVar,
    Union,
    AbstractSet,
    Hashable,
    Iterable,
    Iterator,
    Mapping,
    MutableMapping,
    MutableSequence,
    MutableSet,
    Sequence,
    AsyncIterator,
    AsyncIterable,
    Coroutine,
    Collection,
    AsyncGenerator,
    Deque,
    Dict,
    List,
    Set,
    FrozenSet,
    NamedTuple,
    Generator,
    cast,
    overload,
    TYPE_CHECKING,
)
from pprint import pprint

from typing import Callable, Type, Union, Dict, cast

from paraminjector.typed_callable import TypedCallable
from paraminjector._injector import _find_contravariant_argument, analyze_signature


class ParamInjector:
    available_references: Dict[Type, object]

    def __init__(
        self,
        func: Callable,
        available_args: Dict[Type, object],
        fixed_pos_arg_types: Dict[Type, object] = None,
        follow_wrapped: bool = True,
    ):
        """
        If you expect the callback to change during runtime, use dynamic injections instead.

        Args:
            func: The user-defined function to call. It must not change during runtime.
            available_args:
        """
        self.func = func
        analyze_signature(
            TypedCallable(func),
            available_args=available_args,
            fixed_pos_args=fixed_pos_args,
            follow_wrapped=follow_wrapped,
        )
        self.available_references = available_args

    def map_kwargs(self, callback: Callable, follow_wrapped: bool = True) -> Dict[str, object]:
        sig = inspect.signature(callback, follow_wrapped=follow_wrapped)

        # pprint(sig.parameters)

        result: Dict[str, object] = dict()

        for param_name, parameter in sig.parameters.items():
            print(parameter.default)
            parameter = cast(inspect.Parameter, parameter)

            # TODO: add try catch for "TypeError: Subscripted generics cannot be used with class and instance checks"
            possible_targets = [
                a for a in self.available_references if issubclass(a, parameter.annotation)
            ]

            if len(possible_targets) > 1:
                raise ValueError(
                    f"More than one possible target for parameter {parameter.__repr__()}:"
                    f" {possible_targets}"
                )
            elif not possible_targets:
                if parameter.default is not inspect._empty:
                    # parameter has default value but we cannot determine it
                    continue
                else:
                    raise ValueError(
                        f"Parameter {parameter.__repr__()} cannot be filled. TODO: more info"
                    )

            target = possible_targets[0]

            param = _find_contravariant_argument(self.available_references, parameter.annotation)
            print(param)

            if param is not inspect._empty:
                result[param_name] = param
            else:
                if parameter.default == inspect.Parameter.empty:
                    raise ValueError(
                        "Non-default parameter in callback signature whose type blabla"
                    )
                else:
                    pass  # ignore

            pprint(result)

        return result

    def call(self, *fixed_args, **fixed_kwargs):
        pass

    async def call_async(self, *fixed_args, **fixed_kwargs):
        pass

        # if not used_arg_types:
        #     raise ValueError(
        #         f"No type hints specified for callback '{callback.__name__}'."
        #     )
        #
        # pyrogram_types = {Message, CallbackQuery, InlineQuery, Poll, User}
        #
        # if Update in used_arg_types:
        #     found_arg_type = Update
        # else:
        #     found_arg_type = None
        #
        # for arg in used_arg_types:
        #     if issubclass(arg, Client):
        #         pass
        #     if any((t for t in pyrogram_types if issubclass(arg, t))):
        #         if found_arg_type is not None:
        #             raise ValueError(
        #                 "More than one possible update type found, cannot determine the kind of callback."
        #             )
        #         else:
        #             found_arg_type = arg
        #
        # if not found_arg_type:
        #     raise ValueError(
        #         f"No matching callback type found for signature {type_hints}"
        #     )
        #
        # kwargs = dict(callback=callback, filters=filters)
        # if issubclass(found_arg_type, Message):
        #     return MessageHandler(**kwargs)
        # elif issubclass(found_arg_type, CallbackQuery):
        #     return CallbackQueryHandler(**kwargs)
        # elif issubclass(found_arg_type, InlineQuery):
        #     return InlineQueryHandler(**kwargs)
        # elif issubclass(found_arg_type, Poll):
        #     return PollHandler(**kwargs)
        # elif issubclass(found_arg_type, User):
        #     return UserStatusHandler(**kwargs)
        # elif found_arg_type is Update:
        #     return RawUpdateHandler(callback=callback)
        # else:
        #     raise ValueError(
        #         f"Could not find a matching Pyrogram callback class for type {found_arg_type}."
        #     )
