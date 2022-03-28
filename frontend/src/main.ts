import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import vuetify from "./plugins/vuetify";
import "roboto-fontface/css/roboto/roboto-fontface.css";
import "@mdi/font/css/materialdesignicons.css";
import fullscreen from "vue-fullscreen";

import VueLodash from "vue-lodash";
import lodash from "lodash";
Vue.use(VueLodash, { name: "custom", lodash: lodash });

import "@/plugins/general.css";

import VueMarkdown from "@adapttive/vue-markdown";
import JsonViewer from "vue-json-viewer";
import "@/plugins/json-viewer-gruvbox-dark.scss";
import Tooltip from "@/components/widgets/Tooltip.vue";
Vue.component("VueMarkdown", VueMarkdown);
Vue.component("JsonViewer", JsonViewer);
Vue.component("Tooltip", Tooltip);

Vue.config.productionTip = false;
Vue.use(fullscreen);

// hide console.log when prod
if (process.env.NODE_ENV == "production") {
  const disFunc = () => {};
  console.log = disFunc;
  console.error = disFunc;
  console.warn = disFunc;
  Object.freeze(console);
}

new Vue({
  router,
  store,
  vuetify,
  render: (h) => h(App),
}).$mount("#app");
