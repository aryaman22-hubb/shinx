<script lang="ts">
	import { tv } from "tailwind-variants";
	import { ChevronLeft, ChevronRight } from "@lucide/svelte";
	import Sidebar from '#lib/components/primitives/Sidebar.svelte';
	import type { MainSidebarProps } from './types/MainSidebar';

	let { topItems = [], bottomItems = [], class: className = "" }: MainSidebarProps = $props();

	let expanded = $state(false);
	const toggleExpanded = () => (expanded = !expanded);

	const sidebar = tv({
		base: "bg-secondary text-white",
		variants: {}
	});

	const navItem = tv({
		base: "flex items-center gap-2 px-2 py-2 rounded-lg hover:bg-white/10 transition-colors",
		variants: {}
	});
</script>

{#snippet toggleSlot()}
	<button
		onclick={toggleExpanded}
		class="cursor-pointer p-1.5 rounded-lg hover:bg-white/10 transition-colors"
		aria-label={expanded ? "Collapse sidebar" : "Expand sidebar"}
	>
		{#if expanded}
			<ChevronLeft size={18} />
		{:else}
			<ChevronRight size={18} />
		{/if}
	</button>
{/snippet}

{#snippet topSlot()}
	{#each topItems as item}
		<a href={item.href} class={navItem()}>
			<item.icon size={18} />
			{#if expanded}
				<span class="whitespace-nowrap text-sm">{item.label}</span>
			{/if}
		</a>
	{/each}
{/snippet}

{#snippet bottomSlot()}
	{#each bottomItems as item}
		<a href={item.href} class={navItem()}>
			<item.icon size={18} />
			{#if expanded}
				<span class="whitespace-nowrap text-sm">{item.label}</span>
			{/if}
		</a>
	{/each}
{/snippet}

<Sidebar 
	{expanded} 
	class={sidebar({ class: className })}
	onToggle={toggleExpanded}
	toggleSlot={toggleSlot}
	topSlot={topSlot}
	bottomSlot={bottomSlot}
/>
