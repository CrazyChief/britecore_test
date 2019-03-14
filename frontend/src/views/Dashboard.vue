<template>
    <v-content>
        <v-container grid-list-xl>
            <v-layout align-space-between justify-space-between row fill-height>
                <RiskTypes />
            </v-layout>
        </v-container>
    </v-content>
</template>

<script>
import RiskTypes from "../components/RiskTypes";


export default {
    name: "Dashboard",
    components: {
        RiskTypes,
    },
}
</script>

<style scoped>

</style>
