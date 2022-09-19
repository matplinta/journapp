<template>
  <div>
    <v-btn @click="toggle_theme">Change Theme</v-btn>
    <div class="editor">
      <div class="input" :key="theme">
        <editor :api-key="apiKey" :init="tinyMCEOptions"  v-model="value" inline />
      </div>
      <div class="output" v-html="value">
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import Editor from '@tinymce/tinymce-vue'


@Component({
  components: {
    Editor,
  },
})
export default class TinyEditor extends Vue {

  public apiKey = 'h6k9dn8akv57heejam9a6taac89mgo3qid2kebu3dr9j3d3s'
  public value = ''
  public theme = 'light'
  public tinyMCEOptions = {
        skin: 'oxide',
        // content_css: 'default',
        menubar: false,
        plugins: 'lists link image table code help wordcount',
        toolbar: [
          'bold italic underline fontselect image fontsizeselect link' +
          ' unlink forecolor backcolor selectTags',
        ],
      }

  public mounted() {
    this.value = 'awd'
  };
  public toggle_theme() {
      const theme = this.theme === 'dark' ? 'light' : 'dark'
      this.tinyMCEOptions.skin = theme === 'dark' ? 'oxide-dark' : 'oxide'
      // this.tinyMCEOptions.content_css = theme === 'dark' ? 'dark' : 'default'
      this.theme = theme
      // this.$forceUpdate()
    }
}
</script>
<style>
/* .tedit {
  width: 50%;
  box-sizing: border-box;
  padding: 0 20px;
  margin-left: auto;
  margin-right: 0;
} */
.editor {
  /* height: 100vh; */
  display: flex;
}

.input,
.output {
  overflow: auto;
  width: 50%;
  height: 100%;
  box-sizing: border-box;
  padding: 0 20px;
}

.input {
  border: none;
  border-right: 1px solid #ccc;
  resize: none;
  outline: none;
  color: #ccc;
  background-color: #3f3f3f;
  font-size: 14px;
  font-family: "Monaco", courier, monospace;
  padding: 20px;
}
</style>
