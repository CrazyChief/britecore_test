import Vue from "vue";
import './plugins/vuetify'
import App from "./App.vue";
import VeeValidate from 'vee-validate'
import router from "./router";
import store from "./store";

Vue.use(VeeValidate);

Vue.config.productionTip = false;

export const eventHub = new Vue();

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount("#app");
