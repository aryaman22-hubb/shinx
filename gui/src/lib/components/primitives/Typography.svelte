<script lang="ts">
	import { tv } from "tailwind-variants";

	type Variant =
		| "h1"
		| "h2"
		| "h3"
		| "p"
		| "bh1"
		| "bh2"
		| "bh3"
		| "bhu1"
		| "bhu2";

	interface Props {
		variant: Variant;
		class?: string;
		children: import('svelte').Snippet;
	}

	let { variant, class: className = "", children }: Props = $props();

	const primitive = tv({
		base: "",
		variants: {
			variant: {
				h1: "text-4xl font-bold text-on-surface",
				h2: "text-3xl font-semibold text-on-surface",
				h3: "text-2xl font-medium text-on-surface",
				p: "text-base text-on-surface-variant",
				bh1: "text-4xl font-black text-primary italic tracking-tight",
				bh2: "text-3xl font-black text-primary italic tracking-tight",
				bh3: "text-2xl font-black text-primary italic tracking-tight",
				bhu1: "text-4xl font-black text-primary italic tracking-tight underline decoration-highlight decoration-2 underline-offset-4",
				bhu2: "text-3xl font-black text-primary italic tracking-tight underline decoration-highlight decoration-2 underline-offset-4"
			}
		}
	});

	const tagMap: Record<Variant, keyof HTMLElementTagNameMap> = {
		h1: "h1",
		h2: "h2",
		h3: "h3",
		p: "p",
		bh1: "h1",
		bh2: "h2",
		bh3: "h3",
		bhu1: "h1",
		bhu2: "h2"
	};

	const tag = $derived(tagMap[variant]);
</script>

<svelte:element this={tag} class={primitive({ variant, class: className })}>
	{@render children()}
</svelte:element>
