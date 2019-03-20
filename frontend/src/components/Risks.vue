<template>
  <v-flex xs12 md9>
    <v-card color="primary">
      <div>
        <v-toolbar flat color="green">
          <v-toolbar-title>{{ panelTitle }}</v-toolbar-title>
          <v-divider
            class="mx-2"
            inset
            vertical
          ></v-divider>
          <v-spacer></v-spacer>
          <v-dialog v-model="dialog" max-width="1200px">
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
                <v-form @submit.prevent="handleSubmit">
                  <v-container grid-list-md>
                    <v-layout wrap>
                      <v-flex xs12 sm6 md4 v-for="(field, index) in schema">
                        <template v-if="field.field_type === 'text'">
                          <v-text-field
                            v-model="field.value"
                            :name="field.field_name"
                            :label="makeLabel(field.field_name)"
                            :type="field.field_type"
                            :error-messages="errors.first(field.field_name)"
                            v-validate="field.is_required ? 'required' : ''"
                          ></v-text-field>
                        </template>
                        <template v-if="field.field_type === 'email'">
                          <v-text-field
                            v-model="field.value"
                            :name="field.field_name"
                            :label="makeLabel(field.field_name)"
                            :type="field.field_type"
                            :error-messages="errors.first(field.field_name)"
                            v-validate="field.is_required ? 'required|email' : ''"
                          ></v-text-field>
                        </template>
                        <template v-if="field.field_type === 'tel'">
                          <v-text-field
                            v-model="field.value"
                            :name="field.field_name"
                            :label="makeLabel(field.field_name)"
                            :type="field.field_type"
                            :mask="'phone'"
                            :error-messages="errors.first(field.field_name)"
                            v-validate="field.is_required ? 'required' : ''"
                          ></v-text-field>
                        </template>
                        <template v-if="field.field_type === 'date'">
                          <v-menu
                            v-model="dateWidget"
                            :close-on-content-click="false"
                            :nudge-right="40"
                            lazy
                            transition="scale-transition"
                            offset-y
                            full-width
                            min-width="290px">
                            <template v-slot:activator="{ on }">
                              <v-text-field
                                v-model="field.value"
                                :name="field.field_name"
                                :label="makeLabel(field.field_name)"
                                :error-messages="errors.first(field.field_name)"
                                v-validate="field.is_required ? 'required' : ''"
                                prepend-icon="event"
                                v-on="on"
                              ></v-text-field>
                            </template>
                            <v-date-picker color="success" v-model="field.value" @input="dateWidget = false"></v-date-picker>
                          </v-menu>
                        </template>
                        <template v-if="field.field_type === 'time'">
                          <v-menu
                            ref="menu"
                            v-model="timeWidget"
                            :close-on-content-click="false"
                            :nudge-right="40"
                            :return-value.sync="field.value"
                            lazy
                            transition="scale-transition"
                            offset-y
                            full-width
                            max-width="290px"
                            min-width="290px">
                            <template v-slot:activator="{ on }">
                              <v-text-field
                                v-model="field.value"
                                :name="field.field_name"
                                :label="makeLabel(field.field_name)"
                                :error-messages="errors.first(field.field_name)"
                                v-validate="field.is_required ? 'required' : ''"
                                prepend-icon="access_time"
                                readonly
                                v-on="on"
                              ></v-text-field>
                            </template>
                            <v-time-picker
                              v-if="timeWidget"
                              v-model="field.value"
                              color="success"
                              full-width
                              @click:minute="$refs.menu[0].save(field.value)"
                            ></v-time-picker>
                          </v-menu>
                        </template>
                        <template v-if="field.field_type === 'file'">
                          <v-text-field
                            v-model="field.value"
                            :name="field.field_name"
                            :label="makeLabel(field.field_name)"
                            :type="field.field_type"
                            :error-messages="errors.first(field.field_name)"
                            v-validate="field.is_required ? 'required' : ''"
                          ></v-text-field>
                        </template>
                        <template v-if="field.field_type === 'url'">
                          <v-text-field
                            v-model="field.value"
                            :name="field.field_name"
                            :label="makeLabel(field.field_name)"
                            :type="field.field_type"
                            :error-messages="errors.first(field.field_name)"
                            v-validate="field.is_required ? 'required|url' : ''"
                          ></v-text-field>
                        </template>
                        <template v-if="field.field_type === 'range'">
                          <v-layout>
                            <v-flex
                              shrink
                              style="width: 60px">
                              <v-text-field
                                v-model="field.value[0]"
                                class="mt-0"
                                hide-details
                                single-line
                                type="number"
                                :name="`${field.field_name}_min`"
                                v-validate="field.is_required ? 'required' : ''"
                              ></v-text-field>
                            </v-flex>

                            <v-flex>
                              <v-range-slider
                                v-model="field.value"
                                :name="field.field_name"
                                :label="makeLabel(field.field_name)"
                                :max="field.generatedOptions[1].value"
                                :min="field.generatedOptions[0].value"
                                :step="1"
                              ></v-range-slider>
                            </v-flex>

                            <v-flex
                              shrink
                              style="width: 60px">
                              <v-text-field
                                v-model="field.value[1]"
                                class="mt-0"
                                hide-details
                                single-line
                                type="number"
                                :name="`${field.field_name}_max`"
                                v-validate="field.is_required ? 'required' : ''"
                              ></v-text-field>
                            </v-flex>
                          </v-layout>
                        </template>
                        <template v-if="field.field_type === 'number'">
                          <v-text-field
                            v-model="field.value"
                            :name="field.field_name"
                            :label="makeLabel(field.field_name)"
                            :type="field.field_type"
                            :error-messages="errors.first(field.field_name)"
                            v-validate="field.is_required ? 'required' : ''"
                          ></v-text-field>
                        </template>
                        <template v-if="field.field_type === 'checkbox'">
                          <label class="v-label theme--light">{{ field.field_name }}</label>
                          <template v-for="(checkBox, i) in field.generatedOptions">
                            <v-checkbox
                              v-model="checkBox.value"
                              :label="makeLabel(checkBox.text)"
                              :name="`${field.field_name}_${i}`"
                              v-validate="field.is_required ? 'required' : ''"
                              hide-details
                            ></v-checkbox>
                          </template>
                        </template>
                        <template v-if="field.field_type === 'radio'">
                          <v-radio-group
                            v-model="field.value"
                            :label="makeLabel(field.field_name)"
                            :name="field.field_name"
                            v-validate="field.is_required ? 'required' : ''">
                            <v-radio
                              v-for="n in field.generatedOptions"
                              :key="n.value"
                              :label="makeLabel(n.text)"
                              :value="n.value"
                            ></v-radio>
                          </v-radio-group>
                        </template>

                        <template v-if="field.field_type === 'select'">
                          <v-select
                            v-model="field.value"
                            :items="field.generatedOptions"
                            :name="field.field_name"
                            :label="makeLabel(field.field_name)"
                            :type="field.field_type"
                            :error-messages="errors.first(field.field_name)"
                            v-validate="field.is_required ? 'required' : ''"
                          ></v-select>
                        </template>

                        <template v-if="field.field_type === 'textarea'">
                          <v-textarea
                            v-model="field.value"
                            :name="field.field_name"
                            :label="makeLabel(field.field_name)"
                            :error-messages="errors.first(field.field_name)"
                            v-validate="field.is_required ? 'required' : ''"
                          ></v-textarea>
                        </template>
                      </v-flex>
                    </v-layout>
                  </v-container>
                </v-form>
              </v-card-text>

              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="blue darken-1" flat @click="dialog = false">Cancel</v-btn>
                <v-btn color="blue darken-1" flat
                 :disabled="errors.any()"
                 @click="handleSubmit">Save</v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>
        </v-toolbar>
        <v-data-table
          :headers="headers"
          :items="risks"
          class="elevation-1 max-table-width">
          <template v-slot:items="props">
            <td class="text-xs-center" v-for="item in props.item.risk_data">{{ displayTextValue(item) }}</td>
            <td class="justify-center layout px-0">
              <v-icon small class="mr-2" @click="editItem(props.item)">
                edit
              </v-icon>
              <v-icon small @click="deleteItem(props.item)">
                delete
              </v-icon>
            </td>
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

      <v-snackbar
        v-model="snackbar"
        :color="snackbarColor"
        :multi-line="true"
        :timeout="6000">
        {{ snackbarText }}
        <v-btn dark flat @click="snackbar = false">Close</v-btn>
      </v-snackbar>
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
      deleteDialog: false,
      dateWidget: false,
      timeWidget: false,
      riskTypeId: null,
      typeName: null,
      schema: [],
      fieldValue: { value: null },
      rangeFieldValue: { value: [] },
      generatedOptions: { generatedOptions: [] },
      isActive: null,
      headers: [],
      risks: [],
      riskObj: {},
      editedIndex: -1,
      snackbar: false,
      snackbarText: null,
      snackbarColor: null,
      error: null,
    }),

    computed: {
      formTitle () {
        return this.editedIndex === -1 ?
          `New Risk Item for "${this.typeName}" Risk Type` :
          `Edit Risk Item for "${this.typeName}" Risk Type`
      },
      panelTitle () {
        return this.typeName === null ? 'Risks' : `Risks for "${this.typeName}" Risk Type`
      }
    },

    watch: {
      dialog (val) {
        val || this.close()
      }
    },

    created () {
      eventHub.$on('list-item-clicked', ({id, type_name, schema, is_active}) => {
        if (!this.riskTypeId === false || !this.typeName === false
          || !this.schema.length === false || !this.isActive === false) {
          // Clear variables before assign
          this.riskTypeId = null;
          this.typeName = null;
          this.schema = [];
          this.isActive = null;
          this.generatedOptions = Object.assign({}, { generatedOptions: [] });
        }
        this.riskTypeId = id;
        this.typeName = type_name;
        this.schema = Object.assign([], this.schema, schema);
        this.schema.forEach((item, index) => {
        //  Update schema with value property for using in v-model
          if (item.field_type === 'range') {
            this.schema[index] = Object.assign(this.schema[index], this.rangeFieldValue);
          } else {
            this.schema[index] = Object.assign(this.schema[index], this.fieldValue);
          }
          if ((item.field_type === 'checkbox') || (item.field_type === 'radio')
            || (item.field_type === 'select') || (item.field_type === 'range')) {
            let fieldType = null;
            if ((item.field_type === 'checkbox') || (item.field_type === 'range')) {
              // For providing true/false values to checkboxes and min/max values to ranges.
              fieldType = item.field_type;
            }
            this.generatedOptions.generatedOptions = this.makeOptions(item.options, fieldType);
            this.schema[index] = Object.assign(this.schema[index], this.generatedOptions);
            if ((item.field_type === 'range')) {
              // For providing min/max values to ranges
              let gOptions = this.generatedOptions.generatedOptions;
              this.schema[index] = Object.assign(this.schema[index],
                { 'value': [gOptions[0].value + 1, gOptions[1].value - 1] });
            }
          }
        });
        this.isActive = is_active;
        this.makeHeaders();
        this.getRisks();
      });
    },

    methods: {
      showSnackbar (color, message) {
        // Trigger snackbar with appropriate message.
        this.snackbar = false;
        setTimeout(() => {
          this.snackbarText = message;
          this.snackbarColor = color;
          this.snackbar = true;
        }, 250);
      },
      getRisks () {
        if (this.riskTypeId) {
          apiService.getRisks(this.riskTypeId)
            .then((data) => {
              if (data.status === 200) {
                this.risks = Object.assign([], data.data.results);
              } else {
                this.error = data.error;
                this.showSnackbar('red', `${this.error}`);
              }
            });
        }
      },

      editItem (item) {
        this.editedIndex = this.risks.indexOf(item);
        this.riskObj = Object.assign({}, item);
        this.schema = this.riskObj.risk_data;
        this.dialog = true
      },

      close () {
        setTimeout(() => {
          if (this.editedIndex === -1) {
            this.schema.forEach((item, index) => {
              // clear values on close
              this.schema[index].value = null;
            });
            this.riskObj = {};
          }
          this.editedIndex = -1
        }, 300)
      },

      handleSubmit () {
        if (this.editedIndex > -1) {
          apiService.updateRisk(this.riskObj.id, this.riskObj)
            .then((response) => {
              if (response.status === 200) {
                Object.assign(this.risks[this.editedIndex], this.riskObj);
                this.showSnackbar('success', `You successfully updated Risk item for "${this.typeName}" Risk Type!`);
                this.dialog = false;
              }
            }).catch((error) => {
              this.showSnackbar('red', `${error}`);
          });
        } else {
          this.riskObj = Object.assign(this.riskObj, { 'risk_type': this.riskTypeId });
          this.riskObj = Object.assign(this.riskObj, { 'risk_data': this.schema });
          apiService.createRisk(this.riskObj)
            .then((response) => {
              if (response.status === 201) {
                this.risks.push(response.data);
                this.showSnackbar('success', `You successfully created Risk item!`);
                this.dialog = false;
              }
            }).catch((error) => {
              this.showSnackbar('red', `${error}`);
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
            this.headers.push({ text: temp, value: item.field_name, align: 'center' });
          });
          this.headers.push({ text: 'Actions', value: 'actions', align: 'center' });
          return this.headers;
        }
      },

      makeLabel (fieldName) {
        // Provide Label name created from field_name property.
        const pattern = /\_/;
        if (pattern.test(fieldName) === true) {
          fieldName = fieldName.replace(/\_/g, ' ');
        }
        // Make upper case first letter
        fieldName = fieldName.charAt(0).toUpperCase() + fieldName.slice(1);
        return fieldName;
      },

      makeOptions (optionsString, fieldType=null) {
        // Create options for select field (widget) and variants for radio buttons and checkboxes.
        let pieces = null;
        const pattern = /,\s|,/g;
        if (pattern.test(optionsString) === true) {
          pieces = optionsString.split(pattern);
        }
        let options = [];
        pieces.forEach((item, index) => {
          if (fieldType === 'checkbox') {
            index = false;
          }
          if (fieldType === 'range') {
            index = +item;
          }
          options.push({ text: item, value: index });
        });
        return options;
      },

      displayTextValue (item) {
        let result = null;
        if (item.field_type === 'textarea') {
          result = item.value.substring(0, 20);
          return `${result}...`;
        } else if (item.field_type === 'radio') {
          item.generatedOptions.forEach((part, index) => {
            if (item.value === part.value) {
              result = part.text;
              return result;
            }
          });
        } else if (item.field_type === 'checkbox') {
          let temp = '';
          item.generatedOptions.forEach((part, index) => {
            if (part.value === true) {
              temp += `${part.text}, `;
            }
            return result;
          });
          result = temp;
        } else {
          result = item.value;
          return result;
        }
        return result;
      },
    }
  }
</script>

<style scoped>
  .max-table-width {
    max-width: 850px;
  }
</style>
