from container.application_container import (
    ApplicationContainer,
    build_application_container,
)


container = build_application_container()


__all__ = [
    "ApplicationContainer",
    "build_application_container",
    "container",
]
