from collections import defaultdict
from typing import Callable, Dict, List, TypeVar

TItem = TypeVar("TItem")
TKey = TypeVar("TKey")

def group_by(items: List[TItem], by: Callable[[TItem], TKey]) -> Dict[TKey, List[TItem]]:
    result: Dict[TKey, List[TItem]] = defaultdict(list)

    for item in items:
        result[by(item)].append(item)

    return result