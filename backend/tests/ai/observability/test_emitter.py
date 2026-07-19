from unittest.mock import MagicMock

from app.ai.observability.contracts import (
    ExecutionEvent,
    ExecutionStatus,
)
from app.ai.observability.emitter import AIObservabilityEmitter
from app.ai.observability.listeners import AIObservabilityListener


def build_event() -> ExecutionEvent:
    return ExecutionEvent(
        execution_id="execution-123",
        provider="openai",
        model="gpt-5",
        prompt_version="v1",
        operation="resume_generation",
        status=ExecutionStatus.STARTED,
    )


def test_emit_dispatches_to_single_listener():
    event = build_event()

    listener = MagicMock(
        spec=AIObservabilityListener,
    )

    emitter = AIObservabilityEmitter(
        listeners=[
            listener,
        ],
    )

    emitter.emit(event)

    listener.handle.assert_called_once_with(
        event,
    )


def test_emit_dispatches_to_multiple_listeners():
    event = build_event()

    listener_one = MagicMock(
        spec=AIObservabilityListener,
    )

    listener_two = MagicMock(
        spec=AIObservabilityListener,
    )

    listener_three = MagicMock(
        spec=AIObservabilityListener,
    )

    emitter = AIObservabilityEmitter(
        listeners=[
            listener_one,
            listener_two,
            listener_three,
        ],
    )

    emitter.emit(event)

    listener_one.handle.assert_called_once_with(
        event,
    )

    listener_two.handle.assert_called_once_with(
        event,
    )

    listener_three.handle.assert_called_once_with(
        event,
    )


def test_emit_with_no_listeners_does_not_fail():
    event = build_event()

    emitter = AIObservabilityEmitter(
        listeners=[],
    )

    emitter.emit(event)


def test_emit_preserves_listener_order():
    event = build_event()

    calls: list[str] = []

    class FakeListener(AIObservabilityListener):
        def __init__(
            self,
            name: str,
        ) -> None:
            self.name = name

        def handle(
            self,
            event: ExecutionEvent,
        ) -> None:
            calls.append(
                self.name,
            )

    emitter = AIObservabilityEmitter(
        listeners=[
            FakeListener("A"),
            FakeListener("B"),
            FakeListener("C"),
        ],
    )

    emitter.emit(event)

    assert calls == [
        "A",
        "B",
        "C",
    ]
