import { INoteListed } from '@/interfaces';
import { NoteState } from './state';
import { getStoreAccessors } from 'typesafe-vuex';
import { State } from '../state';

export const mutations = {
    setSelectedDates(state: NoteState, payload: string[]) {
        state.selectedDates = payload;
    },
    setCalendarEvents(state: NoteState, payload: string[]) {
        state.calendarEvents = payload;
    },
    setNotes(state: NoteState, payload: INoteListed[]) {
        state.notes = payload;
    },
    setNote(state: NoteState, payload: INoteListed) {
        const idx = state.notes.findIndex(x => x.id === payload.id);
        if (~idx) {
            state.notes[idx] = payload;
        }
    }
};

const { commit } = getStoreAccessors<NoteState, State>('');

export const commitSetSelectedDates = commit(mutations.setSelectedDates);
export const commitSetCalendarEvents= commit(mutations.setCalendarEvents);
export const commitSetNotes = commit(mutations.setNotes);
export const commitSetNote = commit(mutations.setNote);
