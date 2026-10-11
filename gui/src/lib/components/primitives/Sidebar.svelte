<script lang="ts">
	import { tv } from "tailwind-variants";
	import type { SidebarProps } from './types/Sidebar';

	let { 
		expanded = false, 
		class: className = "", 
		topSlot, 
		bottomSlot, 
		onToggle,
		toggleSlot,
		children
	}: SidebarProps = $props();

	const sidebar = tv({
		base: "transition-all duration-300 flex flex-col justify-between border-r border-white/10",
		variants: {
			expanded: {
				true: "w-38",
				false: "w-14"
			}
		},
		defaultVariants: {
			expanded: false
		}
	});
</script>

<aside class={sidebar({ expanded, class: className })}>
	{#if toggleSlot}
		<div class="p-2 flex justify-end">
			{@render toggleSlot()}
		</div>
	{/if}

	{#if topSlot}
		<nav class="flex-1 px-1">
			{@render topSlot()}
		</nav>
	{/if}

	{#if children}
		<div class="flex-1 overflow-auto">
			{@render children()}
		</div>
	{/if}

	{#if bottomSlot}
		<nav class="px-1 pb-2">
			{@render bottomSlot()}
		</nav>
	{/if}
</aside>
