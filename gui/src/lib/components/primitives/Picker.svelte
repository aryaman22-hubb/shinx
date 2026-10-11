<script lang="ts">
	import { tv } from "tailwind-variants";
	import { ChevronDown } from "@lucide/svelte";
	import MenuItem from '#lib/components/primitives/MenuItem.svelte';
	import type { PickerProps, PickerItem } from './types/Picker';

	let { label, value = label, class: className = "", children, items, onSelect }: PickerProps = $props();

	let isOpen = $state(false);
	let pickerRef: HTMLDivElement;
	const toggle = () => (isOpen = !isOpen);

	const handleClickOutside = (e: MouseEvent) => {
		if (pickerRef && !pickerRef.contains(e.target as Node)) {
			isOpen = false;
		}
	};

	$effect(() => {
		if (isOpen) {
			document.addEventListener('click', handleClickOutside);
		} else {
			document.removeEventListener('click', handleClickOutside);
		}
		return () => {
			document.removeEventListener('click', handleClickOutside);
		};
	});

	const picker = tv({
		base: "relative",
		variants: {}
	});

	const chip = tv({
		base: "flex items-center gap-2 px-3 py-1.5 rounded-md font-medium text-sm cursor-pointer transition-all duration-200 outline-none focus:ring-2 focus:ring-white/20 active:scale-95 bg-transparent text-on-surface border border-white/20 hover:border-white/30 hover:bg-white/5"
	});

	const dropdown = tv({
		base: "absolute top-full left-0 mt-1.5 w-full bg-secondary border border-white/10 rounded-md shadow-xl overflow-hidden z-50"
	});

	const displayValue = $derived(typeof value === 'string' ? value : value?.label || label);
</script>

<div class={picker({ class: className })} bind:this={pickerRef}>
	<button class={chip()} onclick={toggle} aria-expanded={isOpen} aria-haspopup="true">
		<span>{displayValue}</span>
		<ChevronDown size={16} class={isOpen ? "rotate-180 transition-transform" : "transition-transform"} />
	</button>
	{#if isOpen}
		<div class={dropdown()} role="menu">
			{#if items}
				{#each items as item}
					<MenuItem onclick={() => {
						onSelect?.(item);
						isOpen = false;
					}}>
						{item.label}
					</MenuItem>
				{/each}
			{:else if children}
				{@render children()}
			{/if}
		</div>
	{/if}
</div>
