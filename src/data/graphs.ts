// Graphs shared by lesson figures (see GraphFigure.astro).
// python/tests/test_graphs.py checks the results quoted on the pages.
import type { GraphEdgeSpec, GraphNodeSpec } from '../components/GraphFigure.astro';

// Undirected example for graph basics, BFS and DFS.
export const lessonNodes: GraphNodeSpec[] = [
	{ id: 'A', x: 0, y: 90 },
	{ id: 'B', x: 110, y: 30 },
	{ id: 'C', x: 110, y: 150 },
	{ id: 'D', x: 220, y: 90 },
	{ id: 'E', x: 220, y: 210 },
	{ id: 'F', x: 330, y: 210 },
];
export const lessonEdges: GraphEdgeSpec[] = [
	{ from: 'A', to: 'B' },
	{ from: 'A', to: 'C' },
	{ from: 'B', to: 'D' },
	{ from: 'C', to: 'D' },
	{ from: 'C', to: 'E' },
	{ from: 'E', to: 'F' },
];

// Directed acyclic example for topological sort: an edge means "before".
export const taskNodes: GraphNodeSpec[] = [
	{ id: 'A', x: 0, y: 30 },
	{ id: 'B', x: 0, y: 150 },
	{ id: 'C', x: 120, y: 30 },
	{ id: 'D', x: 120, y: 150 },
	{ id: 'E', x: 240, y: 90 },
	{ id: 'F', x: 360, y: 90 },
];
export const taskEdges: GraphEdgeSpec[] = [
	{ from: 'A', to: 'C' },
	{ from: 'B', to: 'C' },
	{ from: 'B', to: 'D' },
	{ from: 'C', to: 'E' },
	{ from: 'D', to: 'E' },
	{ from: 'E', to: 'F' },
];

/** Copy nodes, adding notes (by id) and highlighting some ids. */
export function annotate(
	nodes: GraphNodeSpec[],
	notes: Record<string, string | number> = {},
	active: string[] = []
): GraphNodeSpec[] {
	return nodes.map((n) => ({ ...n, note: notes[n.id], active: active.includes(n.id) }));
}

/** Copy edges, highlighting the ones listed as "A-B" (either direction). */
export function highlightEdges(edges: GraphEdgeSpec[], keys: string[]): GraphEdgeSpec[] {
	const has = (a: string, b: string) => keys.includes(`${a}-${b}`) || keys.includes(`${b}-${a}`);
	return edges.map((e) => ({ ...e, active: has(e.from, e.to) }));
}
