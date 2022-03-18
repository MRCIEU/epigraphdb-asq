<template>
  <div>
    <v-tabs height="30">
      <v-tab><span class="caption">Simple count</span></v-tab>
      <v-tab-item>
        <highcharts v-if="entCountOptions" :options="entCountOptions" />
        <highcharts v-if="tripleCountOptions" :options="tripleCountOptions" />
        <highcharts v-if="assocCountOptions" :options="assocCountOptions" />
      </v-tab-item>
      <v-tab><span class="caption">Entity mapping</span></v-tab>
      <v-tab-item>
        <highcharts
          v-if="ontologyMappingOptions"
          :options="ontologyMappingOptions"
        />
        <highcharts v-if="umlsMappingOptions" :options="umlsMappingOptions" />
        <highcharts v-if="traitMappingOptions" :options="traitMappingOptions" />
      </v-tab-item>
      <v-tab><span class="caption">Evidence scores</span></v-tab>
      <v-tab-item>
        <highcharts v-if="tripleScoreOptions" :options="tripleScoreOptions" />
        <highcharts v-if="assocScoreOptions" :options="assocScoreOptions" />
      </v-tab-item>
    </v-tabs>
  </div>
</template>

<script lang="ts">
import Vue from "vue";

import Highcharts from "highcharts";
import { Chart } from "highcharts-vue";

import { theme } from "@/resources/highchart-theme";
import {
  ASSOC_EVIDENCE_DETAILS,
  TRIPLE_EVIDENCE_DETAILS,
} from "@/resources/evidence-types";

Highcharts.setOptions(theme);

