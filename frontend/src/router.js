import Vue from "vue";
import VueRouter from "vue-router";
import Home from "@/views/Home";
import Dashboard from "@/views/Dashboard";

Vue.use(VueRouter);

const router =  new VueRouter({
  mode: "history",
  routes: [
    {
      path: "/dev/",
      name: "home",
      component: Home
    },
    {
      path: "/dev/dashboard/",
      name: "dashboard",
      component: Dashboard
    }
  ]
});

export default router;
