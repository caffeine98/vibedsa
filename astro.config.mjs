// @ts-check
import { existsSync } from 'node:fs';
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import { curriculum } from './src/data/curriculum.mjs';

const pageExists = (/** @type {string} */ slug) =>
	['.md', '.mdx'].some((ext) => existsSync(`./src/content/docs/${slug}${ext}`));

// Sidebar follows the curriculum, showing only topics that have been written.
const sidebar = [
	{ label: 'How to read this site', slug: 'guide' },
	...curriculum
		.map((section) => ({
			label: `${section.num} ${section.title}`,
			items: section.topics
				.filter((t) => pageExists(t.slug))
				.map((t) => ({ label: t.title, slug: t.slug })),
		}))
		.filter((group) => group.items.length > 0),
];

export default defineConfig({
	site: 'https://caffeine98.github.io',
	base: '/vibedsa',
	integrations: [
		starlight({
			title: 'VibeDSA',
			description: 'Data structures and algorithms in plain English, with tested Python.',
			logo: { src: './src/assets/logo.svg', replacesTitle: false },
			favicon: '/favicon.svg',
			social: [{ icon: 'github', label: 'GitHub', href: 'https://github.com/caffeine98/vibedsa' }],
			customCss: ['./src/styles/fonts.css', './src/styles/theme.css'],
			components: { Hero: './src/components/Hero.astro' },
			expressiveCode: {
				themes: ['github-dark-dimmed', 'github-light'],
				styleOverrides: {
					borderRadius: '0',
					borderColor: 'var(--sl-color-hairline-light)',
					codeFontFamily: 'var(--sl-font-mono)',
					uiFontFamily: 'var(--sl-font-mono)',
					frames: { shadowColor: 'transparent' },
				},
			},
			sidebar,
			lastUpdated: false,
		}),
	],
});
