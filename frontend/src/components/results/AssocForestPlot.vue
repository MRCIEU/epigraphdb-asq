<template>
  <div>
    <highcharts v-if="options" :options="options" />
  </div>
</template>

<script lang="ts">
import Vue from "vue";

import Highcharts from "highcharts";
import highchartMoreInit from "highcharts/highcharts-more";
import dumbbellInit from "highcharts/modules/dumbbell";
import { Chart } from "highcharts-vue";

import { theme } from "@/resources/highchart-theme";

Highcharts.setOptions(theme);
highchartMoreInit(Highcharts);
dumbbellInit(Highcharts);

export default Vue.extend({
  name: "ForestPlot",
  components: {
    highcharts: Chart,
  },
  props: {
    assocData: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      //
    };
  },
  computed: {
    betaData: function (): Array<Array<string | number>> {
      return this._.chain(this.assocData)
        .map((item) => {
          const res = [item["label"], item["effect_size"]];
          return res;
        })
        .value();
    },
    boundData: function (): Array<any> {
      return this._.chain(this.assocData)
        .map((item) => {
          const res = {
            name: item["label"],
            low: item["lbound"],
            high: item["ubound"],
          };
          return res;
        })
        .value();
    },
    options: function (): any {
      const res = {
        chart: {
          inverted: true,
        },
        legend: {
          enabled: false,
        },
        title: {
          text: "Associations evidence",
        },
        tooltip: {
          shared: true,
        },
        xAxis: {
          type: "category",
        },
        yAxis: {
          title: {
            text: "Effect",
          },
          plotLines: [
            {
              color: "#E65100",
              width: 5,
              value: 0,
            },
          ],
        },
        credits: {
          enabled: false,
        },
        series: [
          {
            type: "scatter",
            name: "effect size",
            data: this.betaData,
          },
          {
            type: "dumbbell",
            name: "+-1.96 se",
            data: this.boundData,
          },
        ],
      };
      return res;
    },
  },
  methods: {
    //
  },
});
</script>
