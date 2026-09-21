"""Cron must not deliver a tool-loop guardrail halt as a successful job response."""

import pytest

from cron.scheduler import _final_response_from_result


class _AIAgent:
    @staticmethod
    def _format_turn_completion_explanation(*_args, **_kwargs):
        return ""


def test_tool_guardrail_halt_marks_cron_run_failed():
    result = {
        "final_response": (
            "I stopped retrying because I kept running tool_call 8 times "
            "without making progress."
        ),
        "completed": True,
        "failed": False,
        "turn_exit_reason": "guardrail_halt",
        "guardrail": {
            "action": "halt",
            "code": "repeated_exact_failure_halt",
            "tool_name": "tool_call",
            "count": 8,
        },
        "messages": [],
    }

    with pytest.raises(RuntimeError, match="tool guardrail halted tool_call"):
        _final_response_from_result(result, "job1", "Hourly health", _AIAgent)
