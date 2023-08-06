from paraminjector.typed_callable import TypedCallable


class FunctionSignatureInvalid(Exception):
    def __init__(self, func: TypedCallable, cause: str) -> None:
        super().__init__(f"{cause.rstrip('.')},\ncaused by {func.description}.")
