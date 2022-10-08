<template>
  <v-container fluid>
    <v-card
    class="ma-3 pa-3"
    v-for="entry in entries" :key="entry.id" 
    >
    <v-card-text>
      <div v-if="entry.start_date==entry.end_date">On {{entry.start_date}}</div>
      <div v-else>From {{entry.start_date}} to {{entry.end_date}}</div>
      <p class="text-h4 text--primary">
        {{entry.title}}
      </p>
      <div v-for="tag in entry.tags" class="text--primary">
        {{tag.name}}
      </div>
      </v-card-text>
      <v-card-actions>
        <v-btn
          text
          @click="toggleFavouriteEntry(entry)"
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
        <v-btn
          text
          color="deep-purple accent-4"
        >
          Open
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { Store } from 'vuex';
import { dispatchUpdateNote, actionPartialUpdateNote } from '@/store/note/actions';
import { commitSetNote, commitSetNotes } from '@/store/note/mutations';
import { readNotes } from '@/store/note/getters';
import { readUserProfile } from '@/store/main/getters';
import { INoteListed, INotePartialUpdate } from '@/interfaces';


@Component
export default class Entries extends Vue {

  get entries(){
    return readNotes(this.$store)
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

  public async toggleFavouriteEntry(note: INoteListed) {
    const {id, ...noteToUpdate} = note
    noteToUpdate.favourite = !noteToUpdate.favourite
    await actionPartialUpdateNote(this.$store, {id: note.id, note: noteToUpdate})
    const idx = this.entries.findIndex(x => x.id === note.id)
    note.favourite = noteToUpdate.favourite 
    this.$set(this.entries, idx, note)
    
  }
}
</script>
