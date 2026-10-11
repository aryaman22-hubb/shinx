<script lang="ts">
	import Modal from '#lib/components/primitives/Modal.svelte';
	import Button from '#lib/components/primitives/Button.svelte';
	import Input from '#lib/components/primitives/Input.svelte';
	import Typography from '#lib/components/primitives/Typography.svelte';
	import Picker from '#lib/components/primitives/Picker.svelte';
	import { Lock, Server, User, Key, Database } from '@lucide/svelte';
	import type { DatabaseConnectionProps, DatabaseConnectionData } from './types/DatabaseConnection';

	let { open = false, onClose, onConnect, targetElement }: DatabaseConnectionProps = $props();

	let selectedDialect = $state<{ label: string; value: string }>({ label: "PostgreSQL", value: "postgres" });
	let host = $state("localhost");
	let port = $state("5432");
	let dbname = $state("postgres");
	let user = $state("postgres");
	let password = $state("");
	let isLoading = $state(false);

	const dialectOptions: Array<{ label: string; value: string }> = [
		{ label: "PostgreSQL", value: "postgres" },
		{ label: "MySQL", value: "mysql" },
		{ label: "SQLite", value: "sqlite" }
	];

	const handleDialectSelect = (item: { label: string; value: string } | string) => {
		if (typeof item === 'string') {
			selectedDialect = { label: item, value: item };
		} else {
			selectedDialect = item;
		}
		// Update default port based on dialect
		if (selectedDialect.value === "mysql") {
			port = "3306";
		} else if (selectedDialect.value === "postgres") {
			port = "5432";
		} else if (selectedDialect.value === "sqlite") {
			port = "";
		}
	};

	function handleConnect() {
		const connectionData: DatabaseConnectionData = {
			host,
			port,
			dbname,
			user,
			password
		};

		if (onConnect) {
			isLoading = true;
			// Simulate async connection
			setTimeout(() => {
				onConnect(connectionData);
				isLoading = false;
				handleClose();
			}, 500);
		}
	}

	function handleClose() {
		if (onClose) {
			onClose();
		}
		// Reset form
		host = "localhost";
		port = "5432";
		dbname = "postgres";
		user = "postgres";
		password = "";
	}
</script>

<Modal open={open} variant="positioned" onClose={handleClose} {targetElement} backdropBlur={false}>
	<div class="py-5 px-6 w-full min-w-[800px]">
		<div class="mb-10">
			<Typography variant="h3">Connect to Database</Typography>
			<Typography variant="p" class="text-on-surface-variant text-sm">Enter your connection details</Typography>
		</div>

		<div class="mb-4">
			<Picker
				label="Database Type"
				value={selectedDialect}
				items={dialectOptions}
				onSelect={handleDialectSelect}
			/>
		</div>

		<div class="grid grid-cols-2 gap-4 mb-4">
			<div>
				<label for="db-host" class="block text-sm text-on-surface-variant mb-1.5">Host</label>
				<Input
					id="db-host"
					bind:value={host}
					placeholder="localhost"
				>
					{#snippet leftIcon()}
						<Server size={16} />
					{/snippet}
				</Input>
			</div>

			<div>
				<label for="db-port" class="block text-sm text-on-surface-variant mb-1.5">Port</label>
				<Input
					id="db-port"
					bind:value={port}
					placeholder="5432"
					class="[appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none"
				>
					{#snippet leftIcon()}
						<Key size={16} />
					{/snippet}
				</Input>
			</div>
		</div>

		<div class="grid grid-cols-2 gap-4 mb-4">
			<div>
				<label for="db-name" class="block text-sm text-on-surface-variant mb-1.5">Database Name</label>
				<Input
					id="db-name"
					bind:value={dbname}
					placeholder="postgres"
				>
					{#snippet leftIcon()}
						<Database size={16} />
					{/snippet}
				</Input>
			</div>

			<div>
				<label for="db-user" class="block text-sm text-on-surface-variant mb-1.5">Username</label>
				<Input
					id="db-user"
					bind:value={user}
					placeholder="postgres"
				>
					{#snippet leftIcon()}
						<User size={16} />
					{/snippet}
				</Input>
			</div>
		</div>

		<div class="mb-4">
			<label for="db-password" class="block text-sm text-on-surface-variant mb-1.5">Password</label>
			<Input
				id="db-password"
				bind:value={password}
				placeholder="••••••••"
				type="password"
			>
				{#snippet leftIcon()}
					<Lock size={16} />
				{/snippet}
			</Input>
		</div>

		<div class="flex justify-end gap-3">
			<Button
				variant="secondary"
				onclick={handleClose}
			>
				Cancel
			</Button>
			<Button
				variant="primary"
				onclick={handleConnect}
				disabled={isLoading}
			>
				{#if isLoading}
					<div class="flex items-center gap-2">
						<div class="w-4 h-4 border-2 border-on-primary border-t-transparent rounded-full animate-spin"></div>
						Connecting...
					</div>
				{:else}
					Connect
				{/if}
			</Button>
		</div>
	</div>
</Modal>
