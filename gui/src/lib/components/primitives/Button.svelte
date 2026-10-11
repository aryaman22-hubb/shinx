<script lang="ts">
	import { tv } from "tailwind-variants";
	import type { ButtonProps } from './types/Button';

	let { variant = "primary", size = "md", class: className = "", children, ...rest }: ButtonProps = $props();

	const button = tv({
		base: "cursor-pointer transition-all duration-200 outline-none focus:ring-2 active:scale-95",
		variants: {
			variant: {
				primary: "px-3 py-1.5 rounded-md font-medium text-sm bg-primary text-on-primary hover:bg-primary/90",
				secondary: "px-3 py-1.5 rounded-md font-medium text-sm bg-transparent text-on-surface border border-white/20 hover:border-white/30 hover:bg-white/5",
				ghost: "px-3 py-1.5 rounded-md font-medium text-sm bg-transparent text-on-surface hover:bg-white/10 border border-white/10",
				icon: "rounded-full flex items-center justify-center text-white/60 hover:bg-white/5 hover:text-white/80",
				"icon-bordered": "rounded-full flex items-center justify-center border border-white/20 text-white/60 hover:border-white/30 hover:bg-white/5 hover:text-white/80"
			},
			size: {
				xs: "w-5 h-5",
				sm: "w-6 h-6",
				md: "w-8 h-8",
				lg: "w-10 h-10"
			}
		},
		compoundVariants: [
			{
				variant: ["primary", "secondary", "ghost"],
				size: ["xs", "sm", "md", "lg"],
				class: "w-auto h-auto"
			}
		],
		defaultVariants: {
			variant: "primary",
			size: "md"
		}
	});
</script>

<button class={button({ variant, size, class: className })} {...rest}>
	{#if children}
		{@render children()}
	{/if}
</button>
