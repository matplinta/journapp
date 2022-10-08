export interface IUserProfile {
    email: string;
    is_active: boolean;
    is_superuser: boolean;
    full_name: string;
    id: number;
}

export interface IUserProfileUpdate {
    email?: string;
    full_name?: string;
    password?: string;
    is_active?: boolean;
    is_superuser?: boolean;
}

export interface IUserProfileCreate {
    email: string;
    full_name?: string;
    password?: string;
    is_active?: boolean;
    is_superuser?: boolean;
}

export interface ITag {
    name: string;
    id?: number;
}

export interface INoteCreate {
    title?: string | null;
    contents: string;
    start_date: string;
    end_date: string;
    color?: number;
    favourite?: boolean;
    tags?: ITag[];
}

export interface INoteUpdate {
    title: string | null;
    contents: string;
    start_date: string;
    end_date: string;
    color: string;
    favourite: boolean;
    tags: ITag[];
}

export interface INotePartialUpdate {
    title?: string | null;
    contents?: string;
    start_date?: string;
    end_date?: string;
    color?: string;
    favourite?: boolean;
    tags?: ITag[];
}

export interface INoteListed {
    title: string | null;
    start_date: string;
    end_date: string;
    color: string;
    favourite: boolean;
    id: number;
    author_id: number;
    tags: ITag[];
}

