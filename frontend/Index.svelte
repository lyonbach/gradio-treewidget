<script lang="ts">
	import type { TreeWidgetEvents, TreeWidgetProps, TreeNode } from "./types";
	import { Gradio } from "@gradio/utils";
	import { BlockTitle, Block } from "@gradio/atoms";
	import { StatusTracker } from "@gradio/statustracker";

	const props = $props();
	const gradio = (() => new Gradio<TreeWidgetEvents, TreeWidgetProps>(props))();

	type VisibleNode = {
		node: TreeNode;
		level: number;
		hasChildren: boolean;
	};

	let expanded = $state(new Set<string>());
	let old_value = $state<string | null>(null);
	let initialized = false;

	function flatten(nodes: TreeNode[], level = 1): VisibleNode[] {
		const visible: VisibleNode[] = [];
		for (const node of nodes) {
			const hasChildren = Boolean(node.children?.length);
			visible.push({ node, level, hasChildren });
			if (hasChildren && expanded.has(node.id)) {
				visible.push(...flatten(node.children ?? [], level + 1));
			}
		}
		return visible;
	}

	let visibleNodes = $derived(flatten(gradio.props.nodes));

	function toggleExpanded(id: string): void {
		const next = new Set(expanded);
		if (next.has(id)) {
			next.delete(id);
		} else {
			next.add(id);
		}
		expanded = next;
	}

	function selectNode(id: string): void {
		if (!gradio.shared.interactive) return;
		gradio.props.value = id;
		gradio.dispatch("input");
	}

	$effect(() => {
		if (!initialized) {
			old_value = gradio.props.value;
			initialized = true;
			return;
		}
		if (old_value !== gradio.props.value) {
			old_value = gradio.props.value;
			gradio.dispatch("change");
		}
	});
</script>

<Block
	visible={gradio.shared.visible}
	elem_id={gradio.shared.elem_id}
	elem_classes={gradio.shared.elem_classes}
	scale={gradio.shared.scale}
	min_width={gradio.shared.min_width}
	allow_overflow={false}
	padding={true}
>
	{#if gradio.shared.loading_status}
		<StatusTracker
			autoscroll={gradio.shared.autoscroll}
			i18n={gradio.i18n}
			{...gradio.shared.loading_status}
			on_clear_status={() =>
				gradio.dispatch("clear_status", gradio.shared.loading_status)}
		/>
	{/if}

	<div class="tree-widget">
		<BlockTitle show_label={gradio.shared.show_label} info={undefined}>
			{gradio.shared.label}
		</BlockTitle>
		{#if visibleNodes.length}
			<ul role="tree" aria-label={gradio.shared.label ?? "Tree"}>
				{#each visibleNodes as row (row.node.id)}
					<li
						role="treeitem"
						aria-level={row.level}
						aria-expanded={row.hasChildren ? expanded.has(row.node.id) : undefined}
						aria-selected={gradio.props.value === row.node.id}
					>
						<div class="tree-row" style:--level={row.level}>
							{#if row.hasChildren}
								<button
									class="expander"
									type="button"
									aria-label="{expanded.has(row.node.id) ? 'Collapse' : 'Expand'} {row.node.label}"
									aria-expanded={expanded.has(row.node.id)}
									onclick={() => toggleExpanded(row.node.id)}
								>
									{expanded.has(row.node.id) ? "▾" : "▸"}
								</button>
							{:else}
								<span class="expander-spacer" aria-hidden="true"></span>
							{/if}
							<button
								class="node"
								class:selected={gradio.props.value === row.node.id}
								type="button"
								disabled={!gradio.shared.interactive}
								onclick={() => selectNode(row.node.id)}
							>
								{row.node.label}
							</button>
						</div>
					</li>
				{/each}
			</ul>
		{:else}
			<div class="empty">No items</div>
		{/if}
	</div>
</Block>

<style>
	.tree-widget {
		width: 100%;
		color: var(--body-text-color);
	}

	ul {
		list-style: none;
		margin: 0;
		padding: var(--size-1) 0;
		max-height: 24rem;
		overflow: auto;
	}

	li {
		margin: 0;
		padding: 0;
	}

	.tree-row {
		display: flex;
		align-items: center;
		gap: var(--size-1);
		padding: 1px var(--size-2) 1px calc(var(--size-2) + (var(--level) - 1) * 1.25rem);
		min-height: 2rem;
	}

	.expander,
	.expander-spacer {
		display: inline-flex;
		align-items: center;
		justify-content: center;
		flex: 0 0 1.25rem;
		width: 1.25rem;
		height: 1.5rem;
	}

	.expander {
		border: 0;
		border-radius: var(--button-small-radius);
		background: transparent;
		color: inherit;
		cursor: pointer;
	}

	.expander:hover {
		background: var(--button-secondary-background-fill);
	}

	.node {
		flex: 1;
		min-width: 0;
		padding: var(--size-1) var(--size-2);
		border: 1px solid transparent;
		border-radius: var(--button-small-radius);
		background: transparent;
		color: inherit;
		text-align: left;
		overflow-wrap: anywhere;
		cursor: pointer;
	}

	.node:hover:not(:disabled) {
		background: var(--button-secondary-background-fill);
	}

	.node.selected {
		border-color: var(--input-border-color-focus);
		background: var(--button-secondary-background-fill);
	}

	.node:disabled {
		cursor: default;
		opacity: 0.8;
	}

	.empty {
		padding: var(--size-2);
		color: var(--body-text-color-subdued);
	}
</style>
