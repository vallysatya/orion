import json
import re
from typing import Any

from models.guard_decision import GuardAction, GuardDecision
from models.guard_request import GuardRequest
from policies.base_policy import BasePolicy


class PromptInjectionPolicy(BasePolicy):
    """Detects common prompt-injection language in tool arguments."""

    SUSPICIOUS_PATTERNS = {
        "instruction_override": re.compile(
            r"(?i)\bignore\s+(?:all\s+)?(?:previous|prior|above)"
            r"\s+instructions?\b"
        ),
        "system_prompt_request": re.compile(
            r"(?i)\b(?:reveal|show|print|expose)\b.{0,40}"
            r"\b(?:system prompt|hidden instructions?|developer message)\b"
        ),
        "secret_exfiltration": re.compile(
            r"(?i)\b(?:send|upload|forward|post|transmit)\b.{0,60}"
            r"\b(?:secret|credential|password|token|api key|private key)\b"
        ),
        "security_bypass": re.compile(
            r"(?i)\b(?:bypass|disable|circumvent|override)\b.{0,40}"
            r"\b(?:security|guardrail|policy|approval|authorization)\b"
        ),
        "role_manipulation": re.compile(
            r"(?i)\b(?:you are now|act as|pretend to be)\b.{0,40}"
            r"\b(?:administrator|admin|system|developer)\b"
        ),
    }

    def evaluate(
        self,
        request: GuardRequest,
    ) -> GuardDecision | None:
        searchable_text = self._serialize_arguments(request.arguments)

        for injection_type, pattern in self.SUSPICIOUS_PATTERNS.items():
            if pattern.search(searchable_text):
                return GuardDecision(
                    action=GuardAction.BLOCK,
                    reason=(
                        "Possible prompt injection detected "
                        f"({injection_type.replace('_', ' ')}) in arguments "
                        f"for tool '{request.tool_name}'."
                    ),
                    policy="prompt_injection_policy",
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
