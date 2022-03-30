<template lang="pug">
v-tooltip(v-bind:[position]="true", max-width="400px")
  template(v-slot:activator="{ on, attrs }")
    span.tooltip-span(v-if="showUnderline", v-bind="attrs", v-on="on")
      slot
    span(v-else, v-bind="attrs", v-on="on")
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
    showUnderline: {
      type: Boolean,
      default: true,
    },
    position: {
      type: String,
      default: "bottom",
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
