<script lang="ts">
	import { tv } from 'tailwind-variants';
	import {
		Key,
		ArrowUp,
		ArrowDown,
		Copy,
		Check,
		X
	} from '@lucide/svelte';
	import Typography from '#lib/components/primitives/Typography.svelte';
	import Button from '#lib/components/primitives/Button.svelte';
	import type { Constraint } from '#lib/types.ts';
	import type {
		TableViewProps,
		TableViewTab,
		TableSortState
	} from './types/TableView';

	let {
		table,
		data,
		class: className = '',
		pageSize = 25,
		showRowNumbers = true,
		onRowClick
	}: TableViewProps = $props();

	// Local UI state
	let activeTab = $state<TableViewTab>('data');
	let sortState = $state<TableSortState>({ column: '', direction: null });
	let currentPage = $state(1);
	let currentPageSize = $state(pageSize);
	let copiedValue = $state<string | null>(null);
	let copyTimeout: ReturnType<typeof setTimeout> | null = null;

	const handlePageSizeChange = (newSize: number) => {
		currentPageSize = newSize;
		currentPage = 1;
	};

	// Extract constraints
	const primaryKeys = $derived.by(() => {
		const keys = new Set<string>();
		table.constraints?.forEach((constraint: Constraint) => {
			if (constraint.type === 'p' || constraint.type?.toLowerCase() === 'primary key') {
				constraint.columns?.forEach((col: string) => keys.add(col));
			}
		});
		return keys;
	});

	const foreignKeys = $derived.by(() => {
		const keys = new Map<string, Constraint>();
		table.constraints?.forEach((constraint: Constraint) => {
			if (constraint.type === 'f' || constraint.type?.toLowerCase() === 'foreign key') {
				constraint.columns?.forEach((col: string) => keys.set(col, constraint));
			}
		});
		return keys;
	});

	const uniqueColumns = $derived.by(() => {
		const cols = new Set<string>();
		table.constraints?.forEach((constraint: Constraint) => {
			if (constraint.type === 'u' || constraint.type?.toLowerCase() === 'unique') {
				constraint.columns?.forEach((col: string) => cols.add(col));
			}
		});
		return cols;
	});

	// Normalize table data
	const tableData = $derived(data || []);

	// Default tab selection if data is absent
	$effect(() => {
		if (tableData.length === 0 && (!data || data.length === 0)) {
			activeTab = 'structure';
		} else {
			activeTab = 'data';
		}
	});

	// Sort rows
	const sortedData = $derived.by(() => {
		if (!sortState.column || !sortState.direction) {
			return tableData;
		}

		const { column, direction } = sortState;
		const dirMultiplier = direction === 'asc' ? 1 : -1;

		return [...tableData].sort((a, b) => {
			const valA = a[column];
			const valB = b[column];

			if (valA === valB) return 0;
			if (valA === null || valA === undefined) return 1;
			if (valB === null || valB === undefined) return -1;

			if (typeof valA === 'number' && typeof valB === 'number') {
				return (valA - valB) * dirMultiplier;
			}

			return String(valA).localeCompare(String(valB)) * dirMultiplier;
		});
	});

	// Pagination
	const totalPages = $derived(Math.max(1, Math.ceil(sortedData.length / currentPageSize)));
	const paginatedData = $derived.by(() => {
		const start = (currentPage - 1) * currentPageSize;
		return sortedData.slice(start, start + currentPageSize);
	});

	const visiblePages = $derived.by(() => {
		const pages: (number | '...')[] = [];
		if (totalPages <= 7) {
			for (let i = 1; i <= totalPages; i++) {
				pages.push(i);
			}
			return pages;
		}

		pages.push(1);
		if (currentPage - 2 > 2) {
			pages.push('...');
		}

		const start = Math.max(2, currentPage - 1);
		const end = Math.min(totalPages - 1, currentPage + 1);

		for (let i = start; i <= end; i++) {
			pages.push(i);
		}

		if (currentPage + 1 < totalPages - 1) {
			pages.push('...');
		}

		pages.push(totalPages);
		return pages;
	});

	const handleColumnSort = (columnName: string) => {
		if (sortState.column !== columnName) {
			sortState = { column: columnName, direction: 'asc' };
		} else if (sortState.direction === 'asc') {
			sortState = { column: columnName, direction: 'desc' };
		} else {
			sortState = { column: '', direction: null };
		}
	};

	const copyToClipboard = async (text: string, identifier: string) => {
		try {
			await navigator.clipboard.writeText(text);
			copiedValue = identifier;
			if (copyTimeout) clearTimeout(copyTimeout);
			copyTimeout = setTimeout(() => {
				copiedValue = null;
			}, 1500);
		} catch {
			// Clipboard write fallback
		}
	};

	// Clean, minimal tailwind-variants definitions
	const tableContainer = tv({
		base: 'flex flex-col h-full bg-[#1b1716] text-on-surface rounded-lg border border-white/10 overflow-hidden'
	});

	const tabBtn = tv({
		base: 'px-3 py-1.5 text-xs font-medium cursor-pointer transition-colors border-b-2',
		variants: {
			active: {
				true: 'text-on-surface border-primary',
				false: 'text-outline border-transparent hover:text-on-surface-variant'
			}
		}
	});

	const headerCell = tv({
		base: 'px-3 py-2 text-left font-medium text-xs text-on-surface-variant border-b border-r border-white/10 select-none group transition-colors hover:text-on-surface'
	});

	const bodyCell = tv({
		base: 'px-3 py-2 text-xs border-r border-white/5 text-on-surface transition-colors'
	});
