// The full topic list, in learning order. This is the single source of truth:
// - the home page index is built from it (unwritten topics show as "planned")
// - the sidebar is built from it (only topics whose page exists are shown)
//
// To publish a topic: write src/content/docs/<slug>.mdx. Nothing else to change.

/** @typedef {{ title: string, slug: string }} Topic */
/** @typedef {{ num: string, title: string, blurb: string, topics: Topic[] }} Section */

/** @type {Section[]} */
export const curriculum = [
	{
		num: '00',
		title: 'Foundations',
		blurb: 'The tools you need to read every other page.',
		topics: [
			{ title: 'Big-O notation', slug: 'foundations/big-o' },
			{ title: 'Recursion', slug: 'foundations/recursion' },
		],
	},
	{
		num: '01',
		title: 'Linear structures',
		blurb: 'Data laid out in a line.',
		topics: [
			{ title: 'Arrays', slug: 'data-structures/arrays' },
			{ title: 'Linked lists', slug: 'data-structures/linked-list' },
			{ title: 'Stack', slug: 'data-structures/stack' },
			{ title: 'Queue and deque', slug: 'data-structures/queue' },
			{ title: 'Hash map and hash set', slug: 'data-structures/hash-map' },
		],
	},
	{
		num: '02',
		title: 'Searching and sorting',
		blurb: 'Find things fast. Put things in order.',
		topics: [
			{ title: 'Binary search', slug: 'algorithms/binary-search' },
			{ title: 'Bubble sort', slug: 'algorithms/bubble-sort' },
			{ title: 'Insertion sort', slug: 'algorithms/insertion-sort' },
			{ title: 'Merge sort', slug: 'algorithms/merge-sort' },
			{ title: 'Quicksort', slug: 'algorithms/quicksort' },
			{ title: 'Counting sort', slug: 'algorithms/counting-sort' },
		],
	},
	{
		num: '03',
		title: 'Trees',
		blurb: 'Data with parents and children.',
		topics: [
			{ title: 'Trees and traversals', slug: 'data-structures/trees' },
			{ title: 'Binary search tree', slug: 'data-structures/bst' },
			{ title: 'Heap and heap sort', slug: 'data-structures/heap' },
			{ title: 'Trie', slug: 'data-structures/trie' },
		],
	},
	{
		num: '04',
		title: 'Graphs',
		blurb: 'Things and the connections between them.',
		topics: [
			{ title: 'Graph basics', slug: 'data-structures/graphs' },
			{ title: 'Breadth-first search', slug: 'algorithms/bfs' },
			{ title: 'Depth-first search', slug: 'algorithms/dfs' },
			{ title: 'Topological sort', slug: 'algorithms/topological-sort' },
			{ title: "Dijkstra's algorithm", slug: 'algorithms/dijkstra' },
			{ title: 'Union-Find', slug: 'data-structures/union-find' },
			{ title: 'Minimum spanning tree', slug: 'algorithms/mst' },
		],
	},
	{
		num: '05',
		title: 'Patterns',
		blurb: 'Reusable ideas for solving problems.',
		topics: [
			{ title: 'Two pointers', slug: 'patterns/two-pointers' },
			{ title: 'Sliding window', slug: 'patterns/sliding-window' },
			{ title: 'Prefix sums', slug: 'patterns/prefix-sums' },
			{ title: 'Backtracking', slug: 'patterns/backtracking' },
			{ title: 'Greedy algorithms', slug: 'patterns/greedy' },
			{ title: 'Dynamic programming', slug: 'patterns/dynamic-programming' },
		],
	},
];
