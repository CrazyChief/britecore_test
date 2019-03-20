<template>
  <v-app>
    <v-toolbar app color="green">
      <v-toolbar-title class="headline text-uppercase">
        <span>BriteCore </span>
        <span class="font-weight-light">Risk Types and Risks</span>
      </v-toolbar-title>
      <v-spacer></v-spacer>
    </v-toolbar>

    <router-view />

  </v-app>
</template>

<script>
  export default {
    name: 'App'
  }
</script>
