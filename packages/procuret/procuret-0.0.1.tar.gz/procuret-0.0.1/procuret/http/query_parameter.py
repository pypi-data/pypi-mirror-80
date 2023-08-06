"""
Procuret Python
QueryParameter Module
author: hugh@blinkybeach.com
"""
from typing import Any, TypeVar, Type, List

T = TypeVar('T', bound='QueryParameter')


class QueryParameter:
    """A single URL parameter, e.g. beep=boop"""
    def __init__(
        self,
        key: str,
        value: Any
    ) -> None:

        assert isinstance(key, str)
        str(value)  # provoke error early
        self._key = key
        self._value = value

        return

    key = property(lambda s: s._key)

    def __str__(self) -> str:
        return self._key + '=' + str(self._value)

    @classmethod
    def remove_targets_with(
        cls: Type[T],
        key: str,
        targets: List[T]
    ) -> List[T]:

        retained_targets: List[QueryParameter] = list()
        for target in targets:
            if target._key == key:
                continue
            retained_targets.append(target)
            continue

        return targets
