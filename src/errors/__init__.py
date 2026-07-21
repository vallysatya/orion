"""Orion error model — typed failures by subsystem."""

from .orion_error import OrionError
from .runtime_errors import OrionRuntimeError
from .guard_errors import (
    GuardError,
    GuardEvaluationError,
)
from .memory_errors import (
    OrionMemoryError,
    MemoryOperationError,
)
from .tool_errors import ToolExecutionError
from .integration_errors import (
    IntegrationError,
    GitHubIntegrationError,
)
from .configuration_errors import ConfigurationError

__all__ = [
    "OrionError",
    "OrionRuntimeError",
    "GuardError",
    "GuardEvaluationError",
    "OrionMemoryError",
    "MemoryOperationError",
    "ToolExecutionError",
    "IntegrationError",
    "GitHubIntegrationError",
    "ConfigurationError",
]
