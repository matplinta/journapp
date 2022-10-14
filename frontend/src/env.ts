const env = process.env.VUE_APP_ENV;

let envApiUrl = '';

if (env === 'production') {
  envApiUrl = `https://${process.env.VUE_APP_DOMAIN_PROD}`;
} else if (env === 'staging') {
  envApiUrl = `https://${process.env.VUE_APP_DOMAIN_STAG}`;
} else {
  envApiUrl = `http://${process.env.VUE_APP_DOMAIN_DEV}`;
}

export const apiUrl = envApiUrl;
export const appName = process.env.VUE_APP_NAME;

export const tinyMCEApiKey = 'h6k9dn8akv57heejam9a6taac89mgo3qid2kebu3dr9j3d3s'
export const tinyMCEOptions = {
  skin: 'oxide',
  // content_css: 'default',
  menubar: false,
  // plugins: 'lists link image table code help wordcount',
  selector: 'textarea',
  plugins: 'print preview paste importcss searchreplace autolink autosave save directionality code visualblocks visualchars fullscreen image link media template codesample table charmap hr pagebreak nonbreaking anchor toc insertdatetime advlist lists wordcount imagetools textpattern noneditable help charmap quickbars emoticons',
  // menubar: 'file edit view insert format tools table help',
  toolbar: ['undo redo | bold italic underline strikethrough | forecolor backcolor removeformat | fontselect fontsizeselect formatselect', 'alignleft aligncenter alignright alignjustify | outdent indent |  numlist bullist | charmap emoticons | fullscreen | insertfile image link anchor codesample | ltr rtl hr']
  // toolbar: 'undo redo | bold italic underline strikethrough | fontselect fontsizeselect formatselect | alignleft aligncenter alignright alignjustify | outdent indent |  numlist bullist | forecolor backcolor removeformat | pagebreak | charmap emoticons | fullscreen  preview save print | insertfile image media template link anchor codesample | ltr rtl',

  // toolbar: [
  //   'bold italic underline fontselect image fontsizeselect link' +
  //   ' unlink forecolor backcolor selectTags',
  // ],
};
