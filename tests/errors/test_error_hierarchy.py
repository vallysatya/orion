import pytest

from errors import (
    ConfigurationError,
    GitHubIntegrationError,
    GuardError,
    GuardEvaluationError,
    IntegrationError,
    OrionMemoryError,
    MemoryOperationError,
    OrionError,
    OrionRuntimeError,
    ToolExecutionError,
)


@pytest.mark.parametrize(
    "error_type",
    [
        OrionRuntimeError,
        GuardError,
        GuardEvaluationError,
        OrionMemoryError,
        MemoryOperationError,
        ToolExecutionError,
        IntegrationError,
        GitHubIntegrationError,
        ConfigurationError,
    ],
)
def test_all_orion_errors_inherit_from_orion_error(error_type):
    error = error_type("test failure")

    assert isinstance(error, OrionError)
    assert isinstance(error, Exception)


def test_guard_evaluation_error_inherits_from_guard_error():
    error = GuardEvaluationError("guard failed")

    assert isinstance(error, GuardError)


def test_memory_operation_error_inherits_from_orion_memory_error():
    error = MemoryOperationError("memory failed")

    assert isinstance(error, OrionMemoryError)


def test_github_error_inherits_from_integration_error():
    error = GitHubIntegrationError("GitHub failed")

    assert isinstance(error, IntegrationError)


def test_error_message_is_preserved():
    error = ToolExecutionError("tool execution failed")

    assert str(error) == "tool execution failed"


def test_orion_error_can_be_caught_generically():
    with pytest.raises(OrionError):
        raise GitHubIntegrationError("GitHub unavailable")


def test_orion_memory_error_is_not_builtin_memory_error():
    error = OrionMemoryError("session hydrate failed")

    assert isinstance(error, OrionError)
    assert not isinstance(error, MemoryError)
