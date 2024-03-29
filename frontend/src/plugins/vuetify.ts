import Vue from 'vue';
import Vuetify from 'vuetify/lib';
import colors from 'vuetify/lib/util/colors'

Vue.use(Vuetify);

export default new Vuetify({
  icons: {
    iconfont: 'mdi',
  },
  theme: {
    options: { customProperties: true },
    themes: {
      light: {
        primary: colors.indigo.base,
        secondary: colors.pink.accent2,
        accent: colors.green.accent2,
        background: '#F1F6FF'
      },
      dark: {
        // primary: colors.indigo.lighten2
        secondary: colors.purple.accent2,
        // background: '#000000'
        background: '#333333'
      }
    },
  },
});