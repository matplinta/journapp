<template>
  <div>
    <v-btn @click="toggle_theme">Change Theme</v-btn>
    <div class="editor">
        <editor class="input" :key="theme" :api-key="apiKey" :init="tinyMCEOptions" v-model="value" inline />
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop, Emit } from 'vue-property-decorator';
import Editor from '@tinymce/tinymce-vue'



@Component({
  components: {
    Editor,
  },
})
export default class TinyEditor extends Vue {
  @Prop({default: "Let's start writing..."}) public value!: string;

  public apiKey = 'h6k9dn8akv57heejam9a6taac89mgo3qid2kebu3dr9j3d3s'
  public theme = 'light'
  public tinyMCEOptions = {
        skin: 'oxide',
        // content_css: 'default',
        // menubar: false,
        // plugins: 'lists link image table code help wordcount',
        selector: 'textarea',
        plugins: 'print preview paste importcss searchreplace autolink autosave save directionality code visualblocks visualchars fullscreen image link media template codesample table charmap hr pagebreak nonbreaking anchor toc insertdatetime advlist lists wordcount imagetools textpattern noneditable help charmap quickbars emoticons',
        menubar: 'file edit view insert format tools table help',
        toolbar: ['undo redo | bold italic underline strikethrough | fontselect fontsizeselect formatselect | alignleft aligncenter ','alignright alignjustify | outdent indent |  numlist bullist', 
        'forecolor backcolor removeformat | pagebreak | charmap emoticons | fullscreen  preview save print | insertfile image media template link anchor codesample | ltr rtl'],
        // toolbar: 'undo redo | bold italic underline strikethrough | fontselect fontsizeselect formatselect | alignleft aligncenter alignright alignjustify | outdent indent |  numlist bullist | forecolor backcolor removeformat | pagebreak | charmap emoticons | fullscreen  preview save print | insertfile image media template link anchor codesample | ltr rtl',
  
        // toolbar: [
        //   'bold italic underline fontselect image fontsizeselect link' +
        //   ' unlink forecolor backcolor selectTags',
        // ],
      }

  // public mounted() {
  //   this.value = 'awd'
  // };
  public toggle_theme() {
    const theme = this.theme === 'dark' ? 'light' : 'dark'
    this.tinyMCEOptions.skin = theme === 'dark' ? 'oxide-dark' : 'oxide'
    // this.tinyMCEOptions.content_css = theme === 'dark' ? 'dark' : 'default'
    this.theme = theme
    // this.$forceUpdate()
  }
  get contents() {
    return this.value
  }

  
}
</script>
<style>
.editor {
  /* height: 100vh; */
  display: flex;
}

.input {
  overflow: auto;
  height: 100%;
  width: 100%;
  box-sizing: border-box;
  min-height: 100vh;
  /* padding: 0 20px; */
}

.input {
  /* border: none; */
  border: 1px solid #ccc;
  resize: none;
  outline: none;
  /* color: #ccc;
  background-color: #3f3f3f;
  font-size: 14px;
  font-family: "Monaco", courier, monospace;
  padding: 20px; */
}
</style>
