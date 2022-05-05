<template>
  <v-app>
    <app-bar />
    <v-main>
      <router-view />
      <snackbar-widget />
    </v-main>
    <div v-if="gtagId">
      <cookie-consent />
    </div>
    <app-footer />
  </v-app>
</template>

<script lang="ts">
import Vue from "vue";
import AppBar from "@/components/AppBar.vue";
import AppFooter from "@/components/AppFooter.vue";
import SnackbarWidget from "@/components/widgets/Snackbar.vue";
import CookieConsent from "vue-cookieconsent-component";

import { gtagId } from "@/config";

export default Vue.extend({
  name: "App",
  components: {
    AppBar,
    AppFooter,
    SnackbarWidget,
    CookieConsent,
  },
  data: () => ({
    gtagId: gtagId,
  }),
});
</script>

<style lang="scss">
/* $cookieconstent-background: $light !default;
   $cookieconstent-compliance-background: $primary !default; */
@import "~vue-cookieconsent-component/src/scss/cookie-consent";
@import "~vue-cookieconsent-component/src/scss/cookie-consent-bottom";
@import "~vue-cookieconsent-component/src/scss/cookie-consent-transition";
</style>
