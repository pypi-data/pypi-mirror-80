from typing import Any, List, Union

from spokestack.context import SpeechContext


class SpeechPipeline:
    def __init__(self) -> None:
        self._context = SpeechContext()
        self._stages: List[Any] = []
        self._is_running = False
        self._is_managed = False

    def __call__(self) -> None:
        for stage in self._stages:
            stage()

    @property
    def context(self) -> SpeechContext:
        return self._context

    def activate(self) -> None:
        self._context.is_active = True

    def deactivate(self) -> None:
        self._context.is_active = False

    def start(self) -> None:
        pass

    def stop(self) -> None:
        pass

    def run(self) -> None:
        pass

    def dispatch(self) -> None:
        pass

    def add(self, components: Union[List, Any]) -> None:
        if isinstance(components, list):
            self._stages += components
        else:
            self._stages.append(components)

    @property
    def is_running(self) -> bool:
        return self._is_running
