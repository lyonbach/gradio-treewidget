from __future__ import annotations

from collections.abc import Callable, Sequence
from typing import TYPE_CHECKING, Any, Literal, TypedDict

from gradio.components.base import Component, FormComponent
from gradio.events import Events
from gradio.i18n import I18nData

if TYPE_CHECKING:
    from gradio.components import Timer


class TreeNode(TypedDict, total=False):
    """A node displayed in a :class:`TreeWidget`."""

    id: str
    label: str
    children: list[TreeNode]


def _normalize_nodes(nodes: Sequence[TreeNode] | None) -> list[TreeNode]:
    seen_ids: set[str] = set()

    def normalize_level(level: Sequence[TreeNode], path: str) -> list[TreeNode]:
        normalized: list[TreeNode] = []
        for index, node in enumerate(level):
            node_path = f"{path}[{index}]"
            if not isinstance(node, dict):
                raise TypeError(f"Tree node at {node_path} must be a dictionary.")

            node_id = node.get("id")
            label = node.get("label")
            if not isinstance(node_id, str) or not node_id:
                raise ValueError(f"Tree node at {node_path} must have a non-empty string 'id'.")
            if node_id in seen_ids:
                raise ValueError(f"Tree node id {node_id!r} is duplicated.")
            if not isinstance(label, str):
                raise TypeError(f"Tree node at {node_path} must have a string 'label'.")
            seen_ids.add(node_id)

            result: TreeNode = {"id": node_id, "label": label}
            children = node.get("children", [])
            if not isinstance(children, list):
                raise TypeError(f"'children' at {node_path} must be a list.")
            if children:
                result["children"] = normalize_level(children, f"{node_path}.children")
            normalized.append(result)
        return normalized

    if nodes is None:
        return []
    if not isinstance(nodes, Sequence) or isinstance(nodes, (str, bytes)):
        raise TypeError("'nodes' must be a sequence of tree node dictionaries.")
    return normalize_level(nodes, "nodes")


class TreeWidget(FormComponent):
    """
    Displays a nested tree and returns the ID of the selected node.

    Nodes are dictionaries with a unique ``id``, a display ``label``, and an
    optional list of ``children`` using the same shape.
    """

    EVENTS = [
        Events.change,
        Events.input,
    ]

    def __init__(
        self,
        nodes: Sequence[TreeNode] | None = None,
        value: str | Callable | None = None,
        *,
        label: str | I18nData | None = None,
        every: Timer | float | None = None,
        inputs: Component | Sequence[Component] | set[Component] | None = None,
        show_label: bool | None = None,
        scale: int | None = None,
        min_width: int = 160,
        interactive: bool | None = None,
        visible: bool | Literal["hidden"] = True,
        elem_id: str | None = None,
        elem_classes: list[str] | str | None = None,
        render: bool = True,
        key: int | str | tuple[int | str, ...] | None = None,
        preserved_by_key: list[str] | str | None = "value",
    ):
        self.nodes = _normalize_nodes(nodes)
        super().__init__(
            label=label,
            every=every,
            inputs=inputs,
            show_label=show_label,
            scale=scale,
            min_width=min_width,
            interactive=interactive,
            visible=visible,
            elem_id=elem_id,
            elem_classes=elem_classes,
            value=value,
            render=render,
            key=key,
            preserved_by_key=preserved_by_key,
        )

    def preprocess(self, payload: str | None) -> str | None:
        """Return the selected node ID."""
        return None if payload is None else str(payload)

    def postprocess(self, value: str | None) -> str | None:
        """Set the selected node by ID."""
        return None if value is None else str(value)

    def api_info(self) -> dict[str, Any]:
        return {"type": "string"}

    def example_payload(self) -> Any:
        return "guides"

    def example_value(self) -> Any:
        return "guides"
