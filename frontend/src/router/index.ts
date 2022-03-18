import Vue from "vue";
import VueRouter, { RouteConfig } from "vue-router";
import Home from "../views/Home.vue";
import TripleView from "../views/TripleView.vue";
import AnalysisView from "../views/AnalysisView.vue";

Vue.use(VueRouter);

const routes: Array<RouteConfig> = [
  {
    path: "/",
    name: "Home",
    component: Home,
  },
  {
    path: "/triple",
    name: "TripleView",
    component: TripleView,
  },
  {
    path: "/medrxiv-analysis",
    name: "SystematicAnalysis",
    component: AnalysisView,
  },
  {
    path: "/about",
    name: "About",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/About.vue"),
  },
  {
    path: "/docs",
    name: "Docs",
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/Docs.vue"),
  },
  {
    path: "/loading",
    name: "Loading",
    component: () =>
      import(
        /* webpackChunkName: "about" */ "../components/widgets/LoadingScreen.vue"
      ),
  },
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

export default router;
