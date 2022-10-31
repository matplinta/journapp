<template>
  <div>
    <v-app-bar
      app
      color="white"
      flat
    >
    </v-app-bar>

    <v-main class="background">
      <v-container>
        <v-btn
        to='/login'>
          Log in
        </v-btn>
        <v-btn
        to='/register'>
          Register
        </v-btn>
      </v-container>
    </v-main>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue, Watch } from 'vue-property-decorator';
import { Store } from 'vuex';
import { readUserProfile, readDarkTheme, readToken } from '@/store/main/getters';


export default class Welcome extends Vue {
  public links = [
        'Dashboard',
        'Messages',
        'Profile',
        'Updates',
      ]
}

</script>

<style>

</style>