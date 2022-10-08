import { NoteState } from './state';
import { getStoreAccessors } from 'typesafe-vuex';
import { State } from '../state';

export const getters = {
    selectedDates: (state: NoteState) => state.selectedDates,
    calendarEvents: (state: NoteState) => state.calendarEvents,
    notes: (state: NoteState) => state.notes,
    // adminOneUser: (state: NoteState) => (userId: number) => {
    //     const filteredUsers = state.users.filter((user) => user.id === userId);
    //     if (filteredUsers.length > 0) {
    //         return { ...filteredUsers[0] };
    //     }
    // },
};

const { read } = getStoreAccessors<NoteState, State>('');

export const readSelectedDates = read(getters.selectedDates);
export const readCalendarEvents = read(getters.calendarEvents);
export const readNotes = read(getters.notes);