export default Vue.extend({
  name: "SummaryChart",
  components: {
    highcharts: Chart,
  },
  data: () => ({
    entCats: ["Ontology", "UMLS", "GWAS traits"],
    palatte: ["#2196F3", "#4CAF50", "#FF9800", "#795548"],
    jitterWidth: 0.15,
    jitterMarkerRadius: 5,
  }),
  computed: {
    tripleCats: function (): Array<string> {
      const predGroup = this.$store.getters["ents/predGroup"];
      const labels = this._.chain(TRIPLE_EVIDENCE_DETAILS[predGroup])
        .mapValues((item) => item.label)
        .values()
        .value();
      return labels;
    },
    assocCats: function (): Array<string> {
      const predGroup = this.$store.getters["ents/predGroup"];
      const labels = this._.chain(ASSOC_EVIDENCE_DETAILS[predGroup])
        .mapValues((item) => item.label)
        .values()
        .value();
      return labels;
    },
    entCountOptions: function (): Record<string, any> {
      const series = [
        {
          name: "Subjects",
          data: [
            this.$store.state.ents.ontologySubjectEnts.ents.length,
            this.$store.state.ents.umlsSubjectEnts.ents.length,
            this.$store.state.ents.traitSubjectEnts.ents.length,
          ],
        },
        {
          name: "Objects",
          data: [
            this.$store.state.ents.ontologyObjectEnts.ents.length,
            this.$store.state.ents.umlsObjectEnts.ents.length,
            this.$store.state.ents.traitObjectEnts.ents.length,
          ],
        },
      ];
      const res = {
        chart: {
          type: "bar",
        },
        title: {
          text: "Entity harmonization",
        },
        xAxis: {
          categories: this.entCats,
        },
        yAxis: {
          min: 0,
          title: {
            text: "Number of entities",
          },
        },
        plotOptions: {
          series: {
            stacking: "normal",
          },
          bar: {
            dataLabels: {
              enabled: true,
            },
          },
        },
        credits: {
          enabled: false,
        },
        series: series,
      };
      return res;
    },
    tripleCountOptions: function (): Record<string, any> {
      const tripleCounts = this._.chain(
        this.$store.getters["evidence/tripleEvidence"],
      )
        .mapValues((item) => item.length)
        .values()
        .value();
      const literatureCounts = this._.chain(
        this.$store.getters["evidence/literatureEvidence"],
      )
        .mapValues((item) => item.data.length)
        .values()
        .value();
      const series = [
        {
          name: "Triple evidence",
          data: tripleCounts,
        },
        {
          name: "Literature evidence",
          data: literatureCounts,
        },
      ];
      const res = {
        chart: {
          type: "bar",
        },
        title: {
          text: "Triple and literature evidence",
        },
        xAxis: {
          categories: this.tripleCats,
        },
        yAxis: {
          min: 0,
          title: {
            text: "Number of evidence items",
          },
        },
        plotOptions: {
          series: {
            stacking: "normal",
          },
          bar: {
            dataLabels: {
              enabled: true,
            },
          },
        },
        credits: {
          enabled: false,
        },
        series: series,
      };
      return res;
    },
    assocCountOptions: function (): Record<string, any> {
      const assocCounts = this._.chain(
        this.$store.getters["evidence/assocEvidence"],
      )
        .mapValues((item) => item.data.length)
        .values()
        .value();
      const series = [
        {
          name: "Association evidence",
          data: assocCounts,
        },
      ];
      const res = {
        chart: {
          type: "bar",
        },
        title: {
          text: "Association evidence",
        },
        xAxis: {
          categories: this.assocCats,
        },
        yAxis: {
          min: 0,
          title: {
            text: "Number of evidence items",
          },
        },
        credits: {
          enabled: false,
        },
        plotOptions: {
          bar: {
            dataLabels: {
              enabled: true,
            },
          },
        },
        series: series,
      };
      return res;
    },
    ontologyMappingOptions: function (): Record<string, any> {
      const ontologyData = this.$store.getters["ents/ontologyData"];
      const series = [
        {
          name: "Subjects",
          data: this._.chain(ontologyData.subjects.ents)
            .map((e) => [0, e.similarity_score])
            .value(),
          jitter: {
            x: this.jitterWidth,
          },
          marker: {
            radius: this.jitterMarkerRadius,
          },
        },
        {
          name: "Objects",
          data: this._.chain(ontologyData.objects.ents)
            .map((e) => [1, e.similarity_score])
            .value(),
          jitter: {
            x: this.jitterWidth,
          },
          marker: {
            radius: this.jitterMarkerRadius,
          },
        },
      ];
      const res = {
        chart: {
          inverted: true,
          type: "scatter",
        },
        title: {
          text: "EFO",
        },
        xAxis: {
          categories: ["Subjects", "Objects"],
        },
        yAxis: {
          min: 0.5,
          max: 1,
          title: {
            text: "Semantic semilarity score",
          },
        },
        credits: {
          enabled: false,
        },
        series: series,
      };
      return res;
    },
    umlsMappingOptions: function (): Record<string, any> {
      const umlsData = this.$store.getters["ents/umlsData"];
      const series = [
        {
          name: "Subjects",
          data: this._.chain(umlsData.subjects.detailData)
            .map((e) => [0, e.similarity_score])
            .value(),
          jitter: {
            x: this.jitterWidth,
          },
          marker: {
            radius: this.jitterMarkerRadius,
          },
        },
        {
          name: "Objects",
          data: this._.chain(umlsData.objects.detailData)
            .map((e) => [1, e.similarity_score])
            .value(),
          jitter: {
            x: this.jitterWidth,
          },
          marker: {
            radius: this.jitterMarkerRadius,
          },
        },
      ];
      const res = {
        chart: {
          inverted: true,
          type: "scatter",
        },
        title: {
          text: "UMLS terms",
        },
        xAxis: {
          categories: ["Subjects", "Objects"],
        },
        yAxis: {
          min: 0.5,
          max: 1,
          title: {
            text: "Semantic semilarity score",
          },
        },
        credits: {
          enabled: false,
        },
        series: series,
      };
      return res;
    },
    traitMappingOptions: function (): Record<string, any> {
      const traitData = this.$store.getters["ents/traitData"];
      const series = [
        {
          name: "Subjects",
          data: this._.chain(traitData.subjects.detailData)
            .map((e) => [0, e.similarity_score])
            .value(),
          jitter: {
            x: this.jitterWidth,
          },
          marker: {
            radius: this.jitterMarkerRadius,
          },
        },
        {
          name: "Objects",
          data: this._.chain(traitData.objects.detailData)
            .map((e) => [1, e.similarity_score])
            .value(),
          jitter: {
            x: this.jitterWidth,
          },
          marker: {
            radius: this.jitterMarkerRadius,
          },
        },
      ];
      const res = {
        chart: {
          inverted: true,
          type: "scatter",
        },
        title: {
          text: "GWAS traits",
        },
        xAxis: {
          categories: ["Subjects", "Objects"],
        },
        yAxis: {
          min: 0.5,
          max: 1,
          title: {
            text: "Semantic semilarity score",
          },
        },
        credits: {
          enabled: false,
        },
        series: series,
      };
      return res;
    },
    tripleScoreOptions: function (): Record<string, any> {
      const predGroup = this.$store.getters["ents/predGroup"];
      const labels = TRIPLE_EVIDENCE_DETAILS[predGroup];
      const series = this._.chain(
        this.$store.getters["evidence/tripleEvidence"],
      )
        .map((item, key) => {
          const res = {
            name: key,
            data: this._.chain(item)
              .map((e) => e.evidence_score)
              .value(),
          };
          return res;
        })
        .values()
        .map((item, idx) => {
          const label = labels[item.name].label;
          const res = {
            name: label,
            data: this._.chain(item.data)
              .map((e) => [idx, e])
              .value(),
            color: this.palatte[idx],
            jitter: {
              x: this.jitterWidth,
            },
            marker: {
              radius: this.jitterMarkerRadius,
            },
          };
          return res;
        })
        .value();
      const res = {
        chart: {
          type: "scatter",
          inverted: true,
        },
        title: {
          text: "Triple and literature evidence",
        },
        xAxis: {
          categories: this.tripleCats,
        },
        yAxis: {
          min: 0,
          title: {
            text: "Evidence score",
          },
          plotLines: [
            {
              color: "#E65100",
              width: 5,
              value: 1,
            },
          ],
        },
        credits: {
          enabled: false,
        },
        series: series,
      };
      return res;
    },
    assocScoreOptions: function (): Record<string, any> {
      const predGroup = this.$store.getters["ents/predGroup"];
      const labels = ASSOC_EVIDENCE_DETAILS[predGroup];
      const series = this._.chain(this.$store.getters["evidence/assocEvidence"])
        .map((item, key) => ({
          name: key,
          data: this._.chain(item.data)
            .map((e) => e.evidence_score)
            .value(),
        }))
        .values()
        .map((item, idx) => {
          const label = labels[item.name].label;
          const res = {
            name: label,
            data: this._.chain(item.data)
              .map((e) => [idx, e])
              .value(),
            color: this.palatte[idx],
            jitter: {
              x: this.jitterWidth,
            },
            marker: {
              radius: this.jitterMarkerRadius,
            },
          };
          return res;
        })
        .value();
      const res = {
        chart: {
          type: "scatter",
          inverted: true,
        },
        title: {
          text: "Association evidence",
        },
        xAxis: {
          categories: this.assocCats,
        },
        yAxis: {
          min: 0,
          title: {
            text: "Evidence score",
          },
          plotLines: [
            {
              color: "#E65100",
              width: 5,
              value: 1,
            },
          ],
        },
        credits: {
          enabled: false,
        },
        series: series,
      };
      return res;
    },
  },
  methods: {
    //
  },
});
</script>
