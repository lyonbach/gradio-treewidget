---
tags: [gradio-custom-component, TreeWidget]
title: gradio_treewidget
short_description: A selectable hierarchical tree component for Gradio
colorFrom: blue
colorTo: yellow
sdk: gradio
pinned: false
app_file: space.py
---

# `gradio_treewidget`

A Gradio custom component for displaying and selecting items in a hierarchy, inspired by PySide's `QTreeWidget`.

## Installation

```bash
pip install gradio_treewidget
```

## Usage

Each node has a unique string `id`, a display `label`, and optional `children`.
The component value is the ID of the selected node.

```python
import gradio as gr
from gradio_treewidget import TreeWidget

nodes = [
    {
        "id": "guides",
        "label": "Guides",
        "children": [
            {"id": "installation", "label": "Installation"},
            {"id": "usage", "label": "Usage"},
        ],
    },
    {"id": "api", "label": "API reference"},
]

demo = gr.Interface(
    lambda selected_id: f"Selected node: {selected_id}",
    TreeWidget(nodes=nodes, value="guides"),
    gr.Textbox(label="Selection"),
)

if __name__ == "__main__":
    demo.launch()
```

Expand and collapse branches with the disclosure buttons, and select a node to
send its ID to a Gradio event or prediction function. Use
`TreeWidget(nodes=nodes, interactive=False)` to display a read-only tree.

## API

### `TreeWidget(nodes=None, value=None, ...)`

| Parameter | Type | Description |
| --- | --- | --- |
| `nodes` | `Sequence[TreeNode] \| None` | Root nodes to display. Each node is a dictionary with a unique, non-empty string `id`, a string `label`, and an optional list of `children`. |
| `value` | `str \| Callable \| None` | Selected node ID. |
| `label` | `str \| None` | Component label. |
| `interactive` | `bool \| None` | Whether users can select nodes. Inferred from component use if omitted. |
| `visible` | `bool \| "hidden"` | Whether the component is shown. |
| `elem_id`, `elem_classes` | `str \| list[str] \| None` | DOM identifier and CSS classes. |

The component fires `input` when the user selects a node and `change` when its
value changes. Selection is single-node; expanding and collapsing branches
does not change the component value.
