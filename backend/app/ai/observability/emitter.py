from collections.abc import Sequence

from app.ai.observability.contracts import ExecutionEvent
from app.ai.observability.listeners import AIObservabilityListener


class AIObservabilityEmitter:
    """
    Central dispatcher for AI execution lifecycle events.

    The emitter owns no state. It simply dispatches immutable execution
    events to the configured listeners.
    """

    def __init__(
        self,
        listeners: Sequence[AIObservabilityListener],
    ) -> None:
        self.listeners = list(
            listeners,
        )

    def emit(
        self,
        event: ExecutionEvent,
    ) -> None:
        """
        Dispatch an event to all registered listeners.
        """
        for listener in self.listeners:
            listener.handle(
                event,
            )
