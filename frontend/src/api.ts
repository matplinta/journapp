import { INoteUpdate, INotePartialUpdate, INote } from './interfaces/index';
import axios from 'axios';
import { apiUrl } from '@/env';
import { IUserProfile, IUserProfileUpdate, IUserProfileCreate, INoteCreate, INoteListed } from './interfaces';
import { convertToString } from '@/utils';

function authHeaders(token: string) {
  return {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  };
}

export const api = {
  async logInGetToken(username: string, password: string) {
    const params = new URLSearchParams();
    params.append('username', username);
    params.append('password', password);

    return axios.post(`${apiUrl}/api/v1/login/access-token`, params);
  },
  async getMe(token: string) {
    return axios.get<IUserProfile>(`${apiUrl}/api/v1/users/me`, authHeaders(token));
  },
  async updateMe(token: string, data: IUserProfileUpdate) {
    return axios.put<IUserProfile>(`${apiUrl}/api/v1/users/me`, data, authHeaders(token));
  },
  async getUsers(token: string) {
    return axios.get<IUserProfile[]>(`${apiUrl}/api/v1/users/`, authHeaders(token));
  },
  async updateUser(token: string, userId: number, data: IUserProfileUpdate) {
    return axios.put(`${apiUrl}/api/v1/users/${userId}`, data, authHeaders(token));
  },
  async createUser(token: string, data: IUserProfileCreate) {
    return axios.post(`${apiUrl}/api/v1/users/`, data, authHeaders(token));
  },
  async createUserOpen(data: IUserProfileCreate) {
    return axios.post(`${apiUrl}/api/v1/users/open`, data);
  },
  async deleteUser(token: string, userId: number) {
    return axios.delete(`${apiUrl}/api/v1/users/${userId}`, authHeaders(token));
  },
  async passwordRecovery(email: string) {
    return axios.post(`${apiUrl}/api/v1/password-recovery/${email}`);
  },
  async resetPassword(password: string, token: string) {
    return axios.post(`${apiUrl}/api/v1/reset-password/`, {
      new_password: password,
      token,
    });
  },
  async activateAccount(token: string) {
    return axios.post(`${apiUrl}/api/v1/activate-account/`, {
      token,
    });
  },
  async getNote(token: string, noteId: number) {
    return axios.get<INote>(`${apiUrl}/api/v1/notes/${noteId}`, authHeaders(token));
  },
  async deleteNote(token: string, noteId: number) {
    return axios.delete(`${apiUrl}/api/v1/notes/${noteId}`, authHeaders(token));
  },
  async createNote(token: string, data: INoteCreate) {
    return axios.post(`${apiUrl}/api/v1/notes/`, data, authHeaders(token));
  },
  async updateNote(token: string, noteId: number, data: INoteUpdate) {
    return axios.put(`${apiUrl}/api/v1/notes/${noteId}`, data, authHeaders(token));
  },
  async partialUpdateNote(token: string, noteId: number, data: INotePartialUpdate) {
    return axios.patch(`${apiUrl}/api/v1/notes/${noteId}`, data, authHeaders(token));
  },
  async getUserNotesListedByYear(token: string, year: number) {
    const firstDay = new Date(year, 0, 1);
    const lastDay = new Date(year, 11, 31);

    const params = new URLSearchParams();
    params.append('start_date', convertToString(firstDay));
    params.append('end_date', convertToString(lastDay));

    return axios.get<INoteListed[]>(`${apiUrl}/api/v1/notes/listing/by_date/`, {...authHeaders(token), params: params});
  },

  
};
