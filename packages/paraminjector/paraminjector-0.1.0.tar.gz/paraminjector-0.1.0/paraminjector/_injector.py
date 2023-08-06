import inspect
import traceback

import itertools
from inspect import _empty
from typing import Any, Tuple, Type, Union, Dict, cast

from paraminjector.typed_callable import TypedCallable
from paraminjector.exceptions import FunctionSignatureInvalid


def analyze_signature(
    func: TypedCallable,
    available_args: Dict[Type, object],
    fixed_pos_args: Tuple[Any] = None,
    follow_wrapped: bool = True,
) -> Dict[str, object]:
    if fixed_pos_args is not None:
        params_to_inject = get_detected_params(func, available_args, fixed_pos_args)
    else:
        params_to_inject = func.signature.parameters

    result: Dict[str, object] = dict()

    for param_name, parameter in params_to_inject.items():
        parameter = cast(inspect.Parameter, parameter)

        # account for union type
        annotated_types = (
            type_args
            if (type_args := getattr(parameter.annotation, "__args__", None))
            else parameter.annotation
        )

        # TODO: add try catch for "TypeError: Subscripted generics cannot be used with class and instance checks"
        possible_targets = [a for a in available_args if issubclass(a, annotated_types)]

        if len(possible_targets) > 1:

            # TODO: this is gonna happen

            raise ValueError(
                f"Found more than one possible target for parameter {parameter.__repr__()}:"
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

        param = _find_contravariant_argument(available_args, target)

        if param is not inspect._empty:
            result[param_name] = param
        else:
            if parameter.default == inspect.Parameter.empty:
                raise ValueError("Non-default parameter in callback signature whose type blabla")
            else:
                pass  # ignore

    return result


def get_detected_params(
    func: TypedCallable, available_args: Dict[Type, object], fixed_pos_args: Tuple[Any]
) -> Dict[str, inspect.Parameter]:

    n_fixed = len(fixed_pos_args)
    n_declared = len(func.signature.parameters)

    if n_fixed > n_declared:
        raise FunctionSignatureInvalid(func, f"Expected at least {n_fixed} parameters")

    param_kv_pairs: Dict[int, Tuple[str, inspect.Parameter]] = {
        n: kv for n, kv in enumerate(func.signature.parameters.items())
    }

    # If it has a type annotation, make sure we match that with the arguments we're going to inject.
    for n, pos_arg in enumerate(fixed_pos_args):
        name, param = param_kv_pairs[n]

        # TODO: How can pos_arg be None? Write test!

        try:
            if param.annotation and not issubclass(type(pos_arg), param.annotation):
                raise FunctionSignatureInvalid(
                    func,
                    f"Argument {n} to {func.name} should always be a supertype of "
                    f"{type(pos_arg)}.",
                )
        except TypeError as e:
            traceback.print_exc()

    try:
        return {
            k: v
            for k, v in itertools.islice(func.signature.parameters.items(), n_fixed, n_declared)
        }
    except KeyError:
        raise FunctionSignatureInvalid("lala TODO")


def _find_contravariant_argument(
    refs: Dict[Type, object], param_type: Type
) -> Union[_empty, object]:
    exact_match = refs.get(param_type, None)
    if exact_match is not None:
        # Exact type match
        return exact_match

    covariant_match = next((p for p in refs if issubclass(p, param_type)), _empty)
    return refs[covariant_match]
