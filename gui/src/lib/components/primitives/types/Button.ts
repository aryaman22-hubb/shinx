export interface ButtonProps {
	variant?: "primary" | "secondary" | "ghost" | "icon" | "icon-bordered";
	size?: "xs" | "sm" | "md" | "lg";
	class?: string;
	children?: import('svelte').Snippet;
	[rest: string]: any;
}
