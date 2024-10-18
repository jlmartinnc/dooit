from typing import TYPE_CHECKING, Callable
from textual.widgets import Static


from ...events.events import ModeChanged

if TYPE_CHECKING:  # pragma: no cover
    from .bar_switcher import BarSwitcher
    from dooit.ui.tui import Dooit
    from dooit.ui.api.dooit_api import DooitAPI


class BarBase(Static):
    DEFAULT_CSS = """
    BarBase {
        height: 1;
        width: 100%;
    }
    """

    focused: bool = True

    def __init__(self, callback: Callable = lambda: None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.callback = callback

    @property
    def app(self) -> "Dooit":
        from dooit.ui.tui import Dooit

        app = super().app
        assert isinstance(app, Dooit)
        return app

    @property
    def api(self) -> "DooitAPI": # pragma: no cover
        return self.app.api

    @property
    def switcher(self) -> "BarSwitcher":
        from .bar_switcher import BarSwitcher

        parent = self.parent
        assert isinstance(parent, BarSwitcher)
        return parent

    def perform_action(self, cancel: bool):
        raise NotImplementedError  # pragma: no cover

    def close(self):
        self.switcher.current = "status_bar"
        self.remove()

    def dismiss(self, cancel: bool, close: bool = True):
        self.perform_action(cancel)
        self.app.post_message(ModeChanged("NORMAL"))
        if close:
            self.close()

    async def handle_keypress(self, key: str) -> None: # pragma: no cover
        return
