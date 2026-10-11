export interface SidebarItem {
	icon: any;
	label: string;
	href: string;
}

export interface MainSidebarProps {
	topItems?: SidebarItem[];
	bottomItems?: SidebarItem[];
	class?: string;
}
