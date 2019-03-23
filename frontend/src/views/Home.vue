<template>
    <v-content>
        <v-container grid-list-xl>
            <v-flex xs12 sm10 offset-sm1>
                <v-card>
                    <v-card-title primary-title>
                        <div>
                            <h3 class="headline mb-0">Welcome!</h3>
                            <div> Hello dear customer! Here you can start to provide Risk Types and Risks for insurers! </div>
                        </div>
                    </v-card-title>

                    <v-card-actions>
                        <v-btn block flat color="green" :href="link">Go to Dashboard</v-btn>
                    </v-card-actions>
                </v-card>
            </v-flex>
        </v-container>
    </v-content>
</template>

<script>
    const isProdEnv = process.env.NODE_ENV === 'production';
    export default {
      name: "Home",
      data: () => ({
        link: isProdEnv ? "/dev/dashboard/" : "/dashboard/"
      })
    }
</script>

<style scoped>

</style>
