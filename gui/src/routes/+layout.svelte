<script lang="ts">
  import {
		History,
		Settings,
		User,
		Plus,
		Workflow,
		Sparkles,
	} from "@lucide/svelte";

	import favicon from '#lib/assets/favicon.png';
	import type { LayoutProps } from './$types';
	import "../app.css";
	
	import Typography from '#lib/components/primitives/Typography.svelte';
	import Picker from '#lib/components/primitives/Picker.svelte';
	import Button from '#lib/components/primitives/Button.svelte';
	import MainSidebar from '#lib/components/ui/MainSidebar.svelte';

	let { children }: LayoutProps = $props();

	const topItems = [
		{ icon: Workflow, label: "Data Model", href: "/dashboard" },
		{ icon: History, label: "Query History", href: "/dashboard/history" },
	];
	const bottomItems = [
		{ icon: Settings, label: "Settings", href: "/settings" },
		{ icon: User, label: "Profile", href: "/profile" },
	];

	let selectedDatabase = $state<{ label: string; value: string }>({ label: "Development", value: "Development" });
	const handleDatabaseSelect = (item: { label: string; value: string } | string) => {
		if (typeof item === 'string') {
			selectedDatabase = { label: item, value: item };
		} else {
			selectedDatabase = item;
		}
	};

	const databaseOptions: Array<{ label: string; value: string }> = [
		{ label: "Production", value: "Production" },
		{ label: "Staging", value: "Staging" },
		{ label: "Development", value: "Development" }
	];
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
</svelte:head>

<div class="flex h-screen bg-secondary">
    <MainSidebar {topItems} {bottomItems} />
    <div class="flex-1 flex flex-col">
        <header class="p-4 flex items-center justify-between border-b border-white/10">
            <div class="flex items-center gap-4">
                <Typography variant="bh3">Shinx</Typography>
                <Picker 
                    label="Database" 
                    value={selectedDatabase} 
                    items={databaseOptions}
                    onSelect={handleDatabaseSelect}
                />
                <Button variant="icon-bordered" aria-label="Add database">
                    <Plus size={16} />
                </Button>
            </div>
            <div class="flex items-center gap-2">
                <Button variant="secondary">Feedback</Button>
                <Button variant="icon" aria-label="Sparkles">
                    <Sparkles size={16} class="hover:animate-spin" />
                </Button>
            </div>
        </header>
        <main class="flex-1">
            {@render children()}
        </main>
    </div>
</div>
