<template>
  <div>
    <v-toolbar>
      <v-toolbar-title>
        Manage Users
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn color="primary" to="/main/admin/users/create">Create User</v-btn>
    </v-toolbar>
    <v-data-table :headers="headers" :items="users">
      <template v-slot:item.is_active="{ item }">
        <v-simple-checkbox
          v-model="item.is_active"
          disabled
        ></v-simple-checkbox>
      </template>
      <template v-slot:item.is_superuser="{ item }">
        <v-simple-checkbox
          v-model="item.is_superuser"
          disabled
        ></v-simple-checkbox>
      </template>
      <template v-slot:item.actions="{ item }">
        <v-btn slot="activator" text :to="{name: 'main-admin-users-edit', params: {id: item.id}}">
          <v-icon>edit</v-icon>
        </v-btn>
        <v-dialog
          v-model="deleteDialog"
          persistent
          max-width="550"
          :retain-focus="false"
        >
          <template v-slot:activator="{ on, attrs }">
            <v-btn
              text
              color="red"
              v-bind="attrs"
              v-on="on"
            >
              <v-icon>
                delete
              </v-icon>
            </v-btn>
          </template>
          <v-card>
            <v-card-title class="text-h5">
              Are you sure you want to delete this user?
            </v-card-title>
            <v-card-text>This action is irreversible.</v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn
                color="red accent-2"
                dark
                @click="deleteDialog = false"
              >
                No
              </v-btn>
              <v-btn
                color="red accent-2"
                dark
                outlined
                @click="removeUser(item.id)"
              >
                Yes
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </template>
    </v-data-table>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { Store } from 'vuex';
import { IUserProfile } from '@/interfaces';
import { readAdminUsers } from '@/store/admin/getters';
import { dispatchGetUsers, dispatchDeleteUser } from '@/store/admin/actions';

@Component
export default class AdminUsers extends Vue {
  public deleteDialog = false
  public headers = [
    {
      text: 'Name',
      sortable: true,
      value: 'name',
      align: 'left',
    },
    {
      text: 'Email',
      sortable: true,
      value: 'email',
      align: 'left',
    },
    {
      text: 'Full Name',
      sortable: true,
      value: 'full_name',
      align: 'left',
    },
    {
      text: 'Is Active',
      sortable: true,
      value: 'is_active',
      align: 'left',
    },
    {
      text: 'Is Superuser',
      sortable: true,
      value: 'is_superuser',
      align: 'left',
    },
    {
      text: 'Actions',
      value: 'actions',
    },
  ];
  get users() {
    return readAdminUsers(this.$store);
  }

  public async mounted() {
    await dispatchGetUsers(this.$store);
  }

  public async removeUser(id: number){
    console.log('remove', id)
    await dispatchDeleteUser(this.$store, id);
    console.log('get users')
    await dispatchGetUsers(this.$store);
    console.log('remove dialog')
    this.deleteDialog = false
  }
}
</script>
