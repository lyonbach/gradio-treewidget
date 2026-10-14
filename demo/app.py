import gradio as gr
from gradio_treewidget import TreeWidget


nodes = [
    {
        "id": "project",
        "label": "Project",
        "children": [
            {
                "id": "backend",
                "label": "Backend",
                "children": [
                    {"id": "component", "label": "treewidget.py"},
                ],
            },
            {
                "id": "frontend",
                "label": "Frontend",
                "children": [
                    {"id": "tree", "label": "Index.svelte"},
                    {"id": "types", "label": "types.ts"},
                ],
            },
        ],
    },
    {"id": "readme", "label": "README.md"},
]


with gr.Blocks() as demo:
    tree = TreeWidget(nodes=nodes, value="project", label="Project files")
    selected = gr.Textbox(label="Selected node ID", interactive=False)
    tree.change(lambda node_id: node_id, inputs=tree, outputs=selected)


if __name__ == "__main__":
    demo.launch()
