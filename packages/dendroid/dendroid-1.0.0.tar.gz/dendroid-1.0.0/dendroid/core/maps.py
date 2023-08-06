from collections import abc
from typing import (Callable,
                    Generic,
                    Iterable,
                    Iterator,
                    Optional,
                    Union)

from reprit.base import generate_repr

from dendroid.hints import (Item,
                            Key,
                            Value)
from .abcs import (NIL,
                   Tree)
from .utils import split_items
from .views import (ItemsView,
                    KeysView,
                    ValuesView)


@abc.MutableMapping.register
class Map(Generic[Key, Value]):
    __slots__ = 'tree',

    def __init__(self, tree: Tree) -> None:
        self.tree = tree

    __repr__ = generate_repr(__init__)

    def __contains__(self, key: Key) -> bool:
        return self.tree.find(key) is not NIL

    def __copy__(self) -> 'Map[Key, Value]':
        return Map(self.tree.__copy__())

    def __delitem__(self, key: Key) -> None:
        self.tree.pop(key)

    def __eq__(self, other: 'Map[Key, Value]') -> bool:
        return (self.keys() == other.keys()
                and all(other[key] == value
                        for key, value in self.items())
                if isinstance(other, Map)
                else NotImplemented)

    def __getitem__(self, key: Key) -> Value:
        node = self.tree.find(key)
        if node is NIL:
            raise KeyError(key)
        return node.value

    def __iter__(self) -> Iterator[Key]:
        for node in self.tree:
            yield node.key

    def __len__(self) -> int:
        return len(self.tree)

    def __reversed__(self) -> Iterator[Key]:
        for node in reversed(self.tree):
            yield node.key

    def __setitem__(self, key: Key, value: Value) -> None:
        self.tree.insert(key, value).value = value

    def get(self,
            key: Key,
            default: Optional[Value] = None) -> Optional[Value]:
        node = self.tree.find(key)
        return default if node is NIL else node.value

    def clear(self) -> None:
        self.tree.clear()

    def items(self) -> ItemsView[Key, Value]:
        return ItemsView(self.tree)

    def keys(self) -> KeysView[Key]:
        return KeysView(self.tree)

    def max(self) -> Value:
        return self.tree.max().value

    def maxitem(self) -> Value:
        return self.tree.max().item

    def min(self) -> Value:
        return self.tree.min().value

    def minitem(self) -> Item:
        return self.tree.min().item

    def next(self, key: Key) -> Value:
        return self.tree.next(key).value

    def nextitem(self, key: Key) -> Value:
        return self.tree.next(key).item

    __sentinel = object()

    def pop(self, key: Key, default: Value = __sentinel) -> Value:
        try:
            node = self.tree.pop(key)
        except KeyError:
            if default is self.__sentinel:
                raise
            return default
        else:
            return node.value

    def popmax(self) -> Value:
        return self.tree.popmax().value

    def popmaxitem(self) -> Value:
        return self.tree.popmax().item

    def popmin(self) -> Value:
        return self.tree.popmin().value

    def popminitem(self) -> Item:
        return self.tree.popmin().item

    popitem = popminitem

    def prev(self, key: Key) -> Value:
        return self.tree.prev(key).value

    def previtem(self, key: Key) -> Value:
        return self.tree.prev(key).item

    def setdefault(self,
                   key: Key,
                   default: Optional[Value] = None) -> Optional[Value]:
        node = self.tree.find(key)
        return (self.tree.insert(key, default)
                if node is NIL
                else node).value

    def update(self,
               other: Union['Map[Key, Value]', Iterable[Item]] = ()) -> None:
        for key, value in (other.items() if isinstance(other, Map) else other):
            self[key] = value

    def values(self) -> ValuesView[Value]:
        return ValuesView(self.tree)


def map_constructor(tree_constructor
                    : Callable[[Iterable[Key], Iterable[Value]], Tree],
                    *items: Item) -> Map[Key, Value]:
    return Map(tree_constructor(*split_items(items)))
