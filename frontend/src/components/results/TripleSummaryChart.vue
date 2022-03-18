<template>
  <div>
    <v-tabs right>
      <v-tab>Evidence scores</v-tab>
      <v-tab-item>
        <highcharts v-if="evidenceOptions" :options="evidenceOptions" />
      </v-tab-item>
      <v-tab>Triple strength scores</v-tab>
      <v-tab-item>
        <highcharts v-if="tripleOptions" :options="tripleOptions" />
      </v-tab-item>
    </v-tabs>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import { PropType } from "vue";

import Highcharts from "highcharts";
import highchartMoreInit from "highcharts/highcharts-more";
import histogramInit from "highcharts/modules/histogram-bellcurve";
import { Chart } from "highcharts-vue";
import { theme } from "@/resources/highchart-theme";

import { makeHistogramOptions } from "@/funcs/highchart-charts";

Highcharts.setOptions(theme);
highchartMoreInit(Highcharts);
histogramInit(Highcharts);

export default Vue.extend({
  name: "TripleSummaryChart",
  components: {
    highcharts: Chart,
  },
  props: {
    tripleScores: {
      type: Array as PropType<number[]>,
      required: true,
    },
    evidenceScores: {
      type: Array as PropType<number[]>,
      required: true,
    },
  },
  data: () => ({
    //
  }),
  computed: {
    evidenceOptions: function (): Record<string, any> {
      const res = makeHistogramOptions(this.evidenceScores, "Evidence scores");
      return res;
    },
    tripleOptions: function (): Record<string, any> {
      const res = makeHistogramOptions(
        this.tripleScores,
        "Triple strength scores",
      );
      return res;
    },
  },
  methods: {
    //
  },
});
</script>
