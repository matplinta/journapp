export const getLocalToken = () => localStorage.getItem('token');

export const saveLocalToken = (token: string) => localStorage.setItem('token', token);

export const removeLocalToken = () => localStorage.removeItem('token');

export const convertToString = (date: Date) => {
    return date.getFullYear() + "-"  + (date.getMonth()+1) + "-" +  date.getDate()
}
