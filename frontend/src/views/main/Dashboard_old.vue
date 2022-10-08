<template>
  <v-container fluid>
    <v-card class="ma-3 pa-3">
      <v-card-title primary-title>
        <div class="headline primary--text">Dashboard</div>
      </v-card-title>
      <v-card-text>
        <div class="headline font-weight-light ma-5">
          <TinyEditor :value="noteContents"></TinyEditor>
        </div>
      </v-card-text>
      <v-card-actions>
        <v-btn @click="submit">Save</v-btn>
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { Store } from 'vuex';
import { readUserProfile } from '@/store/main/getters';
import TinyEditor from '@/components/TinyEditorClass.vue';
import { INoteCreate } from '@/interfaces';
import { dispatchCreateNote } from '@/store/admin/actions';


@Component({
  components: {
    TinyEditor,
  },
})
export default class Dashboard extends Vue {
  public noteContents = "awddddddd"
  
  get picker() {
    return (new Date(Date.now() - (new Date()).getTimezoneOffset() * 60000)).toISOString().substr(0, 10)
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

  public async submit() {
    if (await this.$validator.validateAll()) {
      const noteToCreate: INoteCreate = {
        contents: this.noteContents,
        start_date: "2022-05-22",
        end_date: "2022-07-11"
      };
      await dispatchCreateNote(this.$store, noteToCreate);
    }
  }
}
</script>
