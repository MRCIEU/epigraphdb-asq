<template>
  <v-container>
    <div v-if="queryAllDone">
      <evidence />
    </div>
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";

import Evidence from "./results/Evidence.vue";

export default Vue.extend({
  name: "Results",
  components: {
    Evidence,
  },
  data() {
    return {
      //
    };
  },
  computed: {
    queryAllDone(): boolean {
      const res = this.$store.getters["queryStage/queryAllDone"];
      return res;
    },
  },
});
</script>
