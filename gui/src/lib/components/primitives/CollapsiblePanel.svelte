<script lang="ts">
	import { ChevronUp, ChevronDown } from '@lucide/svelte';
	import { tv } from 'tailwind-variants';
	import type { CollapsiblePanelProps } from './types/CollapsiblePanel';

	let {
		expanded,
		onToggle,
		class: className = '',
		headerSlot,
		children,
		defaultHeight = 360,
		minHeight = 160,
		maxHeight = 800
	}: CollapsiblePanelProps = $props();

	let height = $state(defaultHeight);
	let isDragging = $state(false);

	const startResize = (clientY: number) => {
		if (!expanded) return;
		isDragging = true;
		const startY = clientY;
		const startHeight = height;

		const handlePointerMove = (moveEvent: MouseEvent | TouchEvent) => {
			if (!isDragging) return;
			const currentY = 'touches' in moveEvent ? moveEvent.touches[0].clientY : moveEvent.clientY;
			const delta = startY - currentY;
			const newHeight = Math.max(minHeight, Math.min(maxHeight, startHeight + delta));
			height = newHeight;
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

		document.body.style.cursor = 'row-resize';
		document.body.style.userSelect = 'none';

		window.addEventListener('mousemove', handlePointerMove);
		window.addEventListener('mouseup', handlePointerUp);
		window.addEventListener('touchmove', handlePointerMove, { passive: true });
		window.addEventListener('touchend', handlePointerUp);
	};

	const onMouseDown = (e: MouseEvent) => {
		e.preventDefault();
		startResize(e.clientY);
	};

	const onTouchStart = (e: TouchEvent) => {
		if (e.touches.length > 0) {
			startResize(e.touches[0].clientY);
		}
	};

	const panel = tv({
		base: 'flex flex-col border-t border-white/10 relative',
		variants: {
			expanded: {
				true: '',
				false: 'h-10'
			},
			isDragging: {
				true: 'transition-none select-none',
				false: 'transition-[height] duration-200'
			}
		},
		defaultVariants: {
			expanded: false,
			isDragging: false
		}
	});
</script>

<div
	class={panel({ expanded, isDragging, class: className })}
	style={expanded ? `height: ${height}px;` : undefined}
>
	<!-- Drag Resize Handle -->
	{#if expanded}
		<div
			class="absolute top-0 left-0 right-0 h-3 -translate-y-1/2 cursor-row-resize z-20 group flex items-center justify-center select-none"
			onmousedown={onMouseDown}
			ontouchstart={onTouchStart}
			role="separator"
			aria-orientation="horizontal"
			aria-label="Resize panel height"
			aria-valuenow={height}
		>
			<div class="w-12 h-1 rounded-full bg-white/30 group-hover:bg-primary transition-all duration-150 {isDragging ? 'bg-primary w-16 h-1.5' : ''}"></div>
		</div>
	{/if}

	<!-- Header with toggle button -->
	<div
		class="p-3 flex items-center justify-between bg-[#1a1716] flex-shrink-0 cursor-pointer hover:bg-[#231f1e] transition-colors select-none"
		role="button"
		tabindex="0"
		onclick={onToggle}
		onkeydown={(e) => {
			if (e.key === 'Enter' || e.key === ' ') {
				e.preventDefault();
				onToggle();
			}
		}}
	>
		{#if headerSlot}
			{@render headerSlot()}
		{/if}
		<div class="flex items-center gap-2">
			{#if expanded}
				<ChevronDown size={16} class="text-[#bfc8ce]" />
			{:else}
				<ChevronUp size={16} class="text-[#bfc8ce]" />
			{/if}
		</div>
	</div>

	<!-- Content -->
	{#if expanded && children}
		<div class="flex-1 overflow-auto min-h-0">
			{@render children()}
		</div>
	{/if}
</div>
