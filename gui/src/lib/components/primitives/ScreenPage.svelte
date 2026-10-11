<script lang="ts">
	import { tv } from "tailwind-variants";
	import type { ScreenPageProps } from './types/ScreenPage';

	let { variant = "full", class: className = "", children }: ScreenPageProps = $props();

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
