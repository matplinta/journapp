import { INoteCreate, INoteUpdate, INotePartialUpdate } from './../../interfaces/index';
import { api } from '@/api';
import { ActionContext } from 'vuex';
import { IUserProfileCreate, IUserProfileUpdate } from '@/interfaces';
import { State } from '../state';
import { NoteState } from './state';
import { getStoreAccessors } from 'typesafe-vuex';
import { commitSetNotes, commitSetNote } from './mutations';
import { dispatchCheckApiError } from '../main/actions';
import { commitAddNotification, commitRemoveNotification } from '../main/mutations';
import { AxiosError } from 'axios';

type MainContext = ActionContext<NoteState, State>;

export const actions = {
    async actionGetUserNotes(context: MainContext) {
        const year = new Date(context.state.selectedDates[0]).getFullYear()
        try {
            const response = await api.getUserNotesListedByYear(context.rootState.main.token, year);
            if (response) {
                commitSetNotes(context, response.data);
            }
        } catch (error) {
            const _error: AxiosError = error as AxiosError
            await dispatchCheckApiError(context, _error);
        }
    },

    async actionCreateNote(context: MainContext, payload: INoteCreate) {
        try {
            const loadingNotification = { content: 'saving', showProgress: true };
            commitAddNotification(context, loadingNotification);
            const response = await api.createNote(context.rootState.main.token, payload)
            commitRemoveNotification(context, loadingNotification);
            commitAddNotification(context, { content: 'Note successfully created', color: 'success' });
            return response
        } catch (error) {
            const _error: AxiosError = error as AxiosError
            await dispatchCheckApiError(context, _error);
        }
    },

    async actionDeleteNote(context: MainContext, payload: {id: number}) {
        try {
            const loadingNotification = { content: 'deleting', showProgress: true };
            commitAddNotification(context, loadingNotification);
            const response = await api.deleteNote(context.rootState.main.token, payload.id)
            commitRemoveNotification(context, loadingNotification);
            commitAddNotification(context, { content: 'Note successfully deleted', color: 'success' });
            return response
        } catch (error) {
            const _error: AxiosError = error as AxiosError
            await dispatchCheckApiError(context, _error);
        }
    },

    async actionUpdateNote(context: MainContext, payload: { id: number, note: INoteUpdate }) {
        try {
            const loadingNotification = { content: 'saving', showProgress: true };
            commitAddNotification(context, loadingNotification);
            const response = await api.updateNote(context.rootState.main.token, payload.id, payload.note);
            commitRemoveNotification(context, loadingNotification);
            commitAddNotification(context, { content: 'Entry successfully updated', color: 'success' });
        } catch (error) {
            const _error: AxiosError = error as AxiosError
            await dispatchCheckApiError(context, _error);
        }
    },
    async actionPartialUpdateNote(context: MainContext, payload: { id: number, note: INotePartialUpdate }) {
        // try {
            const loadingNotification = { content: 'saving', showProgress: true };
            commitAddNotification(context, loadingNotification);
            // const response = (await Promise.all([
            //     api.partialUpdateNote(context.rootState.main.token, payload.id, payload.note),
            //     await new Promise((resolve, reject) => setTimeout(() => resolve, 500)),
            // ]))[0];
            const response = await api.partialUpdateNote(context.rootState.main.token, payload.id, payload.note)
            console.log(response.data)
            const {contents, ...noteListed} = response.data
            commitSetNote(context, noteListed)
            commitRemoveNotification(context, loadingNotification);
            commitAddNotification(context, { content: 'Entry successfully updated', color: 'success' });
        // } catch (error) {
        //     const _error: AxiosError = error as AxiosError
        //     await dispatchCheckApiError(context, _error);
        // }
    },

    
};

const { dispatch } = getStoreAccessors<NoteState, State>('');

export const dispatchGetUserNotes = dispatch(actions.actionGetUserNotes);
export const dispatchCreateNote = dispatch(actions.actionCreateNote);
export const dispatchUpdateNote = dispatch(actions.actionUpdateNote);
export const dispatchDeleteNote = dispatch(actions.actionDeleteNote);
export const actionPartialUpdateNote = dispatch(actions.actionPartialUpdateNote);
