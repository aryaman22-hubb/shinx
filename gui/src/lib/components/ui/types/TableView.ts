import type { TableMetaData } from '#lib/types.ts';

export type TableViewTab = 'data' | 'structure';

export type SortDirection = 'asc' | 'desc' | null;

export interface TableSortState {
	column: string;
	direction: SortDirection;
}

export interface TableViewProps {
	table: TableMetaData;
	data?: Record<string, unknown>[];
	class?: string;
	pageSize?: number;
	showRowNumbers?: boolean;
	onRowClick?: (row: Record<string, unknown>, index: number) => void;
}

