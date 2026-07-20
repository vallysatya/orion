from observability.exporters.base_exporter import BaseExporter
from observability.trace import Trace


class ConsoleExporter(BaseExporter):

    def export(
        self,
        trace: Trace,
    ) -> None:

        print()

        print("=" * 60)
        print("ORION TRACE")
        print("=" * 60)

        for event in trace.events:

            print(
                f"[{event.timestamp}] "
                f"{event.component} -> "
                f"{event.event}"
            )

            if event.metadata:

                for key, value in event.metadata.items():

                    print(
                        f"    {key}: {value}"
                    )

        print("=" * 60)
