export interface InputProps {
	type?: string;
	placeholder?: string;
	class?: string;
	leftIcon?: import('svelte').Snippet;
	rightIcon?: import('svelte').Snippet;
	children?: import('svelte').Snippet;
	value?: string;
	[rest: string]: any;
}
