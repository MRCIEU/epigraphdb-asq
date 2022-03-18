<template lang="pug">
v-dialog(v-model="showDialog", width="1080")
  template(v-slot:activator="{ on, attrs }")
    v-btn.floating-button(
      v-bind="attrs",
      outlined,
      color="blue-grey",
      @click="showDialog = !showDialog",
      v-on="on"
    )
      v-icon mdi-border-outside
      span Configure parameters (advanced)
  v-card
    v-card-title Adjust query
    v-divider
    adjust-results-params(@regen="update")
</template>

<script lang="ts">
import Vue from "vue";

import AdjustResultsParams from "./AdjustResultsParams.vue";

export default Vue.extend({
  name: "AdjustResults",
  components: {
    AdjustResultsParams,
  },
  data() {
    return {
      showDialog: false,
    };
  },
  computed: {
    //
  },
  methods: {
    async update(): Promise<void> {
      this.showDialog = false;
      await this.$emit("update");
    },
  },
});
</script>
