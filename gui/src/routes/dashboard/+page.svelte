<script lang="ts">
	import type { DBMetadata } from '#lib/types.ts';

	import DatabaseVisualizer from '#lib/components/ui/DatabaseVisualizer.svelte';
	import TableViewSidebar from '#lib/components/ui/TableViewSidebar.svelte';

	let isSidebarOpen = $state(false);
	let selectedTable = $state<string | null>(null);

	const toggleSidebar = () => {
		isSidebarOpen = !isSidebarOpen;
	};

	const sampleMetadata: DBMetadata = {
		version: '1.0',
		extensions: [],
		tables: [
			{
				name: 'users',
				schema_name: 'public',
				columns: [
					{ name: 'id', data_type: 'integer', is_nullable: 'NO', column_default: 'nextval()' },
					{ name: 'email', data_type: 'varchar(255)', is_nullable: 'NO', column_default: '' },
					{ name: 'name', data_type: 'varchar(100)', is_nullable: 'YES', column_default: '' },
					{ name: 'age', data_type: 'integer', is_nullable: 'YES', column_default: '' },
					{ name: 'created_at', data_type: 'timestamp', is_nullable: 'NO', column_default: 'now()' }
				],
				constraints: [
					{
						name: 'users_pkey',
						type: 'p',
						columns: ['id'],
						referenced_columns: []
					},
					{
						name: 'users_email_key',
						type: 'u',
						columns: ['email'],
						referenced_columns: []
					},
					{
						name: 'users_age_check',
						type: 'c',
						columns: ['age'],
						definition: 'age >= 18',
						referenced_columns: []
					}
				],
				indexes: [
					{ name: 'users_name_idx', indexdef: 'CREATE INDEX users_name_idx ON users (name)' },
					{ name: 'users_email_idx', indexdef: 'CREATE UNIQUE INDEX users_email_idx ON users (email)' }
				]
			},
			{
				name: 'orders',
				schema_name: 'public',
				columns: [
					{ name: 'id', data_type: 'integer', is_nullable: 'NO', column_default: 'nextval()' },
					{ name: 'user_id', data_type: 'integer', is_nullable: 'NO', column_default: '' },
					{ name: 'total', data_type: 'decimal(10,2)', is_nullable: 'NO', column_default: '' },
					{ name: 'status', data_type: 'varchar(50)', is_nullable: 'NO', column_default: '' }
				],
				constraints: [
					{
						name: 'orders_pkey',
						type: 'p',
						columns: ['id'],
						referenced_columns: []
					},
					{
						name: 'orders_user_id_fkey',
						type: 'f',
						columns: ['user_id'],
						referenced_table: 'users',
						referenced_columns: ['id']
					},
					{
						name: 'orders_total_check',
						type: 'c',
						columns: ['total'],
						definition: 'total > 0',
						referenced_columns: []
					}
				],
				indexes: [
					{ name: 'orders_user_id_idx', indexdef: 'CREATE INDEX orders_user_id_idx ON orders (user_id)' }
				]
			},
			{
				name: 'products',
				schema_name: 'public',
				columns: [
					{ name: 'id', data_type: 'integer', is_nullable: 'NO', column_default: 'nextval()' },
					{ name: 'name', data_type: 'varchar(255)', is_nullable: 'NO', column_default: '' },
					{ name: 'sku', data_type: 'varchar(50)', is_nullable: 'NO', column_default: '' },
					{ name: 'price', data_type: 'decimal(10,2)', is_nullable: 'NO', column_default: '' },
					{ name: 'stock', data_type: 'integer', is_nullable: 'NO', column_default: '0' }
				],
				constraints: [
					{
						name: 'products_pkey',
						type: 'p',
						columns: ['id'],
						referenced_columns: []
					},
					{
						name: 'products_sku_key',
						type: 'u',
						columns: ['sku'],
						referenced_columns: []
					},
					{
						name: 'products_price_check',
						type: 'c',
						columns: ['price'],
						definition: 'price >= 0',
						referenced_columns: []
					}
				],
				indexes: [
					{ name: 'products_name_idx', indexdef: 'CREATE INDEX products_name_idx ON products (name)' }
				]
			}
		],
		views: [
			{
				name: 'user_orders',
				schema_name: 'public',
				owner: 'admin',
				definition: 'SELECT u.name, o.total FROM users u JOIN orders o ON u.id = o.user_id',
				is_updatable: false,
				is_insertable_into: false,
				is_trigger_updatable: false,
				is_trigger_deletable: false,
				is_trigger_insertable_into: false,
				is_materialized: false,
				description: 'User order summary view',
				columns: [
					{ column_name: 'name', ordinal_position: 1, data_type: 'varchar(100)', is_nullable: 'YES' },
					{ column_name: 'total', ordinal_position: 2, data_type: 'decimal(10,2)', is_nullable: 'YES' }
				]
			},
			{
				name: 'order_summary',
				schema_name: 'public',
				owner: 'admin',
				definition: 'SELECT user_id, COUNT(*) as order_count, SUM(total) as total_spent FROM orders GROUP BY user_id',
				is_updatable: false,
				is_insertable_into: false,
				is_trigger_updatable: false,
				is_trigger_deletable: false,
				is_trigger_insertable_into: false,
				is_materialized: true,
				description: 'Materialized view for order summaries',
				columns: [
					{ column_name: 'user_id', ordinal_position: 1, data_type: 'integer', is_nullable: 'NO' },
					{ column_name: 'order_count', ordinal_position: 2, data_type: 'bigint', is_nullable: 'NO' },
					{ column_name: 'total_spent', ordinal_position: 3, data_type: 'decimal(10,2)', is_nullable: 'NO' }
				]
			}
		]
	};
</script>

<div class="p-4 h-full flex gap-4">
	<div class="flex-1">
		<DatabaseVisualizer
			databaseName="mydb"
			schemaName="public"
			metadata={sampleMetadata}
			onTableSelect={(tableName) => {
				selectedTable = tableName;
				if (!isSidebarOpen) {
					isSidebarOpen = true;
				}
			}}
		/>
	</div>

	<!-- Collapsible sidebar -->
	<TableViewSidebar
		isOpen={isSidebarOpen}
		selectedTable={selectedTable}
		tables={sampleMetadata.tables}
		onToggle={toggleSidebar}
	/>
</div>
