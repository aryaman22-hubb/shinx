import type { TableMetaData } from '#lib/types.ts';

export interface TableViewSidebarProps {
	isOpen?: boolean;
	selectedTable?: string | null;
	tables?: TableMetaData[];
	onToggle?: () => void;
	class?: string;
}
