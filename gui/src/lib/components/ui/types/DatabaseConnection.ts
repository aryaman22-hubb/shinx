export interface DatabaseConnectionProps {
	open?: boolean;
	onClose?: () => void;
	onConnect?: (connection: DatabaseConnectionData) => void;
	targetElement?: HTMLElement;
}

export interface DatabaseConnectionData {
	host: string;
	port: string;
	dbname: string;
	user: string;
	password: string;
}

