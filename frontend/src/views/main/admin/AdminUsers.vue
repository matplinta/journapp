<template>
  <div>
    <v-toolbar light>
      <v-toolbar-title>
        Manage Users
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn color="primary" to="/main/admin/users/create">Create User</v-btn>
    </v-toolbar>
    <v-data-table :headers="headers" :items="users">
      <!-- <template v-slot:default="props">
        <td>{{ props.item.name }}</td>
        <td>{{ props.item.email }}</td>
        <td>{{ props.item.full_name }}</td>
        <td><v-icon v-if="props.item.is_active">mdi-cancel</v-icon></td>
        <td><v-icon v-if="props.item.is_superuser">checkmark</v-icon></td>
        <td class="justify-center layout px-0">
          <v-tooltip top>
            <span>Edit</span>
            <v-btn slot="activator" flat :to="{name: 'main-admin-users-edit', params: {id: props.item.id}}">
              <v-icon>edit</v-icon>
            </v-btn>
          </v-tooltip>
        </td>
      </template> -->
      <template v-slot:item.isActive="{ item }">
        <v-simple-checkbox
          v-model="item.is_active"
          disabled
        ></v-simple-checkbox>
      </template>
      <template v-slot:item.isSuperuser="{ item }">
        <v-simple-checkbox
          v-model="item.is_superuser"
          disabled
        ></v-simple-checkbox>
      </template>
      <template v-slot:item.actions="{ item }">
        <v-btn slot="activator" text :to="{name: 'main-admin-users-edit', params: {id: item.id}}">
          <v-icon>edit</v-icon>
        </v-btn>
        <v-btn 
        text
        color="red"
        @click="removeUser(item.id)">
          <v-icon>delete</v-icon>
        </v-btn>
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
      value: 'isActive',
      align: 'left',
    },
    {
      text: 'Is Superuser',
      sortable: true,
      value: 'isSuperuser',
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

  async removeUser(id: number){
    dispatchDeleteUser(this.$store, id);
    await dispatchGetUsers(this.$store);
  }
}
</script>
