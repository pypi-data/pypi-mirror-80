from abc import abstractmethod
from typing import (Callable,
                    Iterable,
                    Iterator,
                    Optional)

from reprit.base import generate_repr

from dendroid.hints import (Order,
                            Value)
from .abcs import (NIL,
                   MutableSet,
                   Tree)


class BaseSet(MutableSet[Value]):
    __slots__ = 'tree',

    def __init__(self, tree: Tree) -> None:
        self.tree = tree

    __repr__ = generate_repr(__init__)

    def __iter__(self) -> Iterator[Value]:
        for node in self.tree:
            yield node.value

    def __len__(self) -> int:
        return len(self.tree)

    def __reversed__(self) -> Iterator[Value]:
        for node in reversed(self.tree):
            yield node.value

    def clear(self) -> None:
        self.tree.clear()

    def max(self) -> Value:
        return self.tree.max().value

    def min(self) -> Value:
        return self.tree.min().value

    @abstractmethod
    def next(self, value: Value) -> Value:
        """Returns first value greater than the given one."""

    def popmax(self) -> Value:
        return self.tree.popmax().value

    def popmin(self) -> Value:
        return self.tree.popmin().value

    pop = popmin

    @abstractmethod
    def prev(self, value: Value) -> Value:
        """Returns last value lesser than the given one."""


class Set(BaseSet[Value]):
    def __contains__(self, value: Value) -> bool:
        return self.tree.find(value) is not NIL

    def __copy__(self) -> 'Set[Value]':
        return Set(self.tree.__copy__())

    def add(self, value: Value) -> None:
        self.tree.insert(value, value)

    def discard(self, value: Value) -> None:
        node = self.tree.find(value)
        if node is NIL:
            return
        self.tree.remove(node)

    def from_iterable(self, iterable: Iterable[Value]) -> 'Set[Value]':
        return Set(self.tree.from_components(iterable))

    def next(self, value: Value) -> Value:
        return self.tree.next(value).value

    def prev(self, value: Value) -> Value:
        return self.tree.prev(value).value

    def remove(self, value: Value) -> None:
        self.tree.pop(value)


class KeyedSet(BaseSet[Value]):
    __slots__ = 'key',

    def __init__(self, tree: Tree, key: Order) -> None:
        super().__init__(tree)
        self.key = key

    __repr__ = generate_repr(__init__)

    def __contains__(self, value: Value) -> bool:
        return bool(self.tree) and self.tree.find(self.key(value)) is not NIL

    def __copy__(self) -> 'KeyedSet[Value]':
        return KeyedSet(self.tree.__copy__(), self.key)

    def add(self, value: Value) -> None:
        self.tree.insert(self.key(value), value)

    def discard(self, value: Value) -> None:
        node = self.tree.find(self.key(value))
        if node is NIL:
            return
        self.tree.remove(node)

    def from_iterable(self, iterable: Iterable[Value]) -> 'KeyedSet[Value]':
        values = list(iterable)
        return KeyedSet(self.tree.from_components(map(self.key, values),
                                                  values),
                        self.key)

    def next(self, value: Value) -> Value:
        return self.tree.next(self.key(value)).value

    def prev(self, value: Value) -> Value:
        return self.tree.prev(self.key(value)).value

    def remove(self, value: Value) -> None:
        self.tree.pop(self.key(value))


def set_constructor(tree_constructor: Callable[..., Tree],
                    *values: Value,
                    key: Optional[Order] = None) -> BaseSet[Value]:
    return (Set(tree_constructor(values))
            if key is None
            else KeyedSet(tree_constructor([key(value) for value in values],
                                           values),
                          key))