</script>

<div class={tableContainer({ class: className })}>
	<!-- Header -->
	<div class="px-3.5 py-2.5 border-b border-white/10 bg-[#211d1c] flex items-center justify-between gap-3">
		<div class="flex items-center gap-2 min-w-0">
			<Typography variant="h3" class="text-xs font-medium text-on-surface truncate">
				{table.name}
			</Typography>
			<span class="text-xs text-outline/50">·</span>
			<span class="text-xs text-outline truncate">{table.schema_name}</span>
			<span class="text-xs text-outline/50">·</span>
			<span class="text-xs text-outline">
				{tableData.length > 0 ? `${tableData.length} rows` : `${table.columns.length} columns`}
			</span>
		</div>

		<!-- Minimal Tabs -->
		<div class="flex items-center gap-1" role="tablist" aria-label="Table views">
			<button
				type="button"
				role="tab"
				aria-selected={activeTab === 'data'}
				class={tabBtn({ active: activeTab === 'data' })}
				onclick={() => (activeTab = 'data')}
			>
				Data
			</button>
			<button
				type="button"
				role="tab"
				aria-selected={activeTab === 'structure'}
				class={tabBtn({ active: activeTab === 'structure' })}
				onclick={() => (activeTab = 'structure')}
			>
				Columns
			</button>
		</div>
	</div>

	<!-- Tab 1: Data View -->
	{#if activeTab === 'data'}
		<!-- Table Grid -->
		<div class="flex-1 overflow-auto bg-[#1b1716]">
			{#if paginatedData.length === 0}
				<div class="flex flex-col items-center justify-center h-full min-h-[160px] p-6 text-center">
					<p class="text-xs text-outline mb-2">No rows found in this table</p>
					<Button variant="ghost" size="sm" onclick={() => (activeTab = 'structure')}>
						View column structure
					</Button>
				</div>
			{:else}
				<table class="w-full text-xs border-collapse table-fixed min-w-full">
					<colgroup>
						{#if showRowNumbers}
							<col class="w-10" />
						{/if}
						{#each table.columns as _col}
							<col style="min-width: 140px;" />
						{/each}
					</colgroup>
					<thead class="sticky top-0 z-10 bg-[#211d1c] border-b border-white/10">
						<tr>
							{#if showRowNumbers}
								<th class="w-10 px-2 py-2 text-center text-[11px] text-outline/60 border-b border-r border-white/10 bg-[#211d1c]">
									#
								</th>
							{/if}
							{#each table.columns as column}
								{@const isPrimary = primaryKeys.has(column.name)}
								{@const isCurrentSort = sortState.column === column.name}

								<th
									class="{headerCell()} min-w-[140px] whitespace-nowrap cursor-pointer"
									onclick={() => handleColumnSort(column.name)}
								>
									<div class="flex items-center justify-between gap-2 min-w-0">
										<div class="flex items-center gap-1.5 min-w-0 truncate">
											{#if isPrimary}
												<span title="Primary Key" class="text-primary/80 flex-shrink-0">
													<Key size={11} />
												</span>
											{/if}
											<span class="truncate font-medium {isPrimary ? 'text-primary/90' : 'text-on-surface'}">
												{column.name}
											</span>
											<span class="text-[11px] text-outline/70 flex-shrink-0">
												{column.data_type}
											</span>
										</div>

										<div class="w-3.5 h-3.5 flex items-center justify-center flex-shrink-0">
											{#if isCurrentSort && sortState.direction === 'asc'}
												<ArrowUp size={11} class="text-primary" />
											{:else if isCurrentSort && sortState.direction === 'desc'}
												<ArrowDown size={11} class="text-primary" />
											{/if}
										</div>
									</div>
								</th>
							{/each}
						</tr>
					</thead>
					<tbody>
						{#each paginatedData as row, rowIndex}
							{@const absoluteIndex = (currentPage - 1) * pageSize + rowIndex + 1}
							<tr
								class="border-b border-white/5 hover:bg-white/[0.02] transition-colors group"
								onclick={() => onRowClick?.(row, absoluteIndex - 1)}
							>
								{#if showRowNumbers}
									<td class="w-10 px-2 py-1.5 text-center text-[11px] text-outline/40 border-r border-white/5 select-none">
										{absoluteIndex}
									</td>
								{/if}
								{#each table.columns as column}
									{@const val = row[column.name]}
									{@const cellKey = `${absoluteIndex}-${column.name}`}
									{@const isCopied = copiedValue === cellKey}

									<td class="{bodyCell()} min-w-[140px] truncate whitespace-nowrap">
										<div class="flex items-center justify-between gap-1.5 group/cell min-w-0">
											<span class="truncate min-w-0">
												{#if val === null || val === undefined}
													<span class="text-outline/40 italic">null</span>
												{:else if typeof val === 'boolean'}
													<span class="text-outline">{val ? 'true' : 'false'}</span>
												{:else}
													<span>{String(val)}</span>
												{/if}
											</span>

											{#if val !== null && val !== undefined}
												<button
													type="button"
													class="opacity-0 group-hover/cell:opacity-100 text-outline/60 hover:text-on-surface transition-opacity p-0.5 cursor-pointer flex-shrink-0"
													title="Copy"
													onclick={(e) => {
														e.stopPropagation();
														copyToClipboard(String(val), cellKey);
													}}
												>
													{#if isCopied}
														<Check size={11} class="text-primary" />
													{:else}
														<Copy size={11} />
													{/if}
												</button>
											{/if}
										</div>
									</td>
								{/each}
							</tr>
						{/each}
					</tbody>
				</table>
			{/if}
		</div>

		<!-- Pagination Footer -->
		{#if sortedData.length > 0}
			<div class="px-3.5 py-2 border-t border-white/10 bg-[#211d1c] flex flex-wrap items-center justify-between text-xs text-outline gap-2">
				<div class="flex items-center gap-3">
					<span>{Math.min(sortedData.length, (currentPage - 1) * currentPageSize + 1)}–{Math.min(sortedData.length, currentPage * currentPageSize)} of {sortedData.length}</span>

					<div class="flex items-center gap-1.5 text-xs text-outline">
						<span>Rows:</span>
						<select
							value={currentPageSize}
							onchange={(e) => handlePageSizeChange(Number((e.target as HTMLSelectElement).value))}
							class="bg-[#1b1716] border border-white/10 rounded px-1.5 py-0.5 text-xs text-on-surface outline-none cursor-pointer hover:border-white/20 transition-colors"
						>
							<option value={5}>5</option>
							<option value={10}>10</option>
							<option value={25}>25</option>
							<option value={50}>50</option>
						</select>
					</div>

					{#if sortState.column}
						<span class="text-outline/40">·</span>
						<button
							type="button"
							class="text-xs text-outline hover:text-on-surface cursor-pointer flex items-center gap-1"
							onclick={() => (sortState = { column: '', direction: null })}
						>
							<span>sorted by {sortState.column} ({sortState.direction})</span>
							<X size={11} />
						</button>
					{/if}
				</div>

				<div class="flex items-center gap-3">
					<Button
						variant="ghost"
						size="sm"
						class="flex items-center gap-1 text-xs px-2 py-0.5 text-outline hover:text-on-surface"
						onclick={() => copyToClipboard(JSON.stringify(sortedData, null, 2), 'table-json')}
						title="Copy data as JSON"
					>
						{#if copiedValue === 'table-json'}
							<Check size={12} class="text-primary" />
							<span class="text-primary text-xs">Copied</span>
						{:else}
							<Copy size={12} />
							<span class="text-xs">JSON</span>
						{/if}
					</Button>

					{#if totalPages > 1}
						<div class="flex items-center gap-1">
							<Button
								variant="ghost"
								size="xs"
								disabled={currentPage <= 1}
								onclick={() => (currentPage = Math.max(1, currentPage - 1))}
								class="w-6 h-6 p-0 text-xs text-outline hover:text-on-surface disabled:opacity-25 disabled:cursor-not-allowed flex items-center justify-center rounded"
								aria-label="Previous page"
							>
								<span>&lt;</span>
							</Button>

							{#each visiblePages as pageItem}
								{#if pageItem === '...'}
									<span class="px-1 text-xs text-outline/40 select-none">...</span>
								{:else}
									<button
										type="button"
										class="w-6 h-6 text-xs rounded transition-colors cursor-pointer select-none flex items-center justify-center {currentPage === pageItem ? 'text-primary font-medium bg-primary/10' : 'text-outline hover:text-on-surface hover:bg-white/5'}"
										onclick={() => (currentPage = pageItem)}
									>
										{pageItem}
									</button>
								{/if}
							{/each}

							<Button
								variant="ghost"
								size="xs"
								disabled={currentPage >= totalPages}
								onclick={() => (currentPage = Math.min(totalPages, currentPage + 1))}
								class="w-6 h-6 p-0 text-xs text-outline hover:text-on-surface disabled:opacity-25 disabled:cursor-not-allowed flex items-center justify-center rounded"
								aria-label="Next page"
							>
								<span>&gt;</span>
							</Button>
						</div>
					{/if}
				</div>
			</div>
		{/if}

	<!-- Tab 2: Columns / Structure View -->
	{:else if activeTab === 'structure'}
		<div class="flex-1 overflow-auto bg-[#1b1716]">
			<table class="w-full text-xs border-collapse table-fixed min-w-full">
				<colgroup>
					<col style="width: 25%; min-width: 140px;" />
					<col style="width: 20%; min-width: 110px;" />
					<col style="width: 15%; min-width: 90px;" />
					<col style="width: 15%; min-width: 90px;" />
					<col style="width: 25%; min-width: 140px;" />
				</colgroup>
				<thead class="sticky top-0 z-10 bg-[#211d1c] border-b border-white/10">
					<tr>
						<th class="px-3.5 py-2 text-left font-medium text-on-surface-variant border-b border-r border-white/10">Column</th>
						<th class="px-3.5 py-2 text-left font-medium text-on-surface-variant border-b border-r border-white/10">Type</th>
						<th class="px-3.5 py-2 text-left font-medium text-on-surface-variant border-b border-r border-white/10">Nullable</th>
						<th class="px-3.5 py-2 text-left font-medium text-on-surface-variant border-b border-r border-white/10">Default</th>
						<th class="px-3.5 py-2 text-left font-medium text-on-surface-variant border-b border-white/10">Details</th>
					</tr>
				</thead>
				<tbody>
					{#each table.columns as column}
						{@const isPrimary = primaryKeys.has(column.name)}
						{@const foreignKey = foreignKeys.get(column.name)}
						{@const isUnique = uniqueColumns.has(column.name)}

						<tr class="border-b border-white/5 hover:bg-white/[0.02] transition-colors">
							<td class="px-3.5 py-2 font-medium text-on-surface border-r border-white/5">
								<div class="flex items-center gap-1.5">
									{#if isPrimary}
										<span title="Primary Key" class="text-primary/80">
											<Key size={11} />
										</span>
									{/if}
									<span class={isPrimary ? 'text-primary' : ''}>{column.name}</span>
								</div>
							</td>
							<td class="px-3.5 py-2 text-outline border-r border-white/5">
								{column.data_type}
							</td>
							<td class="px-3.5 py-2 text-outline border-r border-white/5">
								{column.is_nullable?.toUpperCase() === 'YES' ? 'yes' : 'no'}
							</td>
							<td class="px-3.5 py-2 text-outline/70 border-r border-white/5">
								{column.column_default || '—'}
							</td>
							<td class="px-3.5 py-2 text-outline">
								{#if isPrimary}
									<span class="text-primary">primary key</span>
								{:else if foreignKey}
									<span>references {foreignKey.referenced_table}</span>
								{:else if isUnique}
									<span>unique</span>
								{:else}
									<span class="text-outline/40">—</span>
								{/if}
							</td>
						</tr>
					{/each}
				</tbody>
			</table>
		</div>
	{/if}
</div>
