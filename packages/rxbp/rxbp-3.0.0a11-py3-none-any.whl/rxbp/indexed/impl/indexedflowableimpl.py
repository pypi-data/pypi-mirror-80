from dataclasses import replace

from dataclass_abc import dataclass_abc

from rxbp.indexed.indexedflowable import IndexedFlowable
from rxbp.indexed.init.initindexedsharedflowable import init_indexed_shared_flowable
from rxbp.indexed.mixins.indexedflowablemixin import IndexedFlowableMixin
from rxbp.typing import ValueType


@dataclass_abc
class IndexedFlowableImpl(IndexedFlowable[ValueType]):
    underlying: IndexedFlowableMixin

    def _copy(
            self,
            is_shared: bool = None,
            **kwargs,
    ):
        if is_shared:
            return init_indexed_shared_flowable(**kwargs)

        return replace(self, **kwargs)
