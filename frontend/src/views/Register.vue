<template>
  <v-main>
    <v-container fluid fill-height>
      <v-layout align-center justify-center>
        <v-flex xs12 sm8 md4>
          <v-card class="elevation-12">
            <v-toolbar dark color="primary">
              <v-toolbar-title>{{appName}} - create account</v-toolbar-title>
              <v-spacer></v-spacer>
            </v-toolbar>
            <v-card-text>
              <v-form @keyup.enter="submit">
                <v-text-field @keyup.enter="submit" v-model="email" prepend-icon="email" name="email" label="Email" type="text"></v-text-field>
                <v-text-field @keyup.enter="submit" v-model="username" prepend-icon="person" name="username" label="Username" type="text"></v-text-field>
                <v-text-field @keyup.enter="submit" v-model="password" prepend-icon="lock" name="password" label="Password" id="password" type="password"></v-text-field>
              </v-form>
              <div v-if="registerError">
                <v-alert :value="registerError" transition="fade-transition" type="error">
                  User with this email already exists!
                </v-alert>
              </div>
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn @click.prevent="submit">Create account</v-btn>
            </v-card-actions>
          </v-card>
        </v-flex>
      </v-layout>
    </v-container>
  </v-main>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { api } from '@/api';
import { appName } from '@/env';
import { readRegisterError } from '@/store/main/getters';
import { dispatchCreateUserOpen } from '@/store/main/actions';

@Component
export default class Register extends Vue {
  public username: string = '';
  public email: string = '';
  public password: string = '';
  public appName = appName;

  public get registerError() {
    return readRegisterError(this.$store);
  }

  public submit() {
    dispatchCreateUserOpen(this.$store, {full_name: this.username, email: this.email, password: this.password});
  }
}
</script>

<style>
</style>
