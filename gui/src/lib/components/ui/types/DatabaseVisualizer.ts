import type { DBMetadata } from '#lib/types.ts';

export interface DatabaseVisualizerProps {
	databaseName: string;
	schemaName: string;
	metadata: DBMetadata;
	class?: string;
	onTableSelect?: (tableName: string) => void;
}
