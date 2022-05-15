from rich.console import RenderableType
from rich.text import Text, TextType
from textual import events
from textual.widgets import TreeControl, TreeNode, NodeID
from textual.events import Key

from ...ui.widgets.entry import Entry


class TreeEdit(TreeControl):
    """
    A Class that allows editing while displaying trees
    """

    def __init__(self, label: TextType) -> None:
        super().__init__(label, None)
        self._tree.hide_root = True
        self.root._tree.expanded = True

        self.highlighted = NodeID(0)
        self.selected = None

    async def on_mouse_move(self, event: events.MouseMove) -> None:
        self.highlighted = event.style.meta.get("tree_node")
        return await super().on_mouse_move(event)

    async def reset(self) -> None:
        """
        Turns off both highlight and editing
        """
        await self.clear_select()
        self.highlighted = NodeID(0)

    async def clear_select(self) -> None:
        """
        Leave editing mode
        """

        if self.selected:
            self.nodes[self.selected].data._has_focus = False

        self.selected = None
        self.refresh()

    async def select(self, id: NodeID | None = None) -> None:
        """
        Selects the node to be edited
        """
        await self.clear_select()
        self.highlighted = id
        self.selected = id
        if self.selected:
            self.nodes[self.selected].data._has_focus = True

        self.hover_node = None  # Not to block due to still mouse pointer
        self.refresh()

    async def remove(self, id: NodeID):
        if next_node := self.nodes[id].next_node:
            if next_node.id != id:
                self.move_highlight_down()
        elif prev_node := self.nodes[id].previous_node:
            if prev_node.id != id:
                self.move_highlight_up()

        parent = self.nodes[id].parent or self.root
        for index, child in enumerate(parent.children):
            if child.id == id:
                parent.children.pop(index)
                parent.tree.children.pop(index)

        self.refresh()

    async def handle_click(self) -> None:
        # Yeah I know this is weird. BUT IT WORKS DAMMIT!
        await self.handle_keypress(Key(self, "enter"))

    def move_highlight_down(self):
        if self.highlighted:
            self.highlight(
                (self.nodes[self.highlighted].next_node or self.root.children[0]).id
            )
        else:
            self.highlight(self.root.children[0].id)

    def move_highlight_up(self):
        if self.highlighted:
            prev_node = self.nodes[self.highlighted].previous_node
            if prev_node == self.root:
                prev_node = self.root.children[-1]

            # SAFETY: The node will never be None because it does not even reach root
            self.highlight(prev_node.id)
        else:
            self.highlight(self.root.children[0].id)

    def highlight(self, id: NodeID = NodeID(0)) -> None:
        """
        Highlights the node
        """

        self.highlighted = id
        self.refresh()

    async def handle_shortcut(self, key: str):
        match key:
            case "m":
                await self.select(self.highlighted)

            case "a":
                node = self.nodes[self.highlighted]
                await node.add("", Entry())
                await node.expand()
                self.highlight(node.children[-1].id)
                await self.select(self.highlighted)

            case "A":
                if parent := self.nodes[self.highlighted].parent:
                    self.highlight(parent.id)
                    await self.handle_keypress(Key(self, "a"))

            case "c":
                self.nodes[self.highlighted].data.mark_complete()

            case "x":
                await self.remove(self.highlighted)

            case "z":
                if self.highlighted:
                    await self.nodes[self.highlighted].toggle()

            case "Z":
                if parent := self.nodes[self.highlighted].parent:
                    if parent != self.root:
                        self.highlight(parent.id)
                        await self.handle_keypress(Key(self, "z"))

            case "j" | "down":
                self.move_highlight_down()

            case "k" | "up":
                self.move_highlight_up()

    async def handle_keypress(self, event: events.Key) -> None:
        """
        Handle incoming kepresses
        """

        if event.key == "escape":
            if self.selected:
                await self.clear_select()
            else:
                await self.reset()

        elif not self.selected:
            await self.handle_shortcut(event.key)
        else:
            if self.selected:
                await self.nodes[self.selected].data.handle_keypress(event.key)

        self.refresh(layout=True)
