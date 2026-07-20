import json

from observability.exporters.base_exporter import BaseExporter
from observability.trace import Trace


class JsonExporter(BaseExporter):

    def export(
        self,
        trace: Trace,
    ) -> None:

        data = []

        for event in trace.events:

            data.append(
                {
                    "timestamp": event.timestamp.isoformat(),
                    "component": event.component,
                    "event": event.event,
                    "metadata": event.metadata,
                }
            )

        print(
            json.dumps(
                data,
                indent=4,
            )
        )
