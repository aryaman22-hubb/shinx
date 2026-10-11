export interface CodeMirrorEditorProps {
	value: string;
	onValueChange?: (value: string) => void;
	readonly?: boolean;
	placeholder?: string;
	class?: string;
	height?: string;
	minHeight?: string;
}
