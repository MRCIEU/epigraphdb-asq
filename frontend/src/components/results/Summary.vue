<template>
  <div>
    <v-tabs v-model="summaryTab" fixed-tabs>
      <v-tab>Charts</v-tab>
      <v-tab>Statistics</v-tab>
    </v-tabs>
    <div class="py-3" />
    <v-tabs-items v-model="summaryTab">
      <v-tab-item>
        <v-row>
          <v-col cols="4">
            <h3>Summary charts</h3>
            <summary-chart />
          </v-col>
          <v-col>
            <h3>Entity diagram</h3>
            <div class="py-2" />
            <network-plot />
          </v-col>
        </v-row>
      </v-tab-item>
      <v-tab-item>
        <summary-stats v-if="summaryData" :data="summaryData" />
      </v-tab-item>
    </v-tabs-items>
  </div>
</template>

<script lang="ts">
import Vue from "vue";

import * as processing from "@/funcs/processing";

import NetworkPlot from "./NetworkPlot.vue";
import SummaryChart from "./SummaryChart.vue";
import SummaryStats from "./SummaryStats.vue";
import * as types from "@/types/types";

export default Vue.extend({
  name: "EvidenceSummary",
  components: {
    NetworkPlot,
    SummaryChart,
    SummaryStats,
  },
  props: {
    data: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      summaryTab: null,
    };
  },
  computed: {
    summaryData(): any {
      return this.data;
    },
  },
  async mounted() {
    //
  },
  methods: {
    toggleFullscreen(elemId) {
      const elem = this.$el.querySelector(elemId);
      this.$fullscreen.toggle(elem);
    },
  },
});
</script>

<style scoped>
.json-view {
  height: 40rem;
  -ms-overflow-style: none; /* IE and Edge */
  scrollbar-width: none; /* Firefox */
}
.json-view-focused {
  max-height: 800px;
  height: 800px;
}
.json-view::-webkit-scrollbar {
  display: none;
}
</style>
