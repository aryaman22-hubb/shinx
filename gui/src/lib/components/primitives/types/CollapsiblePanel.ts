export interface CollapsiblePanelProps {
	expanded: boolean;
	onToggle: () => void;
	class?: string;
	headerSlot?: import('svelte').Snippet;
	children?: import('svelte').Snippet;
	defaultHeight?: number;
	minHeight?: number;
	maxHeight?: number;
}

