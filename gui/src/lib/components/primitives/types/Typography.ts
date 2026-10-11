export type TypographyVariant =
	| "h1"
	| "h2"
	| "h3"
	| "p"
	| "bh1"
	| "bh2"
	| "bh3"
	| "bhu1"
	| "bhu2";

export interface TypographyProps {
	variant: TypographyVariant;
	class?: string;
	children: import('svelte').Snippet;
}
