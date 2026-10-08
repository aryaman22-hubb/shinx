<script lang="ts">
	import favicon from '#lib/assets/favicon.svg';
	import type { LayoutProps } from './$types';

	import {
		Database,
		History,
		Settings,
		User,
		ChevronLeft,
		ChevronRight,
		Menu,
		Plus,
		Workflow,
		Sparkles,
	} from "@lucide/svelte";
	import Typography from '#lib/components/primitives/Typography.svelte';
	import Picker from '#lib/components/primitives/Picker.svelte';
	import Button from '#lib/components/primitives/Button.svelte';

	let { children }: LayoutProps = $props();
	import "../app.css";

	const topItems = [
		{ icon: Workflow, label: "Data Model", href: "/dashboard" },
		{ icon: History, label: "Query History", href: "/dashboard/history" },
	];
	const bottomItems = [
		{ icon: Settings, label: "Settings", href: "/settings" },
		{ icon: User, label: "Profile", href: "/profile" },
	];

	let expanded = $state(false);
	const toggleExpanded = () => (expanded = !expanded);

	let selectedDatabase = $state("Database");
	const handleDatabaseSelect = (value: string) => {
		selectedDatabase = value;
	};
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
</svelte:head>

<div class="flex h-screen bg-secondary">
    <aside
      class="bg-secondary text-white transition-all duration-300 {expanded
        ? 'w-38'
        : 'w-14'} flex flex-col justify-between border-r border-white/10"
    >
      <div class="p-2 flex justify-end">
        <button
          onclick={toggleExpanded}
          class="cursor-pointer p-1.5 rounded-lg hover:bg-white/10 transition-colors"
          aria-label={expanded ? "Collapse sidebar" : "Expand sidebar"}
        >
          {#if expanded}
            <ChevronLeft size={18} />
          {:else}
            <ChevronRight size={18} />
          {/if}
        </button>
      </div>

      <nav class="flex-1 px-1">
        {#each topItems as item}
          <a
            href={item.href}
            class="flex items-center gap-2 px-2 py-2 rounded-lg hover:bg-white/10 transition-colors"
          >
            <item.icon size={18} />
            {#if expanded}
              <span class="whitespace-nowrap text-sm">{item.label}</span>
            {/if}
          </a>
        {/each}
      </nav>

      <nav class="px-1 pb-2">
        {#each bottomItems as item}
          <a
            href={item.href}
            class="flex items-center gap-2 px-2 py-2 rounded-lg hover:bg-white/10 transition-colors"
          >
            <item.icon size={18} />
            {#if expanded}
              <span class="whitespace-nowrap text-sm">{item.label}</span>
            {/if}
          </a>
        {/each}
      </nav>
    </aside>
    <div class="flex-1 flex flex-col">
        <header class="p-4 flex items-center justify-between border-b border-white/10">
            <div class="flex items-center gap-4">
                <Typography variant="bh3">Shinx</Typography>
                <Picker label="Production" value={selectedDatabase} onSelect={handleDatabaseSelect}>
                    <button
                        type="button"
                        class="px-3 py-1.5 text-sm text-on-surface hover:bg-white/10 cursor-pointer w-full text-left transition-colors"
                        onclick={() => handleDatabaseSelect("Production")}
                        role="menuitem"
                    >Production</button>
                    <button
                        type="button"
                        class="px-3 py-1.5 text-sm text-on-surface hover:bg-white/10 cursor-pointer w-full text-left transition-colors"
                        onclick={() => handleDatabaseSelect("Staging")}
                        role="menuitem"
                    >Staging</button>
                    <button
                        type="button"
                        class="px-3 py-1.5 text-sm text-on-surface hover:bg-white/10 cursor-pointer w-full text-left transition-colors"
                        onclick={() => handleDatabaseSelect("Development")}
                        role="menuitem"
                    >Development</button>
                </Picker>
                <button
                    class="w-8 h-8 rounded-full flex items-center justify-center border border-white/20 text-white/60 hover:border-white/30 hover:bg-white/5 hover:text-white/80 transition-all cursor-pointer"
                    aria-label="Add database"
                >
                    <Plus size={16} />
                </button>
            </div>
            <div class="flex items-center gap-2">
                <Button variant="secondary">Feedback</Button>
                <button
                    class="w-8 h-8 rounded-full flex items-center justify-center text-white/60 hover:bg-white/5 hover:text-white/80 cursor-pointer transition-colors"
                    aria-label="Sparkles"
                >
                    <Sparkles size={16} class="hover:animate-spin" />
                </button>
            </div>
        </header>
        <main class="flex-1">
            {@render children()}
        </main>
    </div>
</div>
