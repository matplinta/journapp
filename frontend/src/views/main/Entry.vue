<template>
  <v-container fluid>
    <v-card 
    class="pa-3 ma-4"
    min-height="45rem"
    >
      <v-card-text>
        <div class="d-flex flex-row mb-6">
          <v-chip
            class="dateRangeTag py-5"
            color="accent"
            text-color="accent darken-4"
            label
            ripple>
            <v-icon left>
              mdi-calendar-range
            </v-icon>
              {{date_range}}
            </v-chip>
          <v-spacer></v-spacer>
          <v-combobox
            v-model="tagsStrings"
            clearable
            chips
            multiple
            prepend-inner-icon="mdi-label"
            outlined
            placeholder="Note tags..."
            label="Note tags..."
            color="indigo lighten-2"
            dense
          >
            <template v-slot:selection="{ attrs, item, select, selected }">
              <v-chip
                v-bind="attrs"
                :input-value="selected"
                close
                dark
                color="indigo lighten-2"
                @click="select"
                @click:close="removeTag(item)"
               
              >
                <strong>{{ item }}</strong>&nbsp;
              </v-chip>
            </template>
          </v-combobox>
          <v-spacer></v-spacer>
          <div class="px-4">
            <!-- <v-btn 
            @click="deleteNote"
            color="secondary"
            outlined
            >Delete</v-btn> -->
            <v-dialog
              v-model="deleteDialog"
              persistent
              max-width="550"
            >
              <template v-slot:activator="{ on, attrs }">
                <v-btn
                  text
                  color="red"
                  v-bind="attrs"
                  v-on="on"
                >
                <v-icon left>
                  mdi-trash-can-outline
                </v-icon>
                  Delete
                </v-btn>
              </template>
              <v-card>
                <v-card-title class="text-h5">
                  Are you sure you want to delete this entry?
                </v-card-title>
                <v-card-text>This action is irreversible.</v-card-text>
                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn
                    color="red accent-2"
                    dark
                    @click="deleteDialog = false"
                  >
                    No
                  </v-btn>
                  <v-btn
                    color="red accent-2"
                    dark
                    outlined
                    @click="deleteNote"
                  >
                    Yes
                  </v-btn>
                </v-card-actions>
              </v-card>
            </v-dialog>
          </div>
          <div>
            <v-btn 
            @click="save"
            color="primary"
            dark
            depressed
            >Save</v-btn>
          </div>
        </div>
        <v-text-field
          class="titleTextField"
          v-model="note.title"
        ></v-text-field>
        <div class="headline editorDiv">
          <editor class="input" :key="editorTheme" :api-key="tinyMCEApiKey" :init="tinyMCEOptions" v-model="note.contents" inline />
        </div>
      </v-card-text>
      <v-card-actions>
        
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<script lang="ts">
import { Component, Prop, Vue, Watch } from 'vue-property-decorator';
import { Store } from 'vuex';
import { readUserProfile, readDarkTheme, readToken } from '@/store/main/getters';
import Editor from '@tinymce/tinymce-vue'
import { INote, ITag } from '@/interfaces';
import { tinyMCEOptions, tinyMCEApiKey } from '@/env';
import { readSelectedDates } from '@/store/note/getters';
import { api } from '@/api'
import { dispatchDeleteNote, dispatchGetUserNotes, dispatchUpdateNote } from '@/store/note/actions';
import { noteModule } from '@/store/note';


@Component({
  components: {
    Editor,
  },
})
export default class Entry extends Vue {
  @Prop() public id!: number;
  @Watch('id') async onPropIdChange() {
    this.loadNoteFromDB()
  }

  // public note: INote | null = null
  public note: INote = {
    title: '',
    start_date: '',
    end_date: '',
    contents: '', 
    color: '',
    favourite: false,
    id: null,
    author_id: null,
    tags: []
  }
  public deleteDialog = false
  public editorTheme = 'light'
  public tinyMCEApiKey = tinyMCEApiKey

  public async loadNoteFromDB() {
    const note = await api.getNote(readToken(this.$store), this.id)
    this.note = note.data
  }

  public async created() {
    this.loadNoteFromDB()
  };

  // public get note_contents() {
  //   if (this.note == null) {
  //     return ''
  //   }
  //   return this.note.contents
  // }
  // public set note_contents(value: string) {
  //   if (this.note !== null) {
  //     this.note.contents = value
  //   }
  // } 

  public async removeTag(name: string) {
    let tagIdx = this.note.tags.findIndex(object => {
      return object.name === name
    })
    this.note.tags.splice(tagIdx, 1)

  }

  get tagsStrings() {
    return this.note.tags.map(({ name }) => name);
  }

  set tagsStrings(tags: string[]) {
    let uniqTags = Array.from(new Set(tags))
    let newTags: ITag[] = uniqTags.map((name) => ({"name": name.toLowerCase()} as ITag))
    this.note.tags = newTags
  }

  get date_range() {
    return `${this.note?.start_date.replaceAll('-', '/')} - ${this.note?.end_date.replaceAll('-', '/')}`
  }

  get tinyMCEOptions () {
    let tinyOptions = tinyMCEOptions
    let theme = readDarkTheme(this.$store) ? 'dark' : 'light'
    tinyOptions.skin = theme === 'dark' ? 'oxide-dark' : 'oxide'
    // this.tinyMCEOptions.content_css = theme === 'dark' ? 'dark' : 'default'
    this.editorTheme = theme
    return tinyOptions

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

  public async save() {
    if (await this.$validator.validateAll()) {
      const {id, author_id, ...note} = this.note 
      await dispatchUpdateNote(this.$store, {id: id as number, note: note});
    }
    // console.log(this.$route)
  }
  public async deleteNote() {
    this.deleteDialog = false
    if (await this.$validator.validateAll()) {
      const response = await dispatchDeleteNote(this.$store, {id: this.note.id as any});
      if (response?.status == 200) {
        await dispatchGetUserNotes(this.$store)
        this.$router.push({name: 'entries'})
      }
    }
  }
}
</script>
<style>
 .titleTextField input{
      font-size: 2.5rem;
      line-height: 3rem;
      padding: 1rem 0 2rem 0 ;
}
.theme--light.v-card > .v-card__text{
  color: black;
}
.theme--dark.v-card > .v-card__text{
  color: white;
}

.dateRangeTag {
  overflow: visible !important;
  font-size: 18px !important;
}
/* .editorDiv {
  border: 1px solid #ccc;
  border-radius: 16px;
} */
/* .theme--light.v-input input, .theme--light.v-input textarea {
  color: white;
} */
</style>