<template>
  <v-content>
    <v-container grid-list-xl>
      <v-layout align-space-between justify-space-between row fill-height>
        <Risks />
        <RiskTypes />
      </v-layout>
    </v-container>
  </v-content>
</template>

<script>
import RiskTypes from "../components/RiskTypes";
import Risks from "../components/Risks";


export default {
  name: "Dashboard",
  components: {
    RiskTypes,
    Risks,
  },
}
</script>

<style scoped>

</style>
