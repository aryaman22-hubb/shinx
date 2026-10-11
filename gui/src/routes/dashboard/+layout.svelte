<script lang="ts">
	import type { LayoutProps } from './$types';
	import { Search, Copy } from "@lucide/svelte";

	import Picker from '#lib/components/primitives/Picker.svelte';
	import Button from '#lib/components/primitives/Button.svelte';
	import Input from '#lib/components/primitives/Input.svelte';

	let { children }: LayoutProps = $props();

	let selectedSchema = $state<{ label: string; value: string }>({ label: "public", value: "public" });
	let searchQuery = $state("");

	const handleSchemaSelect = (item: { label: string; value: string } | string) => {
		if (typeof item === 'string') {
			selectedSchema = { label: item, value: item };
		} else {
			selectedSchema = item;
		}
	};

	const databaseSchema = [
		{
			name: "public",
			tables: ["users", "orders", "products", "categories"]
		},
		{
			name: "analytics",
			tables: ["events", "metrics", "reports"]
		},
		{
			name: "auth",
			tables: ["sessions", "permissions", "roles"]
		}
	];

	const schemaOptions: Array<{ label: string; value: string }> = databaseSchema.map(schema => ({
		label: schema.name,
		value: schema.name
	}));
</script>

<div class="flex flex-col h-full">
    <div class="p-4 flex items-center gap-2">
        <div class="flex items-center">
            <span class="text-xs font-semibold text-on-surface-variant tracking-wider">SCHEMA</span>
            <Picker 
                label="Schema" 
                value={selectedSchema} 
                items={schemaOptions}
                onSelect={handleSchemaSelect}
                class="mx-2 mr-3"
            />
        </div>
        <div class="flex-1 max-w-md">
            <Input
                type="text"
                placeholder="Search table"
                bind:value={searchQuery}
            >
                {#snippet leftIcon()}
                    <Search size={18} />
                {/snippet}
            </Input>
        </div>
        <div class="ml-auto flex items-center gap-2">
            <span class="text-sm text-on-surface-variant">Copy as JSON</span>
            <Button
                variant="icon-bordered"
                size="sm"
                aria-label="Copy as JSON"
            >
                <Copy size={14} />
            </Button>
        </div>
    </div>
    <div class="flex-1 overflow-auto">
        {@render children()}
    </div>
</div>
