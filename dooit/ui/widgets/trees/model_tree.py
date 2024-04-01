from dooit.api.model import Model
from collections import defaultdict
from .base_tree import BaseTree


class ModelTree(BaseTree):
    DEFAULT_CSS = """
    ModelTree {
        height: 100%;
        width: 100%;
    }
    """

    def __init__(self, model: Model) -> None:
        tree = self.__class__.__name__
        super().__init__(id=f"{tree}_{model.uuid}")
        self._model = model
        self.expaned = defaultdict(bool)

    @property
    def model(self) -> Model:
        return self._model

    def force_refresh(self) -> None:
        raise NotImplementedError

    def on_mount(self):
        self.force_refresh()

    def key_p(self):
        if self.highlighted is not None:
            self.notify(str(self.highlighted))
            self.toggle_expand()
