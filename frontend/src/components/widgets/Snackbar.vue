<template>
  <v-snackbar
    v-model="snackbar.visible"
    :timeout="null"
    multi-line
    bottom
    :color="snackbar.color"
  >
    <span v-html="snackbar.text" />
    <template v-slot:action="{ attrs }">
      <v-btn text outlined v-bind="attrs" @click="closeSnackbar">Close</v-btn>
    </template>
  </v-snackbar>
</template>

<script lang="ts">
import Vue from "vue";

export default Vue.extend({
  name: "SnackbarWidget",
  computed: {
    snackbar() {
      return this.$store.state.snackbar;
    },
  },
  methods: {
    closeSnackbar() {
      this.$store.commit("snackbar/closeSnackbar");
    },
  },
});
</script>
