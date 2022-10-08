import { INoteListed, INoteUpdate } from '@/interfaces';

export interface NoteState {
    selectedDates: string[];
    calendarEvents: string[];
    notes: INoteListed[];
    currentNote: INoteUpdate | null;

}
