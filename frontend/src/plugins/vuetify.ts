import Vue from 'vue';
import Vuetify from 'vuetify/lib';
import colors from 'vuetify/lib/util/colors'

Vue.use(Vuetify);

export default new Vuetify({
  icons: {
    iconfont: 'mdi',
  },
  theme: {
    themes: {
      light: {
        primary: colors.indigo.base,
        secondary: colors.indigo.darken2,
        accent: colors.green.accent2,
      },
      dark: {
        // primary: colors.indigo.lighten2
      }
    },
  },
});