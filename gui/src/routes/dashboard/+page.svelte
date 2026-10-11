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

	const mockTableData: Record<string, Record<string, unknown>[]> = {
		users: [
			{ id: 1, email: 'alice.walker@example.com', name: 'Alice Walker', age: 29, created_at: '2024-01-10 08:30:00' },
			{ id: 2, email: 'bob.harris@example.com', name: 'Bob Harris', age: 34, created_at: '2024-01-12 11:15:00' },
			{ id: 3, email: 'charlie.brown@example.com', name: 'Charlie Brown', age: 24, created_at: '2024-01-15 14:20:00' },
			{ id: 4, email: 'diana.ross@example.com', name: 'Diana Ross', age: 41, created_at: '2024-01-18 09:45:00' },
			{ id: 5, email: 'ethan.hunt@example.com', name: 'Ethan Hunt', age: 37, created_at: '2024-01-20 16:10:00' },
			{ id: 6, email: 'fiona.gallagher@example.com', name: 'Fiona Gallagher', age: 28, created_at: '2024-01-22 13:05:00' },
			{ id: 7, email: 'george.clark@example.com', name: 'George Clark', age: 52, created_at: '2024-01-25 17:40:00' },
			{ id: 8, email: 'hannah.abbott@example.com', name: 'Hannah Abbott', age: 22, created_at: '2024-01-28 10:25:00' },
			{ id: 9, email: 'ian.wright@example.com', name: 'Ian Wright', age: 31, created_at: '2024-02-01 12:50:00' },
			{ id: 10, email: 'julia.roberts@example.com', name: 'Julia Roberts', age: 45, created_at: '2024-02-04 15:30:00' },
			{ id: 11, email: 'kevin.bacon@example.com', name: 'Kevin Bacon', age: 39, created_at: '2024-02-08 09:10:00' },
			{ id: 12, email: 'laura.croft@example.com', name: 'Laura Croft', age: 27, created_at: '2024-02-12 18:00:00' }
		],
		orders: [
			{ id: 101, user_id: 1, total: '149.50', status: 'completed' },
			{ id: 102, user_id: 2, total: '89.99', status: 'completed' },
			{ id: 103, user_id: 1, total: '34.20', status: 'pending' },
			{ id: 104, user_id: 4, total: '299.00', status: 'processing' },
			{ id: 105, user_id: 3, total: '15.99', status: 'cancelled' },
			{ id: 106, user_id: 5, total: '450.75', status: 'completed' },
			{ id: 107, user_id: 7, total: '120.00', status: 'completed' },
			{ id: 108, user_id: 2, total: '65.40', status: 'pending' },
			{ id: 109, user_id: 6, total: '210.30', status: 'completed' },
			{ id: 110, user_id: 8, total: '78.50', status: 'processing' },
			{ id: 111, user_id: 9, total: '512.00', status: 'completed' },
			{ id: 112, user_id: 10, total: '94.25', status: 'completed' }
		],
		products: [
			{ id: 501, name: 'Pro Wireless Keyboard', sku: 'KB-WL-01', price: '129.99', stock: 45 },
			{ id: 502, name: 'Ergonomic Vertical Mouse', sku: 'MS-ERG-02', price: '69.50', stock: 120 },
			{ id: 503, name: '4K UltraSharp Monitor 27"', sku: 'MN-4K-27', price: '449.00', stock: 18 },
			{ id: 504, name: 'USB-C Aluminum Dock 10-in-1', sku: 'DK-USBC-10', price: '89.95', stock: 64 },
			{ id: 505, name: 'Noise-Cancelling Headphones', sku: 'HP-NC-BT', price: '249.99', stock: 32 },
			{ id: 506, name: 'Desk Mat Felt & Leather', sku: 'AC-MAT-GR', price: '29.00', stock: 150 },
			{ id: 507, name: 'Adjustable Laptop Stand', sku: 'ST-LPT-AL', price: '45.00', stock: 85 },
			{ id: 508, name: 'Mechanical Keycaps PBT Set', sku: 'AC-KCP-PBT', price: '39.99', stock: 70 },
			{ id: 509, name: 'Webcam 1080p 60fps', sku: 'WC-HD-60', price: '79.99', stock: 40 },
			{ id: 510, name: 'Studio Cardioid Microphone', sku: 'MC-USB-ST', price: '119.00', stock: 25 },
			{ id: 511, name: 'Cable Management Tray', sku: 'AC-CBL-TR', price: '24.50', stock: 95 }
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
		tableDataMap={mockTableData}
		onToggle={toggleSidebar}
	/>
</div>
