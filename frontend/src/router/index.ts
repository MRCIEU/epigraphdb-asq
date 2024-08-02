import Vue from "vue";
import VueRouter, { RouteConfig } from "vue-router";
import Home from "../views/Home.vue";

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
    component: () =>
      import(/* webpackChunkName: "TripleView" */ "@/views/TripleView.vue"),
  },
  {
    path: "/medrxiv-analysis",
    name: "SystematicAnalysis",
    component: () =>
      import(
        /* webpackChunkName: "SystematicAnalysis" */ "@/views/AnalysisView.vue"
      ),
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
    component: () => import(/* webpackChunkName: "docs" */ "../views/Docs.vue"),
  },
  {
    path: "/tutorial",
    name: "Tutorial",
    component: () =>
      import(/* webpackChunkName: "tutorial" */ "../views/Tutorial.vue"),
  },
  {
    path: "/loading",
    name: "Loading",
    component: () =>
      import(
        /* webpackChunkName: "LoadingScreen" */ "../components/widgets/LoadingScreen.vue"
      ),
  },
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

export default router;
