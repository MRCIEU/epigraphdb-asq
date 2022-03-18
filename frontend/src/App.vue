<template>
  <v-app>
    <app-bar />
    <v-main>
      <router-view />
      <snackbar-widget />
    </v-main>
    <app-footer />
  </v-app>
</template>

<script lang="ts">
import Vue from "vue";
import AppBar from "@/components/AppBar.vue";
import AppFooter from "@/components/AppFooter.vue";
import SnackbarWidget from "@/components/widgets/Snackbar.vue";

export default Vue.extend({
  name: "App",
  components: {
    AppBar,
    AppFooter,
    SnackbarWidget,
  },
  data: () => ({
    //
  }),
});
</script>
