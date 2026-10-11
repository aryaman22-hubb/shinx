<script lang="ts">
	import { tv } from "tailwind-variants";
	import { X, ChevronLeft, ChevronRight, Table2 } from "@lucide/svelte";
	import Button from '#lib/components/primitives/Button.svelte';
	import { Info } from '@lucide/svelte';
	import type { TableMetaData } from '#lib/types.ts';
	import TableView from './TableView.svelte';
	import type { TableViewSidebarProps } from './types/TableViewSidebar';

	let { isOpen = false, selectedTable = null, tables = [], onToggle, class: className = "" }: TableViewSidebarProps = $props();

	const sidebar = tv({
		base: "bg-[#231f1e] border-l border-white/10 transition-all duration-300 flex flex-col",
		variants: {
			isOpen: {
				true: "w-[600px]",
				false: "w-14"
			}
		},
		defaultVariants: {
			isOpen: false
		}
	});

	const selectedTableData = $derived(tables.find(t => t.name === selectedTable));
</script>

<div class={sidebar({ isOpen, class: className })}>
	{#if isOpen}
		<div class="p-4 h-full flex flex-col">
			<div class="flex justify-end">
				<Button 
					variant="icon" 
					size="sm"
					onclick={onToggle}
					aria-label="Close table view"
				>
					<ChevronLeft size={16} />
				</Button>
			</div>
			{#if selectedTableData}
				<TableView table={selectedTableData} />
			{:else}
				<div class="flex flex-col items-center justify-center h-full">
					<div class="border border-dashed border-white/20 rounded-lg px-4 py-3 flex flex-col items-center gap-2">
						<Info size={16} class="text-[#899298]" />
						<p class="text-sm text-[#bfc8ce]">Select a table</p>
					</div>
				</div>
			{/if}
		</div>
	{:else}
		<button
			type="button"
			class="w-full h-full flex items-center justify-center cursor-pointer hover:bg-white/5 transition-colors"
			onclick={onToggle}
			aria-label="Toggle table view"
			aria-expanded={isOpen}
		>
			<span
				class="text-sm text-[#bfc8ce] origin-center group-hover:text-[#eae0df] transition-colors"
				style="writing-mode: vertical-rl;"
			>
				Table View
			</span>
		</button>
	{/if}
</div>
