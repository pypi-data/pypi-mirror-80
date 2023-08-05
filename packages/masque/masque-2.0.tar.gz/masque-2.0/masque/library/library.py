from typing import Dict, Callable, TypeVar, Generic, TYPE_CHECKING
from functools import lru_cache

if TYPE_CHECKING:
    from ..pattern import Pattern


Key = TypeVar('Key')
Value = TypeVar('Value')


class DeferredDict(dict, Generic[Key, Value]):
    """
    This is a modified `dict` which is used to defer loading/generating
     values until they are accessed.

    ```
    bignum = my_slow_function()         # slow function call, would like to defer this
    numbers = Library()
    numbers['big'] = my_slow_function        # no slow function call here
    assert(bignum == numbers['big'])    # first access is slow (function called)
    assert(bignum == numbers['big'])    # second access is fast (result is cached)
    ```

    The `set_const` method is provided for convenience;
     `numbers['a'] = lambda: 10` is equivalent to `numbers.set_const('a', 10)`.
    """
    def __init__(self, *args, **kwargs):
        dict.__init__(self)
        self.update(*args, **kwargs)

    def __setitem__(self, key: Key, value: Callable[[], Value]):
        cached_fn = lru_cache(maxsize=1)(value)
        dict.__setitem__(self, key, cached_fn)

    def __getitem__(self, key: Key) -> Value:
        return dict.__getitem__(self, key)()

    def update(self, *args, **kwargs):
        for k, v in dict(*args, **kwargs).items():
            self[k] = v

    def __repr__(self) -> str:
        return '<Library with keys ' + repr(set(self.keys())) + '>'

    def set_const(self, key: Key, value: Value):
        """
        Convenience function to avoid having to manually wrap
         constant values into callables.
        """
        self[key] = lambda: value


class LibraryLockedError(Exception):
    pass


D = TypeVar('D', bound='Library')


class Library(DeferredDict[str, 'Pattern']):
    """
    This class is usually used to create a device library by mapping names to
     functions which generate or load the relevant `Pattern` object as-needed.
    """
    modlocked: bool
    ''' When `True`, disallows modifying any existing entries '''

    def __init__(self, *args, **kwargs):
        DeferredDict.__init__(self, *args, **kwargs)
        self.modlocked = False

    def __setitem__(self, key: str, value: Callable[[], 'Pattern']):
        if self.modlocked and key in self:
            raise LibraryLockedError('Attempted to modify locked library')
        DeferredDict.__setitem__(self, key, value)

    def modlock(self: D) -> D:
        """
        Dis-allow modifying existing entries
        """
        self.modlocked = True
        return self

    def modunlock(self: D) -> D:
        """
        Re-allow modifying existing entries
        """
        self.modlocked = False
        return self

    def set_modlocked(self: D, value: bool) -> D:
        self.modlocked = value
        return self


@dataclass
class PatternGenerator:
    gen: Callable[[], Pattern]
    source: Any     # If equal, can autoload


r"""

Let's say we want to load a GDS of RootCell
                                       \
                                     MidCell
                                         \
                                      LeafCell
  MidCell and LeafCell might already be loaded in the library, present
  but not loaded, or not present?
Do we
    - load the whole gds and cache MidCell and LeafCell if they're present?
        + Replace with cached versions if already loaded, or replace the cached ones?
        + Maybe check file dates or something?
    - load RootCell, then load and replace MidCell/LeafCell from their own locations?
    - need partial load of files?

    # Traverse and add a hierarchy?
    #   Add a filter for names which aren't added
    # Merge two libraries?
"""
