import type { TableMetaData } from '#lib/types.ts';

export interface TableViewSidebarProps {
	isOpen?: boolean;
	selectedTable?: string | null;
	tables?: TableMetaData[];
	tableDataMap?: Record<string, Record<string, unknown>[]>;
	data?: Record<string, unknown>[];
	onToggle?: () => void;
	class?: string;
	defaultWidth?: number;
	minWidth?: number;
	maxWidth?: number;
}
