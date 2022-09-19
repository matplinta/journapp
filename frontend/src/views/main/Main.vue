<template>
  <div>
    <v-app-bar dark color="primary" app
    :clipped-left="true"
    :clipped-right="true"
    >
      <v-app-bar-nav-icon @click.stop="switchShowDrawer"></v-app-bar-nav-icon>
      <v-toolbar-title v-text="appName"></v-toolbar-title>
      <v-spacer></v-spacer>
      <v-switch dark color="white"
      :hide-details="true"
      prepend-icon="mdi-lightbulb"
      append-icon="mdi-lightbulb-outline"
      v-model="$vuetify.theme.dark"
      ></v-switch>
      <v-btn 
      icon
      @click="$vuetify.theme.dark = !$vuetify.theme.dark" 
      >
        <v-icon v-if="$vuetify.theme.dark">mdi-lightbulb-outline</v-icon>
        <v-icon v-else>mdi-lightbulb</v-icon>
      </v-btn>
      <v-spacer></v-spacer>
      
      <v-menu bottom left offset-y>
        <template v-slot:activator="{ on }">
          <v-btn 
          v-on="on" 
          icon>
          <v-avatar color="accent">
            <v-icon dark>
              mdi-account-circle
            </v-icon>
          </v-avatar>
          </v-btn>
        </template>
          <v-list>
            <v-list-item to="/main/profile">
              <v-list-item-content>
                <v-list-item-title>Profile</v-list-item-title>
              </v-list-item-content>
              <v-list-item-action>
                <v-icon>person</v-icon>
              </v-list-item-action>
            </v-list-item>
            <v-list-item @click="logout">
              <v-list-item-content>
                <v-list-item-title>Logout</v-list-item-title>
              </v-list-item-content>
              <v-list-item-action>
                <v-icon>close</v-icon>
              </v-list-item-action>
            </v-list-item>
          </v-list>
      </v-menu>
    </v-app-bar>
    <v-navigation-drawer floating
    width="320" persistent v-model="showDrawer" fixed app :clipped="true">
      <v-layout column fill-height>
        <v-list>
          <v-list-item class="calendar_item">
            <!-- <v-list-item-action>
              <v-icon>mdi-calendar</v-icon>
            </v-list-item-action> -->
            <!-- <v-list-item-content> -->
              <!-- <v-list-item-title>Dashboard</v-list-item-title> -->
            
              <v-date-picker 
                year-icon="mdi-calendar-blank" 
                full-width 
                show-adjacent-months
                first-day-of-week="1"
                v-model="picker"
                show-current="true"
                :title-date-format="customTitleDate"
              ></v-date-picker>
            <!-- </v-list-item-content> -->
          </v-list-item>
          <v-subheader>Main menu</v-subheader>
          <v-list-item to="/main/dashboard">
            <v-list-item-action>
              <v-icon>web</v-icon>
            </v-list-item-action>
            <v-list-item-content>
              <v-list-item-title>Dashboard</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
          <v-list-item to="/main/profile/view">
            <v-list-item-action>
              <v-icon>person</v-icon>
            </v-list-item-action>
            <v-list-item-content>
              <v-list-item-title>Profile</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
          <v-list-item to="/main/profile/edit">
            <v-list-item-action>
              <v-icon>edit</v-icon>
            </v-list-item-action>
            <v-list-item-content>
              <v-list-item-title>Edit Profile</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
          <v-list-item to="/main/profile/password">
            <v-list-item-action>
              <v-icon>vpn_key</v-icon>
            </v-list-item-action>
            <v-list-item-content>
              <v-list-item-title>Change Password</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </v-list>
        <v-divider></v-divider>
        <v-list subheader v-show="hasAdminAccess">
          <v-subheader>Admin</v-subheader>
          <v-list-item to="/main/admin/users/all">
            <v-list-item-action>
              <v-icon>group</v-icon>
            </v-list-item-action>
            <v-list-item-content>
              <v-list-item-title>Manage Users</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
          <v-list-item to="/main/admin/users/create">
            <v-list-item-action>
              <v-icon>person_add</v-icon>
            </v-list-item-action>
            <v-list-item-content>
              <v-list-item-title>Create User</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </v-list>
        <v-spacer></v-spacer>
        <v-list>
          <v-list-item @click="logout">
            <v-list-item-action>
              <v-icon>close</v-icon>
            </v-list-item-action>
            <v-list-item-content>
              <v-list-item-title>Logout</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </v-list>
      </v-layout>
    </v-navigation-drawer>
    
    <v-main>
      <router-view></router-view>
    </v-main>

    <v-navigation-drawer 
    floating
    width="320" 
    persistent 
    fixed 
    app 
    :clipped="true"
    right
    overlay-color="blue"
    overlay-opacity="50"
    >
      <v-layout column fill-height>
      </v-layout>
    </v-navigation-drawer>
    <v-footer class="pa-3" fixed app>
      <v-spacer></v-spacer>
      <span>&copy; {{appName}}</span>
    </v-footer>
  </div>
</template>

<script lang="ts">
import { Vue, Component } from 'vue-property-decorator';

import { appName } from '@/env';
import { readDashboardMiniDrawer, readDashboardShowDrawer, readHasAdminAccess } from '@/store/main/getters';
import { commitSetDashboardShowDrawer, commitSetDashboardMiniDrawer } from '@/store/main/mutations';
import { dispatchUserLogOut } from '@/store/main/actions';

const routeGuardMain = async (to, from, next) => {
  if (to.path === '/main') {
    next('/main/dashboard');
  } else {
    next();
  }
};

@Component
export default class Main extends Vue {
  public appName = appName;
  public isDarkTheme = true;

  public beforeRouteEnter(to, from, next) {
    routeGuardMain(to, from, next);
  }

  public beforeRouteUpdate(to, from, next) {
    routeGuardMain(to, from, next);
  }

  public customTitleDate(date) {
    return date.toString()
  }

  get picker() {
    return (new Date(Date.now() - (new Date()).getTimezoneOffset() * 60000)).toISOString().substr(0, 10)
  }

  get miniDrawer() {
    return readDashboardMiniDrawer(this.$store);
  }

  get showDrawer() {
    return readDashboardShowDrawer(this.$store);
  }

  set showDrawer(value) {
    commitSetDashboardShowDrawer(this.$store, value);
  }

  public switchShowDrawer() {
    commitSetDashboardShowDrawer(
      this.$store,
      !readDashboardShowDrawer(this.$store),
    );
  }

  public switchMiniDrawer() {
    commitSetDashboardMiniDrawer(
      this.$store,
      !readDashboardMiniDrawer(this.$store),
    );
  }

  public get hasAdminAccess() {
    return readHasAdminAccess(this.$store);
  }

  public async logout() {
    await dispatchUserLogOut(this.$store);
  }
}
</script>
<style>
.calendar_item {
  padding: 0  
}
/* .v-navigation-drawer__border {
  width: 0px;
} */
</style>
