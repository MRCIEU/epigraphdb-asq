<template>
  <div class="text-center py-3">
    <p>Now loading: {{ message }}...</p>
    <v-progress-circular indeterminate :size="75" />
  </div>
</template>

<script lang="ts">
import Vue from "vue";

export default Vue.extend({
  name: "Loading",
  props: {
    message: {
      type: String,
      default: null,
    },
  },
});
</script>
