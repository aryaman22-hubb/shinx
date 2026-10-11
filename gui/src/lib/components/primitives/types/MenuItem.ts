export interface MenuItemProps {
	onclick?: () => void;
	class?: string;
	children?: import('svelte').Snippet;
	[rest: string]: any;
}
