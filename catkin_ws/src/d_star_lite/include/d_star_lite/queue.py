# -*- coding: utf-8 -*-
"""
Parts of the code in this file may be modified and/or original code by Peter Norvig.

Original Software License Agreement

Copyright © 1998-2002 by Peter Norvig.
Permission is granted to anyone to use this software, in source or object code form, on any computer system, and to modify, compile, decompile, run, and redistribute it to anyone else, subject to the following restrictions:

The author makes no warranty of any kind, either expressed or implied, about the suitability of this software for any purpose.
The author accepts no liability of any kind for damages or other consequences of the use of this software, even if they arise from defects in the software.
The origin of this software must not be misrepresented, either by explicit claim or by omission.
Altered versions must be plainly marked as such, and must not be misrepresented as being the original software. Altered versions may be distributed in packages under other licenses (such as the GNU license).
If you find this software useful, it would be nice if you let me (peter@norvig.com) know about it, and nicer still if you send me modifications that you are willing to share. However, you are not required to do so.

http://www.norvig.com/license.html
"""

import bisect
from copy import deepcopy


class PriorityQueue():
    """A queue in which the minimum (or maximum) element (as determined by f and
    order) is returned first. If order is min, the item with minimum f(x) is
    returned first; if order is max, then it is the item with maximum f(x).
    Also supports dict-like lookup.

    PriorityQueue(order, f): Queue in sorted order (default min-first).

    Supports the following methods and functions:
        q.insert(item)  -- add an item to the queue
        q.extend(items) -- equivalent to: for item in items: q.insert(item)
        q.pop()         -- return the top item from the queue
        len(q)          -- number of items in q (also q.__len())
        item in q       -- does q contain item?
    """
    def __init__(self, order=min, f=lambda x: x):
        update(self, A=[], order=order, f=f)

    def __eq__(self, other):
        return self.A == other.A

    def __repr__(self):
        return "PriorityQueue<(key, item): %s>" % str(self.A)
    __str__ = __repr__

    def extend(self, items):
        for item in items:
            self.insert(item)

    def copy(self):
        return deepcopy(self)

    def insert(self, item):
        bisect.insort(self.A, (self.f(item), item))

    def pop(self):
        if not self.A:
            raise IndexError("queue is empty; can't pop")
        if self.order == min:
            return self.A.pop(0)[1]
        else:
            return self.A.pop()[1]

    def remove(self, item):
        "removes all instances of item from the queue"
        self.__delitem__(item)

    def top_key(self):
        "Get the key corresponding to the next item to be popped"
        if not self.A:
            raise IndexError("queue is empty; no top key")
        next_item = self.A[0][1]
        return self.f(next_item)

    def is_empty(self):
        if not self.A:
            return True
        else:
            return False

    def __len__(self):
        return len(self.A)

    def __contains__(self, item):
        return some(lambda (_, x): x == item, self.A)

    def __getitem__(self, key):
        for _, item in self.A:
            if item == key:
                return item

    def __delitem__(self, key):
        for i, (value, item) in enumerate(self.A):
            if item == key:
                self.A.pop(i)
                return

def update(x, **entries):
    """Update a dict; or an object with slots; according to entries.
    >>> update({'a': 1}, a=10, b=20)
    {'a': 10, 'b': 20}
    >>> update(Struct(a=1), a=10, b=20)
    Struct(a=10, b=20)
    """
    if isinstance(x, dict):
        x.update(entries)
    else:
        x.__dict__.update(entries)
    return x

def some(predicate, seq):
    """If some element x of seq satisfies predicate(x), return predicate(x).
    >>> some(callable, [min, 3])
    1
    >>> some(callable, [2, 3])
    0
    """
    for x in seq:
        px = predicate(x)
        if px: return px
    return False
