# built-in
import inspect
from asyncio import iscoroutinefunction
from contextlib import suppress
from functools import update_wrapper
from typing import Callable, Generic, TypeVar

# external
import vaa

# app
from .._exceptions import ContractError
from .._state import state
from .._types import ExceptionType


#: We use this type in many other subclasses of `Base` decorator.
_CallableType = TypeVar('_CallableType', bound=Callable)


class Base(Generic[_CallableType]):
    exception: ExceptionType = ContractError
    function: _CallableType  # pytype: disable=not-supported-yet

    def __init__(self, validator, *, message: str = None,
                 exception: ExceptionType = None):
        """
        Step 1. Set contract (validator).
        """
        self.validator = self._make_validator(validator, message=message)
        if exception:
            self.exception = exception
        if message:
            self.exception = self.exception(message)    # type: ignore

    @staticmethod
    def _make_validator(validator, message: str = None):
        if validator is None:
            return None
        # implicitly wrap in vaa all external validators
        with suppress(TypeError):
            return vaa.wrap(validator, simple=False)

        # implicitly wrap in vaa.simple only funcs with one `_` argument.
        if inspect.isfunction(validator):
            params = inspect.signature(validator).parameters
            if set(params) == {'_'}:
                return vaa.simple(validator, error=message)

        return validator

    def validate(self, *args, **kwargs) -> None:
        """
        Step 4. Process contract (validator)
        """

        if hasattr(self.validator, 'is_valid'):
            self._vaa_validation(*args, **kwargs)
        else:
            self._simple_validation(*args, **kwargs)

    def _vaa_validation(self, *args, **kwargs) -> None:
        params = kwargs.copy()

        # if it is a decorator for a function, convert positional args into named ones.
        if hasattr(self, 'function'):
            # detect original function
            function = self.function
            while hasattr(function, '__wrapped__'):
                function = function.__wrapped__     # type: ignore
            # assign *args to real names
            kwargs.pop('result', None)
            params.update(inspect.getcallargs(function, *args, **kwargs))
            # drop args-kwargs, we already put them on the right places
            for bad_name in ('args', 'kwargs'):
                if bad_name in params and bad_name not in kwargs:
                    del params[bad_name]

        # validate
        validator = self.validator(data=params)
        if validator.is_valid():
            return

        # if no errors returned, raise the default exception
        errors = validator.errors
        if not errors:
            raise self.exception

        # Flatten single error without field to one simple str message.
        # This is for better readability of simple validators.
        if type(errors) is list:  # pragma: no cover
            if type(errors[0]) is vaa.Error:
                if len(errors) == 1:
                    if errors[0].field is None:
                        errors = errors[0].message

        # raise errors
        if isinstance(self.exception, Exception):
            raise type(self.exception)(errors)
        raise self.exception(errors)

    def _simple_validation(self, *args, **kwargs) -> None:
        validation_result = self.validator(*args, **kwargs)
        # is invalid (validator returns error message)
        if isinstance(validation_result, str):
            if isinstance(self.exception, Exception):
                raise type(self.exception)(validation_result)
            raise self.exception(validation_result)
        # is valid (truely result)
        if validation_result:
            return
        # is invalid (falsy result)
        raise self.exception

    @property
    def enabled(self) -> bool:
        return state.debug

    def __call__(self, function: _CallableType) -> _CallableType:
        """
        Step 2. Return wrapped function.
        """
        self.function = function

        def wrapped(*args, **kwargs):
            if self.enabled:
                return self.patched_function(*args, **kwargs)
            else:
                return function(*args, **kwargs)

        async def async_wrapped(*args, **kwargs):
            if self.enabled:
                return await self.async_patched_function(*args, **kwargs)
            else:
                return await function(*args, **kwargs)

        def wrapped_generator(*args, **kwargs):
            if self.enabled:
                yield from self.patched_generator(*args, **kwargs)
            else:
                yield from function(*args, **kwargs)

        if iscoroutinefunction(function):
            new_callable = update_wrapper(async_wrapped, function)
        elif inspect.isgeneratorfunction(function):
            new_callable = update_wrapper(wrapped_generator, function)
        else:
            new_callable = update_wrapper(wrapped, function)
        return new_callable  # type: ignore

    def patched_function(self, *args, **kwargs):
        """
        Step 3. Wrapped function calling.
        """
        raise NotImplementedError

    async def async_patched_function(self, *args, **kwargs):
        """
        Step 3. Wrapped function calling.
        """
        raise NotImplementedError

    def patched_generator(self, *args, **kwargs):
        """
        Step 3. Wrapped function calling.
        """
        raise NotImplementedError
