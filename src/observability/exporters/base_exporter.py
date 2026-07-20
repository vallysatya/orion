from abc import ABC, abstractmethod

from observability.trace import Trace


class BaseExporter(ABC):
    """
    Base interface for exporting traces.
    """

    @abstractmethod
    def export(
        self,
        trace: Trace,
    ) -> None:
        """
        Export a trace.
        """
        raise NotImplementedError
