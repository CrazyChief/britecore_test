<template>
    <v-flex xs12>
        <v-card dark color="primary">
            <v-toolbar flat color="green">
              <v-toolbar-title>Risk Types</v-toolbar-title>
                <p v-show="riskTypes"></p>
              <v-divider
                class="mx-2"
                inset
                vertical
              ></v-divider>
              <v-spacer></v-spacer>
                <v-btn fab dark small color="primary">
                  <v-icon dark>add</v-icon>
                </v-btn>
            </v-toolbar>
            <v-list>
              <v-list-tile
                v-for="item in riskTypeItems"
                :key="item.type_name"
                @click=""
              >
                <v-list-tile-content>
                  <v-list-tile-title v-text="item.type_name"></v-list-tile-title>
                </v-list-tile-content>

              </v-list-tile>
            </v-list>
        </v-card>
    </v-flex>
</template>

<script>
    export default {
        name: 'RiskTypes',
    }
</script>

<style scoped>

</style>
