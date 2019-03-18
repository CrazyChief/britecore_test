<template>
  <v-flex xs5>
    <v-card color="primary">
      <v-toolbar flat color="green">
        <v-toolbar-title>Risk Types</v-toolbar-title>
        <v-divider
          class="mx-2"
          inset
          vertical
        ></v-divider>
        <v-spacer></v-spacer>
          <v-dialog v-model="dialog">
            <template v-slot:activator="{ on }">
              <v-btn fab dark small color="primary" v-on="on">
                <v-icon dark>add</v-icon>
              </v-btn>
            </template>
            <v-card>
              <v-card-title>
                <span class="headline">{{ formTitle }}</span>
              </v-card-title>
                <v-divider class="mx-3" horizontal></v-divider>
              <v-card-text>
                <v-form @submit.prevent="handleSubmit">
                  <v-layout row wrap>
                    <v-flex xs12 md3>
                      <v-text-field
                        v-model="riskTypeName"
                        v-validate="'required'"
                        label="Risk Type Name"
                        :name="'type_name'"
                        :error-messages="errors.first('type_name')"
                      ></v-text-field>
                    </v-flex>
                    <v-flex xs12 md3>
                      <v-checkbox
                        v-model="riskTypeActive"
                        v-validate="'required'"
                        label="Is Risk Type Active?"
                        :name="'is_active'"
                        :error-messages="errors.first('is_active')"
                      ></v-checkbox>
                    </v-flex>
                    <v-spacer></v-spacer>
                    <v-divider inset dark></v-divider>
                    <v-spacer></v-spacer>
                  </v-layout>

                  <template v-for="(form, index) in formsetRows">
                    <v-layout row wrap :key="index">
                      <v-flex xs12 md3>
                        <v-text-field
                          v-model="form.field_name"
                          :key="'field_name' + index"
                          label="Field Name"
                          :name="'field_name' + index"
                          :error-messages="errors.first('field_name' + index)"
                          v-validate="'required'"
                          @input="checkSameFieldNames(form, index)"
                        ></v-text-field>
                      </v-flex>
                      <v-flex xs12 md3>
                        <v-select
                          v-model="form.field_type"
                          :items="fieldsData"
                          :key="'field_type' + index"
                          label="Field Type"
                          :name="'field_type' + index"
                          :error-messages="errors.first('field_type' + index)"
                          v-validate="'required'"
                          @input="checkSelected(form, index, 'options' + index)"
                          ></v-select>
                      </v-flex>
                      <v-flex xs12 md3>
                        <v-text-field
                          v-model="form.options"
                          :name="'options' + index"
                          v-validate="form.optionsDisabled ? '' : 'required'"
                          label="Options (comma separated field)"
                          :error-messages="form.optionsDisabled ? '' : errors.first('options' + index)"
                          :disabled="form.optionDisabled"
                        ></v-text-field>
                      </v-flex>
                      <v-flex xs12 md2>
                        <v-checkbox
                          v-model="form.is_required"
                          label="Is Required?"
                          :name="'checkbox' + index"
                          type="checkbox"
                          ></v-checkbox>
                      </v-flex>
                      <v-flex xs12 md1>
                        <v-tooltip bottom>
                          <template v-slot:activator="{ on }">
                            <v-btn fab dark small color="red"
                             :key="index"
                              @click="removeRow(index)" v-on="on">
                                <v-icon dark>remove</v-icon>
                            </v-btn>
                          </template>
                          <span>Remove provided setting</span>
                        </v-tooltip>
                      </v-flex>
                    </v-layout>
                  </template>
                  <v-btn block color="green" dark
                    @click="addRow">
                      <v-icon dark>add</v-icon>
                      Add Risk Type Setting
                  </v-btn>
                </v-form>
              </v-card-text>

              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="blue darken-1" flat @click="close">Cancel</v-btn>
                <template v-if="editedIndex === -1">
                  <v-btn
                  :disabled="errors.any()"
                  color="blue darken-1" flat
                  @click="handleSubmit">Save</v-btn>
                </template>
                <template v-else>
                  <v-btn
                  :disabled="errors.any()"
                  color="blue darken-1" flat
                  @click="editDialog = true">Save</v-btn>
                </template>
              </v-card-actions>
            </v-card>
          </v-dialog>
      </v-toolbar>
      <v-list>
        <v-list-tile
          v-for="item in riskTypeItems"
          :key="item.id"
          @click="provideRiskType(item)"
        >
          <v-list-tile-content>
            <v-list-tile-title v-text="item.type_name"></v-list-tile-title>
          </v-list-tile-content>
            <v-btn fab dark small color="cyan"
            @click="editItem(item)">
                <v-icon dark>edit</v-icon>
            </v-btn>

        </v-list-tile>
      </v-list>
      <v-snackbar
        v-model="snackbar"
        :color="snackbarColor"
        :multi-line="true"
        :timeout="6000">
        {{ snackbarText }}
        <v-btn dark flat @click="snackbar = false">Close</v-btn>
      </v-snackbar>

      <v-dialog
        v-model="editDialog">
        <!--<template v-slot:activator="{ on }">-->
          <v-card>
            <v-card-title class="headline">Do you really want to make changes?</v-card-title>

            <v-card-text>
              Attention! After schema changes of current ({{ riskTypeName }}) Risk Type data provided in Risks
              can be removed in case you remove old fields in schema. Do you really want to make changes?
            </v-card-text>

            <v-card-actions>
              <v-spacer></v-spacer>

              <v-btn
                color="green darken-1"
                flat="flat"
                @click="editDialog = false">
                Disagree
              </v-btn>

              <v-btn
                color="green darken-1"
                flat="flat"
                @click="handleSubmit">
                Agree
              </v-btn>
            </v-card-actions>
          </v-card>
        <!--</template>-->
      </v-dialog>
    </v-card>
  </v-flex>
