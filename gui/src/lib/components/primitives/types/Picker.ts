export interface PickerItem {
	label: string;
	value: string;
}

export interface PickerProps {
	label: string;
	value?: PickerItem | string;
	class?: string;
	children?: import('svelte').Snippet;
	items?: PickerItem[];
	onSelect?: (item: PickerItem | string) => void;
}
