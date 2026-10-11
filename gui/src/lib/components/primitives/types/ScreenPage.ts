export type ScreenPageVariant = "padded" | "centered" | "full";

export interface ScreenPageProps {
	variant?: "padded" | "centered" | "full";
	class?: string;
	children: import('svelte').Snippet;
}