</template>

<script>
  import { eventHub } from '../main';
  import { APIService } from '../services/APIService';

  const apiService = new APIService();

  export default {
    name: 'RiskTypes',
    data () {
      return {
        dialog: false,
        editDialog: false,
        loading: true,
        riskTypeItems: [],
        riskType: {},
        error: null,
        optionsDisabled: true,
        editedIndex: -1,
        riskTypeId: null,
        riskTypeName: null,
        riskTypeActive: true,
        fieldsData: [
          { text: '', value: null },
          { text: 'Small text field', value: 'text' },
          { text: 'Email field', value: 'email' },
          { text: 'Phone field', value: 'tel' },
          { text: 'Date field', value: 'date' },
          { text: 'Time field', value: 'time' },
          { text: 'File field', value: 'file' },
          { text: 'Image field', value: 'image' },
          { text: 'URL field', value: 'url' },
          { text: 'Range (number) field', value: 'range' },
          { text: 'Number field', value: 'number' },
          { text: 'Checkbox field', value: 'checkbox' },
          { text: 'Radio field', value: 'radio' },
          { text: 'Select field', value: 'select' },
          { text: 'Large field', value: 'textarea' },
          ],
        startFormsetRows: [
          // initial data
          { field_name: '', field_type: '', options: '', optionDisabled: true, is_required: false }
        ],
        formsetRows: [
          // initial data
          { field_name: '', field_type: '', options: '', optionDisabled: true, is_required: false }
        ],
        snackbar: false,
        snackbarText: null,
        snackbarColor: null,
        submitted: false,
      }
    },
    computed: {
      formTitle () {
        return this.editedIndex === -1 ? 'New Risk Type Item' : 'Edit Risk Type Item'
      },
    },
    watch: {
      dialog (val) {
        val || this.close()
      }
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
      getAllRiskTypes () {
        apiService.getAllRiskTypes()
          .then((data) => {
            if (data.status === 200) {
              this.riskTypeItems = data.data.results;
              this.loading = false;
            } else {
              this.error = data.error;
              this.showSnackbar('red', `${this.error}`);
            }
          });
      },
      editItem (item) {
        this.editedIndex = this.riskTypeItems.indexOf(item);
        this.riskTypeId = item.id;
        this.formsetRows = Object.assign([], item.schema);
        this.riskTypeName = item.type_name;
        this.riskTypeActive = item.is_active;
        this.dialog = true
      },
      close () {
        // Closes dialog and pass initial data.
        this.dialog = false;
        this.editDialog = false;
        setTimeout(() => {
          this.riskTypeId = null;
          this.riskTypeName = null;
          this.riskTypeActive = true;
          this.formsetRows = Object.assign([], this.startFormsetRows);
          this.editedIndex = -1;
          this.submitted = false;
          this.$validator.errors.clear();
        }, 300)
      },
      addRow () {
        this.formsetRows.push(
          { field_name: '', field_type: '', options: '', optionDisabled: true, is_required: false });
      },
      removeRow (index) {
        this.formsetRows.splice(index, 1);
      },
      checkSelected (form, index, fieldName=null) {
        // Check selected variant for field_type setting.
        // Provide available field options in case select, radio, checkbox were chosen.
        const value = form.field_type;
        if ((value === 'select') || (value === 'checkbox') || (value === 'radio')) {
          this.formsetRows[index].optionDisabled = false;
        } else {
          this.formsetRows[index].options = '';
          this.formsetRows[index].optionDisabled = true;
          this.$validator.errors.remove(fieldName);
        }
      },
      checkSameFieldNames (form, i) {
        // Checks if the same field name already typed for another setting.
        const fieldName = form.field_name;
        if (fieldName !== '') {
          let msg = 'You already have setting with same field name! ' +
            'Change it, please, to avoid name conflicts!';
          this.formsetRows.forEach((item, index) => {
            if ((i !== index) && (item.field_name === fieldName)) {
              this.$validator.errors.add({
                field: `field_name${index}`,
                msg: msg
              });
              return true;
            } else {
              this.$validator.errors.remove(`field_name${index}`);
              return false;
            }
          });
        }
      },
      handleSubmit() {
        // Makes form validation.
        this.submitted = true;
        this.$validator.validate().then(valid => {
          if (valid) {
            this.riskType = Object.assign(this.riskType, { 'type_name': this.riskTypeName });
            this.riskType = Object.assign(this.riskType, { 'is_active': this.riskTypeActive });
            this.riskType = Object.assign(this.riskType, { 'schema': this.formsetRows });
            if (this.riskTypeId === null) {
              // Send post request to the server in case validation passed.
              apiService.createRiskType(this.riskType)
                .then((response) => {
                  if (response.status === 201) {
                    this.riskTypeItems.push(response.data);
                    this.showSnackbar('success', `You successfully created ${response.data.type_name} risk type`);
                    this.close();
                  }
                }).catch((error) => {
                  this.showSnackbar('red', `${error}`);
                });
            } else {
              // Send put request to the server in case validation passed.
              apiService.updateRiskType(this.riskTypeId, this.riskType)
                .then((response) => {
                  if (response.status === 200) {
                    this.showSnackbar('success', `You successfully updated ${response.data.type_name} risk type`);
                    const updated = response.data;
                    this.riskTypeItems.forEach((item, index) => {
                      if (item.id === updated.id) {
                        this.riskTypeItems[index] = Object.assign(
                          this.riskTypeItems[index], { 'type_name': updated.type_name });
                        this.riskTypeItems[index] = Object.assign(
                          this.riskTypeItems[index], { 'schema': updated.schema });
                        this.riskTypeItems[index] = Object.assign(
                          this.riskTypeItems[index], { 'is_active': updated.is_active });
                        this.provideRiskType(this.riskTypeItems[index]);
                      }
                    });
                    this.close()
                  }
                }).catch((error) => {
                  this.showSnackbar('red', `${error}`);
                });
            }
          } else {
            if (this.riskTypeId !== null) {
              this.editDialog = false;
            }
          }
        });
      },
      provideRiskType (riskType) {
        this.riskType = Object.assign({}, riskType);
        eventHub.$emit('list-item-clicked', this.riskType);
        this.riskType = {};
      },
    },
    mounted () {
      this.getAllRiskTypes();
    },
  }
</script>

<style scoped>

</style>
