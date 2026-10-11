<script lang="ts">
	import type { MenuItemProps } from './types/MenuItem';

	let { onclick, class: className = "", children, ...rest }: MenuItemProps = $props();
</script>

<button
	type="button"
	class="px-3 py-1.5 text-sm text-on-surface hover:bg-white/10 cursor-pointer w-full text-left transition-colors {className}"
	onclick={onclick}
	role="menuitem"
	{...rest}
>
	{#if children}
		{@render children()}
	{/if}
</button>
