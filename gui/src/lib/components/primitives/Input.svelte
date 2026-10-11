<script lang="ts">
	import { tv } from "tailwind-variants";
	import type { InputProps } from './types/Input';

	let { type = "text", placeholder, id, class: className = "", leftIcon, rightIcon, children, value = $bindable(), ...rest }: InputProps = $props();

	const wrapper = tv({
		base: "relative",
		variants: {}
	});

	const input = tv({
		base: "w-full py-1.5 rounded-md bg-white/5 border border-white/10 text-sm text-on-surface placeholder:text-white/40 focus:outline-none focus:border-white/20 focus:bg-white/10 transition-all",
		variants: {
			hasLeftIcon: {
				true: "pl-10",
				false: "pl-4"
			},
			hasRightIcon: {
				true: "pr-10",
				false: "pr-4"
			}
		},
		defaultVariants: {
			hasLeftIcon: false,
			hasRightIcon: false
		}
	});

	const icon = tv({
		base: "absolute top-1/2 -translate-y-1/2 text-white/60",
		variants: {
			position: {
				left: "left-3",
				right: "right-3"
			}
		}
	});
</script>

<div class={wrapper({ class: className })}>
	{#if leftIcon}
		<div class={icon({ position: "left" })}>
			{@render leftIcon()}
		</div>
	{/if}
	<input
		{type}
		{placeholder}
		{id}
		bind:value
		class={input({ hasLeftIcon: !!leftIcon, hasRightIcon: !!rightIcon })}
		{...rest}
	/>
	{#if rightIcon}
		<div class={icon({ position: "right" })}>
			{@render rightIcon()}
		</div>
	{/if}
	{#if children}
		{@render children()}
	{/if}
</div>
