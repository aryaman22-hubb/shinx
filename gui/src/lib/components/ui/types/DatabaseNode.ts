export interface IndexData {
	name: string;
	definition: string;
	columns: string[];
	isUnique?: boolean;
}

export interface ColumnData {
	name: string;
	dataType: string;
	isNullable: string;
	isPrimaryKey?: boolean;
	isForeignKey?: boolean;
	isUnique?: boolean;
	isCheck?: boolean;
	checkDefinition?: string;
	referencedTable?: string;
	referencedColumn?: string;
}

export interface DatabaseNodeData {
	name: string;
	schemaName: string;
	type: 'table' | 'view' | 'materialized_view';
	columns?: ColumnData[];
	indexes?: IndexData[];
	definition?: string | null;
	onSelect?: () => void;
	[key: string]: unknown;
}

export interface DatabaseNodeProps {
	data: DatabaseNodeData;
}
