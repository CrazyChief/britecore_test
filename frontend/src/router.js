import Vue from "vue";
import VueRouter from "vue-router";
import Home from "@/views/Home";
import Dashboard from "@/views/Dashboard";

Vue.use(VueRouter);

const isProdEnv = process.env.NODE_ENV === 'production';

const router =  new VueRouter({
  mode: "history",
  routes: [
    {
      path: isProdEnv ? "/dev/" : "/",
      name: "home",
      component: Home
    },
    {
      path: isProdEnv ? "/dev/dashboard/" : "/dashboard/",
      name: "dashboard",
      component: Dashboard
    }
  ]
});

export default router;
