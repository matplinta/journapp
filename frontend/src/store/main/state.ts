import { IUserProfile } from '@/interfaces';

export interface AppNotification {
    content: string;
    color?: string;
    showProgress?: boolean;
}

export interface MainState {
    token: string;
    isLoggedIn: boolean | null;
    logInError: boolean;
    registerError: boolean;
    userProfile: IUserProfile | null;
    dashboardShowDrawer: boolean;
    notifications: AppNotification[];
    darkTheme: boolean;
}
