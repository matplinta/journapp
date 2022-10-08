import { mutations } from './mutations';
import { getters } from './getters';
import { actions } from './actions';
import { NoteState } from './state';

const defaultState: NoteState = {
  selectedDates: [],
  calendarEvents: [],
  notes: [],
  currentNote: null,

}

export const noteModule = {
  state: defaultState,
  mutations,
  actions,
  getters,
};
