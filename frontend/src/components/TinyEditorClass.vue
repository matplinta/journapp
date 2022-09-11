<template>
  <div>
    <v-btn @click="toggle_theme">Change Theme</v-btn>
    <v-btn @click="print_contents">Log options</v-btn>
    <div class="editor">
      <div class="input" :key="theme">
        <editor :api-key="apiKey" :init="tinyMCEOptions" v-model="value"  />
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

  public apiKey = "h6k9dn8akv57heejam9a6taac89mgo3qid2kebu3dr9j3d3s";
  public value = '';
  public theme = "dark";
  public tinyMCEOptions = {
        skin: 'oxide-dark',
        content_css: 'dark',
        menubar: false,
        plugins: 'lists link image table code help wordcount',
        toolbar: [
          'bold italic underline fontselect image fontsizeselect link' +
          ' unlink forecolor backcolor selectTags'
        ]
      }

  public mounted() {
    this.value = 'awd'
  };
  public toggle_theme() {
      console.log(this.theme)
      const theme = this.theme === "dark" ? "light" : "dark"
      console.log(this.theme)
      console.log(theme)
      this.tinyMCEOptions.skin = theme === "dark" ? "oxide-dark" : "oxide"
      this.tinyMCEOptions.content_css = theme
      this.theme = theme
      this.$forceUpdate()
      console.log(this.tinyMCEOptions.skin)
      console.log(this.tinyMCEOptions.content_css)
      // this.$forceUpdate()
    }
  public print_contents() {
      console.log(this.value)
      console.log(this.tinyMCEOptions)
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
  background-color: #f6f6f6;
  font-size: 14px;
  font-family: "Monaco", courier, monospace;
  padding: 20px;
}
</style>
