<template>
  <v-flex xs12>
    <v-card color="primary">
      <div>
        <v-toolbar flat color="green">
          <v-toolbar-title>Risks</v-toolbar-title>
          <v-divider
            class="mx-2"
            inset
            vertical
          ></v-divider>
          <v-spacer></v-spacer>
          <v-dialog v-model="dialog" max-width="500px">
            <template v-slot:activator="{ on }">
              <v-btn color="primary"
               :disabled="headers.length === 0 ? true : false"
               dark class="mb-2" v-on="on">New Risk Item</v-btn>
            </template>
            <v-card>
              <v-card-title>
                <span class="headline">{{ formTitle }}</span>
              </v-card-title>

              <v-card-text>
                <v-container grid-list-md>
                  <v-layout wrap>
                  </v-layout>
                </v-container>
              </v-card-text>

              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="blue darken-1" flat @click="">Cancel</v-btn>
                <v-btn color="blue darken-1" flat @click="">Save</v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>
        </v-toolbar>
        <v-data-table
          :headers="headers"
          :items="risks"
          class="elevation-1">
          <template v-slot:items="props">
          </template>
          <template v-slot:no-data>
            <v-alert
              :value="true"
              type="info"
            >
              No data to display. Create new Risk Type if button available, or choose Risk Type first or create
              new Risk Type and provide new Risk.
            </v-alert>
          </template>
        </v-data-table>
      </div>
  </v-card>
</v-flex>
</template>

<script>
  import { eventHub } from '../main';
  import { APIService } from '../services/APIService';

  const apiService = new APIService();

  export default {
    name: "Risks",
    data: () => ({
      dialog: false,
      riskTypeId: null,
      typeName: null,
      schema: [],
      isActive: null,
      headers: [],
      risks: [],
      editedIndex: -1,
    }),

    computed: {
      formTitle () {
        return this.editedIndex === -1 ? 'New Risk Item' : 'Edit Risk Item'
      }
    },

    watch: {
      dialog (val) {
        val || this.close()
      }
    },

    created () {
      eventHub.$on('list-item-clicked', ({id, type_name, schema, is_active}) => {
        this.riskTypeId = id;
        this.typeName = type_name;
        this.schema = Object.assign([], this.schema, schema);
        this.isActive = is_active;
        this.makeHeaders();
      });
    },

    methods: {
      getRisks () {
        if (this.riskTypeId) {
          apiService.getRisks(this.riskTypeId)
            .then((data) => {
              console.log(data);
            });
        }
      },
      makeHeaders () {
        // Dynamically create headers for Risks table
        this.headers = [];
        if (!this.schema.isEmpty) {
          let temp = null;
          const pattern = /\_/;
          this.schema.forEach((item, index) => {
            if (pattern.test(item.field_name)) {
              temp = item.field_name.replace('_', ' ');
            } else {
              temp = item.field_name;
            }
            this.headers.push({ text: temp, value: item.field_name, sortable: true, align: 'center' });
          });
          return this.headers;
        }
      },
    }
  }
</script>

<style scoped>

</style>
