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
      v-model="darkThemeSet"
      ></v-switch>
      <v-btn 
      icon
      @click="toggleTheme" 
      >
        <v-icon v-if="darkThemeSet">mdi-lightbulb-outline</v-icon>
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
        <v-date-picker 
          class="picker-override"
          year-icon="mdi-calendar-blank" 
          full-width 
          range
          color="accent"
          show-adjacent-months
          first-day-of-week="1"
          v-model="picker"
          @change="dblClick"
          :show-current="true"
          :no-title="true"
          :events="eventsFunction"
          
        ></v-date-picker>
        <v-list>
          <!-- <v-list-item class="calendar_item">
          </v-list-item> -->
          <v-subheader>Main menu</v-subheader>
          <v-list-item to="/main/dashboard">
            <v-list-item-action>
              <v-icon>web</v-icon>
            </v-list-item-action>
            <v-list-item-content>
              <v-list-item-title>Dashboard</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
          <v-list-item to="/main/entries">
            <v-list-item-action>
              <v-icon>notes</v-icon>
            </v-list-item-action>
            <v-list-item-content>
              <v-list-item-title>Entires</v-list-item-title>
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
    <v-footer class="pa-1" fixed app>
      <v-spacer></v-spacer>
      <span>&copy; {{appName}}</span>
    </v-footer>
  </div>
</template>

<script lang="ts">
import { Vue, Component } from 'vue-property-decorator';

import { appName } from '@/env';
import { readDashboardShowDrawer, readHasAdminAccess, readDarkTheme, readToken } from '@/store/main/getters';
import { commitSetDashboardShowDrawer, commitSetDarkTheme} from '@/store/main/mutations';
import { dispatchUserLogOut } from '@/store/main/actions';
import { api } from '@/api';
import { commitSetCalendarEvents, commitSetSelectedDates } from '@/store/note/mutations';
import { dispatchGetUserNotes } from '@/store/note/actions';
import { readCalendarEvents, readNotes, readSelectedDates } from '@/store/note/getters';

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


  get calendarEntries() {
    return readCalendarEvents(this.$store)
  }

  set calendarEntries(value: string[]) {
    commitSetCalendarEvents(this.$store, value)
  }

  get picker(){
    return readSelectedDates(this.$store)
  }

  set picker(value) {
    commitSetSelectedDates(this.$store, value)
  }

  public beforeRouteEnter(to, from, next) {
    routeGuardMain(to, from, next);
  }

  public beforeRouteUpdate(to, from, next) {
    routeGuardMain(to, from, next);
  }

  public customTitleDate(date) {
    return date.toString()
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

  get darkThemeSet() {
    return readDarkTheme(this.$store);
  }

  set darkThemeSet(value) {
    commitSetDarkTheme(this.$store, value);
    this.$vuetify.theme.dark = value;
  }

  public toggleTheme() {
    let toggledDarkThemeValue = !readDarkTheme(this.$store);
    commitSetDarkTheme(
      this.$store,
      toggledDarkThemeValue
    )
    this.$vuetify.theme.dark = toggledDarkThemeValue
  }

  public get hasAdminAccess() {
    return readHasAdminAccess(this.$store);
  }

  public async logout() {
    await dispatchUserLogOut(this.$store);
  }

  public async dblClick (date) {
        alert(`You have just double clicked the following date: ${date}`)
  }

  public async setCalendarEvents(){
    const entriesListed = readNotes(this.$store)
    const datesSet = new Set()
    for (const entry of entriesListed) {
      datesSet.add(entry.start_date)
    }
    console.log(datesSet)
    this.calendarEntries = Array.from(datesSet) as string[]
  }

  public getEventColor(color: string){
    if (color === 'pear') return 'pink lighten-1'
    else if (color === 'banana') return 'yellow'
    else return 'accent'
  }

  public eventsFunction(date) {
    const entriesListed = readNotes(this.$store)
    const colors: string[] = [];
    for (const entry of entriesListed) {
      var start = new Date(entry.start_date)
      var end = new Date(entry.end_date)
      var _date = new Date(date)
      if (start <=_date && _date <= end ) {
        colors.push(this.getEventColor(entry.color))
      }
    }
    return colors
  }

  public async mounted() {
    this.picker = [
    (new Date(Date.now() - (new Date()).getTimezoneOffset() * 60000)).toISOString().substr(0, 10), 
    (new Date(Date.now() - (new Date()).getTimezoneOffset() * 60000)).toISOString().substr(0, 10)
  ]
    // commitSetSelectedDates(this.$store, this.picker)
    await dispatchGetUserNotes(this.$store)
    await this.setCalendarEvents()
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
.v-navigation-drawer{
  background-color: var(--v-background-base) !important;
} 
.theme--dark.v-card, .theme--dark.v-picker__body {
  background-color: inherit !important;
}

</style>
