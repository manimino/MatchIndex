from typing import Callable, Union, Dict, Any, Iterable, Optional

from cykhash import Int64Set

from hashindex.constants import TUPLE_SIZE_MAX, SET_SIZE_MIN
from hashindex.init_helpers import compute_mutable_dict
from hashindex.utils import get_field


class MutableFieldIndex:
    """
    Stores the possible values of this field in a collection of buckets.
    Several values may be allocated to the same bucket for space efficiency reasons.
    """

    def __init__(
        self,
        field: Union[Callable, str],
        obj_map: Dict[int, Any],
        objs: Optional[Iterable[Any]] = None,
    ):
        self.field = field
        self.obj_map = obj_map
        if objs:
            self.d = compute_mutable_dict(objs, field)
        else:
            self.d = dict()

    def get_obj_ids(self, val: Any) -> Int64Set:
        ids = self.d.get(val, Int64Set())
        if isinstance(ids, tuple):
            return Int64Set(ids)
        return ids

    def add(self, ptr: int, obj: Any):
        val = get_field(obj, self.field)
        if val in self.d:
            if len(self.d[val]) == TUPLE_SIZE_MAX:
                self.d[val] = Int64Set(self.d[val])
                self.d[val].add(ptr)
            elif isinstance(self.d[val], tuple):
                self.d[val] = tuple(list(self.d[val]) + [ptr])
            else:
                self.d[val].add(ptr)
        else:
            self.d[val] = (ptr,)

    def remove(self, ptr: int, obj: Any):
        """
        Remove a single object from the index.

        If a val slot ever gets empty, remove it.
        """
        val = get_field(obj, self.field)
        obj_ids = self.d[val]
        if ptr in obj_ids:
            if isinstance(obj_ids, tuple):
                self.d[val] = tuple(obj_id for obj_id in obj_ids if obj_id != ptr)
            else:
                self.d[val].remove(ptr)
                if len(self.d[val]) < SET_SIZE_MIN:
                    self.d[val] = tuple(self.d[val])
            if len(self.d[val]) == 0:
                del self.d[val]
