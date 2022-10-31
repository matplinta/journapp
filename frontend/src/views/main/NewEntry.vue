<template>
  <v-container fluid>
    <v-card 
    class="pa-3 ma-4"
    min-height="45rem"
    >
      <v-card-text v-if="date_range_selected_bool">
        <div class="d-flex flex-row mb-6">
          <v-chip
            class="dateRangeTag py-5"
            color="accent"
            text-color="accent darken-4"
            ripple
            label>
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
            color="secondary"
            dense
          >
            <template v-slot:selection="{ attrs, item, select, selected }">
              <v-chip
                v-bind="attrs"
                :input-value="selected"
                close
                dark
                color="secondary"
                @click="select"
                @click:close="removeTag(item)"
               
              >
                <strong>{{ item }}</strong>&nbsp;
              </v-chip>
            </template>
          </v-combobox>
          <v-spacer></v-spacer>
          <div>
            <v-btn 
            @click="save"
            color="green"
            dark
            depressed
            >Save</v-btn>
          </div>
        </div>
        <v-text-field
          class="titleTextField"
          placeholder="Title"
          v-model="note.title"
        ></v-text-field>
        <div class="headline font-weight-light ">
          <editor class="input" :key="editorTheme" :api-key="tinyMCEApiKey" :init="tinyMCEOptions" v-model="note.contents" inline />
        </div>
      </v-card-text>
      <v-card-text v-else>
        <div class="d-flex flex-row mb-6">
          <div class="date_container accent text-center rounded-lg py-1 px-4">
            <span class="accent--text text--darken-3 font-weight-regular subtitle-1">
              {{date_range}}
            </span>
          </div>
        </div>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script lang="ts">
import { Component, Prop, Vue, Watch} from 'vue-property-decorator';
import { Store } from 'vuex';
import { readUserProfile, readDarkTheme } from '@/store/main/getters';
import Editor from '@tinymce/tinymce-vue'
import { INote, INoteCreate, ITag } from '@/interfaces';
import { dispatchCreateNote, dispatchGetUserNotes } from '@/store/note/actions';
import { tinyMCEOptions, tinyMCEApiKey } from '@/env';
import { readSelectedDates } from '@/store/note/getters';


@Component({
  components: {
    Editor,
  },
})
export default class NewEntry extends Vue {
  @Watch('date_range') async onSelectedDatesChange() {
    const dates = readSelectedDates(this.$store)
    this.note.start_date = dates[0]
    this.note.end_date = dates[1]
  }
  public note: INoteCreate = {
    title: '',
    start_date: '',
    end_date: '',
    contents: "Let's start writing todays notes...", 
    color: 'pear',
    favourite: false,
    tags: []
  }
  public editorTheme = 'light'
  public tinyMCEApiKey = tinyMCEApiKey

  public mounted() {
    const dates = readSelectedDates(this.$store)
    this.note.start_date = dates[0]
    this.note.end_date = dates[1]
  };

  get tagsStrings() {
    return this.note.tags!.map(({ name }) => name);
  }

  set tagsStrings(tags: string[]) {
    let uniqTags = Array.from(new Set(tags))
    let newTags: ITag[] = uniqTags.map((name) => ({"name": name.toLowerCase()} as ITag))
    this.note.tags = newTags
  }

  public async removeTag(name: string) {
    let tagIdx = this.note.tags!.findIndex(object => {
      return object.name === name
    })
    this.note.tags!.splice(tagIdx, 1)

  }

  get date_range() {
    const dates = readSelectedDates(this.$store)
    const start = dates[0] == undefined ? '...' : dates[0]
    const end = dates[1] == undefined ? '...' : dates[1]
    return `${start.replaceAll('-', '/')} - ${end.replaceAll('-', '/')}`
  }

  get date_range_selected_bool() {
    const dates = readSelectedDates(this.$store)
    if (dates[0] !== undefined && dates[1] !== undefined) return true
    else return false
  }

  get tinyMCEOptions () {
    let tinyOptions = tinyMCEOptions
    let theme = readDarkTheme(this.$store) ? 'dark' : 'light'
    tinyOptions.skin = theme === 'dark' ? 'oxide-dark' : 'oxide'
    // this.tinyMCEOptions.content_css = theme === 'dark' ? 'dark' : 'default'
    this.editorTheme = theme
    return tinyOptions

  }

  public async save() {
    if (await this.$validator.validateAll()) {
      const note: INoteCreate = this.note
      const resp  = await dispatchCreateNote(this.$store, note);
      const noteCreated: INote  = resp?.data
      console.log(noteCreated)
      if (noteCreated.id !== undefined) {
        await dispatchGetUserNotes(this.$store)
        this.$router.push({name: 'entry', params: { id: noteCreated.id as any}})
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
</style>