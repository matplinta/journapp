import { INoteListed } from '@/interfaces';
import { NoteState } from './state';
import { getStoreAccessors } from 'typesafe-vuex';
import { State } from '../state';

export const mutations = {
    setSelectedDates(state: NoteState, payload: string[]) {
        console.log(payload)
        const date1 = payload[0] !== undefined ? new Date(payload[0]) : null
        const date2 = payload[1] !== undefined ? new Date(payload[1]) : null
        if (date1 !== null && date2 !== null) {
            if (date1 < date2 ) {
                state.selectedDates = payload;
            }
            else {
                state.selectedDates = [payload[1], payload[0]]
            }
        }
        else {
            state.selectedDates = payload;
        }
        
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
