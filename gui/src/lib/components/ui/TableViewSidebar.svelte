<script lang="ts">
	import { tv } from "tailwind-variants";
	import { ChevronLeft, Info } from "@lucide/svelte";
	import Button from '#lib/components/primitives/Button.svelte';
	import TableView from './TableView.svelte';
	import type { TableViewSidebarProps } from './types/TableViewSidebar';

	let {
		isOpen = false,
		selectedTable = null,
		tables = [],
		tableDataMap,
		data,
		onToggle,
		class: className = "",
		defaultWidth = 580,
		minWidth = 360,
		maxWidth = 960
	}: TableViewSidebarProps = $props();

	let width = $state(defaultWidth);
	let isDragging = $state(false);

	const startResize = (clientX: number) => {
		if (!isOpen) return;
		isDragging = true;
		const startX = clientX;
		const startWidth = width;

		const handlePointerMove = (moveEvent: MouseEvent | TouchEvent) => {
			if (!isDragging) return;
			const currentX = 'touches' in moveEvent ? moveEvent.touches[0].clientX : moveEvent.clientX;
			// Dragging towards the left increases width
			const delta = startX - currentX;
			const newWidth = Math.max(minWidth, Math.min(maxWidth, startWidth + delta));
			width = newWidth;
		};

		const handlePointerUp = () => {
			isDragging = false;
			window.removeEventListener('mousemove', handlePointerMove);
			window.removeEventListener('mouseup', handlePointerUp);
			window.removeEventListener('touchmove', handlePointerMove);
			window.removeEventListener('touchend', handlePointerUp);
			document.body.style.cursor = '';
			document.body.style.userSelect = '';
		};

		document.body.style.cursor = 'col-resize';
		document.body.style.userSelect = 'none';

		window.addEventListener('mousemove', handlePointerMove);
		window.addEventListener('mouseup', handlePointerUp);
		window.addEventListener('touchmove', handlePointerMove, { passive: true });
		window.addEventListener('touchend', handlePointerUp);
	};

	const onMouseDown = (e: MouseEvent) => {
		e.preventDefault();
		startResize(e.clientX);
	};

	const onTouchStart = (e: TouchEvent) => {
		if (e.touches.length > 0) {
			startResize(e.touches[0].clientX);
		}
	};

	const sidebar = tv({
		base: "bg-[#231f1e] border-l border-white/10 flex flex-col relative",
		variants: {
			isOpen: {
				true: "",
				false: "w-14"
			},
			isDragging: {
				true: "transition-none select-none",
				false: "transition-[width] duration-200"
			}
		},
		defaultVariants: {
			isOpen: false,
			isDragging: false
		}
	});

	const selectedTableData = $derived(tables.find(t => t.name === selectedTable));
	const currentTableData = $derived(
		selectedTable && tableDataMap?.[selectedTable]
			? tableDataMap[selectedTable]
			: data
	);
</script>

<div
	class={sidebar({ isOpen, isDragging, class: className })}
	style={isOpen ? `width: ${width}px;` : undefined}
>
	<!-- Left Edge Resize Handle -->
	{#if isOpen}
		<div
			class="absolute top-0 bottom-0 left-0 w-3 -translate-x-1/2 cursor-col-resize z-30 group flex items-center justify-center select-none"
			onmousedown={onMouseDown}
			ontouchstart={onTouchStart}
			role="separator"
			aria-orientation="vertical"
			aria-label="Resize sidebar width"
			aria-valuenow={width}
		>
			<div class="w-1 h-12 rounded-full bg-white/30 group-hover:bg-primary transition-all duration-150 {isDragging ? 'bg-primary w-1.5 h-16' : ''}"></div>
		</div>
	{/if}

	{#if isOpen}
		<div class="p-4 h-full flex flex-col min-h-0">
			<div class="flex justify-end mb-3">
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
				<div class="flex-1 min-h-0">
					<TableView table={selectedTableData} data={currentTableData} />
				</div>
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
			class="w-full h-full flex items-center justify-center cursor-pointer hover:bg-white/5 transition-colors select-none"
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
