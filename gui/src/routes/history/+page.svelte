<script lang="ts">
	import type { TableMetaData, Column } from '#lib/types.ts';
	import TableView from '#lib/components/ui/TableView.svelte';

	// Create a TableMetaData structure for query history
	const historyTable: TableMetaData = {
		name: 'query_history',
		schema_name: 'public',
		columns: [
			{ name: 'timestamp', data_type: 'timestamp', is_nullable: 'NO', column_default: 'now()' },
			{ name: 'query', data_type: 'text', is_nullable: 'NO', column_default: '' },
			{ name: 'duration', data_type: 'varchar', is_nullable: 'NO', column_default: '' },
			{ name: 'status', data_type: 'varchar', is_nullable: 'NO', column_default: '' },
			{ name: 'rows', data_type: 'integer', is_nullable: 'YES', column_default: '0' }
		] as Column[],
		constraints: [],
		indexes: []
	};

	// Query history data
	const historyData = [
		{
			timestamp: '2024-01-15 10:30:00',
			query: 'SELECT * FROM users WHERE age > 25',
			duration: '125ms',
			status: 'success',
			rows: 15
		},
		{
			timestamp: '2024-01-15 11:45:00',
			query: 'SELECT name, email FROM users ORDER BY created_at DESC LIMIT 10',
			duration: '89ms',
			status: 'success',
			rows: 10
		},
		{
			timestamp: '2024-01-15 14:20:00',
			query: 'SELECT * FROM orders WHERE status = "pending"',
			duration: '234ms',
			status: 'success',
			rows: 42
		},
		{
			timestamp: '2024-01-16 09:15:00',
			query: 'SELECT COUNT(*) FROM products WHERE stock < 10',
			duration: '45ms',
			status: 'success',
			rows: 1
		},
		{
			timestamp: '2024-01-16 16:30:00',
			query: 'SELECT * FROM invalid_table',
			duration: '12ms',
			status: 'error',
			rows: 0
		}
	];
</script>

<div class="p-4 h-full">
	<TableView table={historyTable} data={historyData} />
</div>
