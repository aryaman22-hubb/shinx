export interface ModalProps {
	open?: boolean;
	variant?: "center" | "positioned";
	class?: string;
	onClose?: () => void;
	children?: import('svelte').Snippet;
	targetElement?: HTMLElement;
	backdropBlur?: boolean;
	[rest: string]: any;
}
