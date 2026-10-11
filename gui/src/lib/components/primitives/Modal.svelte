<script lang="ts">
	import { tv } from "tailwind-variants";
	import type { ModalProps } from './types/Modal';

	let {
		open = false,
		variant = "center",
		class: className = "",
		onClose,
		children,
		targetElement,
		backdropBlur = true,
		...rest
	}: ModalProps = $props();

	const backdrop = tv({
		base: "fixed inset-0 bg-black/60 transition-opacity duration-200 z-50",
		variants: {
			open: {
				true: "opacity-100",
				false: "opacity-0 pointer-events-none"
			},
			backdropBlur: {
				true: "backdrop-blur-sm",
				false: ""
			}
		},
		defaultVariants: {
			open: false,
			backdropBlur: true
		}
	});

	const modal = tv({
		base: "bg-secondary border border-white/10 rounded-lg shadow-2xl transition-all duration-200",
		variants: {
			variant: {
				center: "fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 z-50 max-w-[90vw] max-h-[90vh] overflow-auto",
				positioned: "absolute z-50 min-w-[200px]"
			},
			open: {
				true: "opacity-100 scale-100",
				false: "opacity-0 scale-95 pointer-events-none"
			}
		},
		defaultVariants: {
			variant: "center",
			open: false
		}
	});

	let modalPosition = $derived(() => {
		if (variant === "positioned" && targetElement) {
			const rect = targetElement.getBoundingClientRect();
			return `top: ${rect.bottom + 8}px; left: ${rect.left}px;`;
		}
		return "";
	});

	function handleBackdropClick(e: MouseEvent) {
		if (e.target === e.currentTarget && onClose) {
			onClose();
		}
	}
</script>

{#if open}
	<div class={backdrop({ open, backdropBlur })} onclick={handleBackdropClick} {...rest}>
		<div 
			class={modal({ variant, open, class: className })}
			style={modalPosition()}
		>
			{#if children}
				{@render children()}
			{/if}
		</div>
	</div>
{/if}
