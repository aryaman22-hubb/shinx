<script lang="ts">
	import { tv } from "tailwind-variants";

	type Variant = "padded" | "centered" | "full";

	interface Props {
		variant?: Variant;
		class?: string;
		children: import('svelte').Snippet;
	}

	let { variant = "full", class: className = "", children }: Props = $props();

	const screenPage = tv({
		base: "h-full bg-secondary",
		variants: {
			variant: {
				padded: "p-8",
				centered: "flex items-center justify-center",
				full: ""
			}
		},
		defaultVariants: {
			variant: "full"
		}
	});
</script>

<div class={screenPage({ variant, class: className })}>
	{@render children()}
</div>
