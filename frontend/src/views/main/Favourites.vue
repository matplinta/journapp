<template>
  <v-container fluid
  color="">
    <div
    class="mx-15 my-4">
      <h1>My favourites</h1>
    </div>
    <v-card
    elevation="4"
    class="mx-15 my-4 pa-2"
    v-for="entry in entries" :key="entry.id" 
    >
    <v-card-text>
      <v-btn
      x-large
      right
      absolute
      icon
      depressed
      @click="removeFavouriteEntry(entry)"
      > 
        <v-icon
          v-if="!entry.favourite"
          color="grey lighten-1"
        >
          mdi-star-outline
        </v-icon>
        <v-icon
          v-else
          color="yellow darken-3"
        >
          mdi-star
        </v-icon>
      </v-btn>
      <div v-if="entry.start_date==entry.end_date">On <span class="secondary--text">{{entry.start_date}}</span></div>
      <div v-else>From <span class="secondary--text">{{entry.start_date}}</span> to <span class="secondary--text">{{entry.end_date}}</span></div>
      <p :class="entry.title? 'text-h4 text--primary mb-0' : 'text-h4 mb-0 text--disabled'">
        {{entry.title ? entry.title: 'untitled...'}}
      </p>
      </v-card-text>
      <v-card-actions>
        <v-btn
          dark
          depressed
          color="primary"
          @click="routeToEntryPage(entry)"
        >
          Open
        </v-btn>
        <v-spacer></v-spacer>
        <div
        class="float-right">
          <v-chip 
            v-for="tag in entry.tags" 
            :key="tag.name"
            class="ml-2"
            dark
            color="secondary"
            ripple
            >
              {{tag.name}}
          </v-chip>
        </div>
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { Store } from 'vuex';
import { dispatchUpdateNote, actionPartialUpdateNote } from '@/store/note/actions';
import { commitSetNote, commitSetNotes, commitSetSelectedDates } from '@/store/note/mutations';
import { readNotes } from '@/store/note/getters';
import { readUserProfile } from '@/store/main/getters';
import { INoteListed, INotePartialUpdate } from '@/interfaces';


@Component
export default class Entries extends Vue {

  get entries(){
    return readNotes(this.$store).filter(entry => entry.favourite === true)
  }

  get greetedUser() {
    const userProfile = readUserProfile(this.$store);
    if (userProfile) {
      if (userProfile.full_name) {
        return userProfile.full_name;
      } else {
        return userProfile.email;
      }
    }
  }

  public async routeToEntryPage (entry) {
    commitSetSelectedDates(this.$store, [entry.start_date, entry.end_date])
    this.$router.push({name: 'entry', params: { id: entry.id as any}})
    
  }

  public async removeFavouriteEntry(note: INoteListed) {
    const {id, ...noteToUpdate} = note
    noteToUpdate.favourite = false
    await actionPartialUpdateNote(this.$store, {id: note.id, note: noteToUpdate})
    note.favourite = false
  }
}
</script>
