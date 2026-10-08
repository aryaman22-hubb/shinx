<script lang="ts">
	import { tv } from "tailwind-variants";

	interface Props {
		variant?: "primary" | "secondary" | "ghost";
		class?: string;
		children?: import('svelte').Snippet;
	}

	let { variant = "primary", class: className = "", children }: Props = $props();

	const button = tv({
		base: "px-3 py-1.5 rounded-md font-medium text-sm cursor-pointer transition-all duration-200 outline-none focus:ring-2 active:scale-95",
		variants: {
			variant: {
				primary: "bg-primary text-on-primary hover:bg-primary/90",
				secondary: "bg-transparent text-on-surface border border-white/20 hover:border-white/30 hover:bg-white/5",
				ghost: "bg-transparent text-on-surface hover:bg-white/10 border border-white/10"
			}
		},
		defaultVariants: {
			variant: "primary"
		}
	});
</script>

<button class={button({ variant, class: className })}>
	{#if children}
		{@render children()}
	{/if}
</button>
