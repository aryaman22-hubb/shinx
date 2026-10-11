export interface SidebarProps {
	expanded?: boolean;
	class?: string;
	topSlot?: import('svelte').Snippet;
	bottomSlot?: import('svelte').Snippet;
	onToggle?: () => void;
	toggleSlot?: import('svelte').Snippet;
	children?: import('svelte').Snippet;
}
