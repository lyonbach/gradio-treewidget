import type { ILoadingStatus as LoadingStatus } from "@gradio/statustracker";

export interface TreeNode {
	id: string;
	label: string;
	children?: TreeNode[];
}

export interface TreeWidgetProps {
	value: string | null;
	nodes: TreeNode[];
}

export interface TreeWidgetEvents {
	change: never;
	input: never;
	clear_status: LoadingStatus;
}
