// Tree specs shared by lesson figures (see TreeFigure.astro).
import type { TreeNodeSpec } from '../components/TreeFigure.astro';

// The binary search tree from inserting 8, 3, 10, 1, 6, 14, 4, 7, 13.
// python/tests/test_trees.py checks its traversals.
export const lessonTree: TreeNodeSpec = {
	label: 8,
	children: [
		{
			label: 3,
			children: [{ label: 1 }, { label: 6, children: [{ label: 4 }, { label: 7 }] }],
		},
		{
			label: 10,
			children: [null, { label: 14, children: [{ label: 13 }, null] }],
		},
	],
};

/** A copy of tree with some labels highlighted and others faded. */
export function highlight(
	tree: TreeNodeSpec,
	active: (string | number)[] = [],
	dim: (string | number)[] = []
): TreeNodeSpec {
	return {
		...tree,
		active: active.includes(tree.label),
		dim: dim.includes(tree.label),
		children: tree.children?.map((c) => (c ? highlight(c, active, dim) : null)),
	};
}
