export interface Book {
    id: number;
    title: string;
    author: string;
    edition: string;
    price: number;
    category_id: number;
}

export interface Category {
    id: number;
    name: string;
}