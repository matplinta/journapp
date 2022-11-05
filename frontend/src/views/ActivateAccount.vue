<template>
  <v-main>
    <v-container fluid fill-height>
      <v-layout align-center justify-center>
        <v-flex xs12 sm8 md4>
          <v-card class="elevation-12">
            <v-toolbar dark color="primary">
              <v-toolbar-title>{{appName}} - Account activation</v-toolbar-title>
            </v-toolbar>
            <v-card-text>
              <p v-if="valid" class="h1">Thank you! Your account is now activated. You can now log in</p>
              <p v-if="alreadyActive" class="h1">This account is already active. You can log in</p>
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn
              color="primary"
              to='/login'>
                Log in
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-flex>
      </v-layout>
    </v-container>
  </v-main>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { Store } from 'vuex';
import { api } from '@/api';
import { appName } from '@/env';
import { commitAddNotification } from '@/store/main/mutations';
import { AxiosError } from 'axios';
import { VMain, VContainer, VLayout, VFlex, VCard, VToolbar, VToolbarTitle, VCardText, VCardActions } from 'vuetify/lib';

@Component
export default class UserProfileActivate extends Vue {
  public appName = appName;
  public valid = false;
  public alreadyActive = false;

  public mounted() {
    this.activateAccount();
  }

  public checkToken() {
    const token = (this.$router.currentRoute.query.token as string);
    if (!token) {
      commitAddNotification(this.$store, {
        content: 'No token provided in the URL, start a new password recovery',
        color: 'error',
      });
      this.$router.push('/');
    } else {
      return token;
    }
  }

  public async activateAccount() {
    const token = this.checkToken();
    if (token) {
      try {
        const response = await api.activateAccount(token);
        if (response.status === 200) {
          this.valid = true
        }
      }
      catch (error) {
        const errorObj: AxiosError = error as AxiosError
        if (errorObj.response?.status === 400) {
          this.alreadyActive = true
        }
      }
    }
  }

  public goToLogin() {
    this.$router.push({name: 'login'})
  }
}
</script>
