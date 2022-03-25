<template lang="pug">
v-tooltip(bottom, max-width="400px")
  template(v-slot:activator="{ on, attrs }")
    span.tooltip-span(v-bind="attrs", v-on="on")
      slot
  vue-markdown(:source="docs", :breaks="false")
</template>

<script lang="ts">
import Vue from "vue";

export default Vue.extend({
  name: "Tooltip",
  props: {
    docs: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      //
    };
  },
});
</script>

<style scoped>
.tooltip-span {
  text-decoration: underline dotted grey 1px;
}
</style>
