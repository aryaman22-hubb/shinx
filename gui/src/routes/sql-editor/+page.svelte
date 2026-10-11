<script lang="ts">
	import { Play, Loader2, RotateCcw } from "@lucide/svelte";
	import { onMount } from "svelte";

	import Button from '#lib/components/primitives/Button.svelte';
	import Typography from '#lib/components/primitives/Typography.svelte';
	import CodeMirrorEditor from '#lib/components/primitives/CodeMirrorEditor.svelte';
	import CollapsiblePanel from '#lib/components/primitives/CollapsiblePanel.svelte';
	import TableView from '#lib/components/ui/TableView.svelte';
	import type { TableMetaData } from '#lib/types.ts';

	let query = $state("select * from kb_documents;");
	let isRunning = $state(false);
	let isResultsExpanded = $state(true);

	// Detect Mac vs Windows/Linux for keyboard shortcut hint
	let isMac = $state(false);
	onMount(() => {
		isMac = typeof navigator !== 'undefined' && /Mac|iPod|iPhone|iPad/.test(navigator.platform);

		const handleKeyDown = (e: KeyboardEvent) => {
			if ((e.metaKey || e.ctrlKey) && e.key === 'Enter') {
				e.preventDefault();
				handleRun();
			}
		};

		window.addEventListener('keydown', handleKeyDown);
		return () => {
			window.removeEventListener('keydown', handleKeyDown);
		};
	});

	const handleQueryChange = (value: string) => {
		query = value;
	};

	const handleClear = () => {
		query = "";
	};

	const handleRun = () => {
		if (isRunning) return;
		isRunning = true;
		setTimeout(() => {
			isRunning = false;
			if (!isResultsExpanded) {
				isResultsExpanded = true;
			}
		}, 300);
	};

	const toggleResults = () => {
		isResultsExpanded = !isResultsExpanded;
	};

	// Mock query results
	const queryResults = $derived.by(() => {
		return [
			{ id: 1, client_id: "client_001", doc_type: "pdf", source_ref: "doc_123", title: "Annual Report 2024", content_hash: "a1b2c3d4" },
			{ id: 2, client_id: "client_001", doc_type: "docx", source_ref: "doc_124", title: "Q4 Financial Summary", content_hash: "e5f6g7h8" },
			{ id: 3, client_id: "client_002", doc_type: "pdf", source_ref: "doc_125", title: "Product Specification", content_hash: "i9j0k1l2" },
			{ id: 4, client_id: "client_003", doc_type: "txt", source_ref: "doc_126", title: "Architecture RFC v2", content_hash: "m3n4o5p6" },
			{ id: 5, client_id: "client_001", doc_type: "pdf", source_ref: "doc_127", title: "Compliance Audit Guidelines", content_hash: "q7r8s9t0" },
			{ id: 6, client_id: "client_004", doc_type: "docx", source_ref: "doc_128", title: "Security Playbook 2025", content_hash: "u1v2w3x4" },
			{ id: 7, client_id: "client_002", doc_type: "pdf", source_ref: "doc_129", title: "API Gateway Specifications", content_hash: "y5z6a7b8" },
			{ id: 8, client_id: "client_005", doc_type: "csv", source_ref: "doc_130", title: "Telemetry Raw Logs", content_hash: "c9d0e1f2" },
			{ id: 9, client_id: "client_003", doc_type: "json", source_ref: "doc_131", title: "Config Schema Definitions", content_hash: "g3h4i5j6" },
			{ id: 10, client_id: "client_001", doc_type: "pdf", source_ref: "doc_132", title: "Customer Privacy Notice", content_hash: "k7l8m9n0" }
		];
	});

	// Derive table metadata for TableView
	const resultTable = $derived.by<TableMetaData>(() => {
		const firstRow = queryResults[0];
		const columns = firstRow
			? Object.entries(firstRow).map(([key, val]) => ({
					name: key,
					data_type: typeof val === 'number' ? 'integer' : 'varchar',
					is_nullable: 'NO',
					column_default: ''
				}))
			: [];

		return {
			name: 'kb_documents',
			schema_name: 'public',
			columns,
			constraints: [
				{
					name: 'kb_documents_pkey',
					type: 'p',
					columns: ['id']
				}
			],
			indexes: []
		};
	});
</script>

<div class="flex flex-col h-full p-3 gap-3 overflow-hidden">
	<!-- Unified SQL Editor Container -->
	<div class="flex-1 min-h-0 flex flex-col rounded-lg border border-white/10 bg-[#231f1e] overflow-hidden shadow-sm">
		<!-- Compact Integrated Toolbar -->
		<div class="h-9 px-3 border-b border-white/10 bg-[#1a1716] flex items-center justify-between shrink-0 select-none">
			<!-- Left: Shortcut prompt -->
			<div class="flex items-center gap-1.5 text-xs text-outline font-normal">
				<span>Press</span>
				<kbd class="px-1.5 py-0.5 rounded bg-white/5 border border-white/10 text-[10px] text-on-surface-variant font-sans font-medium">
					{isMac ? '⌘ Enter' : 'Ctrl Enter'}
				</kbd>
				<span>to run</span>
			</div>

			<!-- Right: Clear action & Run button -->
			<div class="flex items-center gap-2">
				{#if query.length > 0}
					<button
						type="button"
						onclick={handleClear}
						class="flex items-center gap-1 px-2 py-0.5 text-xs text-outline hover:text-on-surface hover:bg-white/5 rounded transition-colors"
						title="Clear editor"
					>
						<RotateCcw size={11} />
						<span>Clear</span>
					</button>
				{/if}

				<Button
					variant="primary"
					size="sm"
					onclick={handleRun}
					disabled={isRunning}
					class="flex items-center gap-1.5 h-7 px-3 text-xs font-medium"
				>
					{#if isRunning}
						<Loader2 size={12} class="animate-spin" />
						<span>Running...</span>
					{:else}
						<Play size={11} class="fill-current" />
						<span>Run</span>
					{/if}
				</Button>
			</div>
		</div>

		<!-- CodeMirror Editor Area -->
		<div class="flex-1 min-h-0 overflow-hidden">
			<CodeMirrorEditor
				value={query}
				onValueChange={handleQueryChange}
				placeholder="Enter your SQL query here..."
				height="100%"
				minHeight="0"
				class="h-full w-full"
			/>
		</div>
	</div>

	<!-- Collapsible Results Panel -->
	<CollapsiblePanel
		expanded={isResultsExpanded}
		onToggle={toggleResults}
		class="rounded-lg border border-white/10 bg-[#1a1716] overflow-hidden"
	>
		{#snippet headerSlot()}
			<div class="flex items-center gap-2">
				<Typography variant="p" class="text-xs text-on-surface font-medium">Results</Typography>
				<span class="text-xs text-outline font-normal">({queryResults.length} rows)</span>
			</div>
		{/snippet}

		{#snippet children()}
			<div class="p-3 h-full min-h-0 bg-secondary">
				<TableView table={resultTable} data={queryResults} pageSize={5} />
			</div>
		{/snippet}
	</CollapsiblePanel>
</div>
