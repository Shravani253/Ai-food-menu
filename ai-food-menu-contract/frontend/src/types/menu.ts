export type Status = "Fresh" | "Caution" | "Unavailable";

export interface MenuItem {
    id: number;
    name: string;
    category: string;
    price: number;
    status: Status;
    availability: string;
    priority: number;
    warnings: string[];
}
