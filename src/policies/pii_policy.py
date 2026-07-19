import json
import re
from typing import Any

from models.guard_decision import GuardAction, GuardDecision
from models.guard_request import GuardRequest
from policies.base_policy import BasePolicy


class PIIPolicy(BasePolicy):
    """Blocks tool calls whose arguments appear to contain sensitive data."""

    PATTERNS = {
        "email_address": re.compile(
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
        ),
        "social_security_number": re.compile(
            r"\b\d{3}-\d{2}-\d{4}\b"
        ),
        "credit_card_number": re.compile(
            r"\b(?:\d[ -]*?){13,19}\b"
        ),
        "api_key": re.compile(
            r"(?i)\b(?:api[_-]?key|secret[_-]?key|access[_-]?token)"
            r"\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{12,}"
        ),
        "private_key": re.compile(
            r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"
        ),
    }

    def evaluate(
        self,
        request: GuardRequest,
    ) -> GuardDecision | None:
        searchable_text = self._serialize_arguments(request.arguments)

        for pii_type, pattern in self.PATTERNS.items():
            if pattern.search(searchable_text):
                return GuardDecision(
                    action=GuardAction.BLOCK,
                    reason=(
                        f"Possible {pii_type.replace('_', ' ')} detected in "
                        f"arguments for tool '{request.tool_name}'."
                    ),
                    policy="pii_policy",
                )

        return None

    @staticmethod
    def _serialize_arguments(arguments: Any) -> str:
        try:
            return json.dumps(
                arguments,
                default=str,
                sort_keys=True,
            )
        except (TypeError, ValueError):
            return str(arguments)
