<template>
  <div>
    <v-row>
      <v-col cols="6">
        <h4>Documentation</h4>
        <p class="blockquote">
          <vue-markdown :source="docs" :breaks="false" />
        </p>
      </v-col>
      <v-col cols="6">
        <h4>Evidence summary</h4>
        <p v-if="stat">
          <span>Number of evidence items: &nbsp;</span>
          <b>{{ stat.numEvidenceItems }}</b>
          <br />
          <span>Aggregated association strength score: &nbsp;</span>
          {{ stat.aggAssocStrengthScore }}
          <span>&nbsp; &nbsp; &nbsp; &nbsp;</span>
          <span>Average score: &nbsp;</span>
          <b>{{ stat.avgAssocStrengthScore }}</b>
          <br />
          <span>Aggregated evidence score: &nbsp;</span>
          {{ stat.aggEvidenceScore }}
          <span>&nbsp; &nbsp; &nbsp; &nbsp;</span>
          <span>Average score: &nbsp;</span>
          <b>{{ stat.avgEvidenceScore }}</b>
        </p>
        <div v-if="histogramSeries">
          <assoc-summary-chart
            :assoc-scores="histogramSeries.assocScores"
            :evidence-scores="histogramSeries.evidenceScores"
          />
        </div>
      </v-col>
    </v-row>
    <h4>Association evidence</h4>
    <v-data-table
      :headers="assocHeaders"
      :items="assocItems"
      show-expand
      item-key="idx"
    >
      <template v-slot:header.mapping_score="{ header }">
        <tooltip :docs="$store.state.docs.scores.mappingScore">
          {{ header.text }}
        </tooltip>
      </template>
      <template v-slot:header.assoc_score="{ header }">
        <tooltip :docs="$store.state.docs.scores.assocScore">
          {{ header.text }}
        </tooltip>
      </template>
      <template v-slot:header.evidence_score="{ header }">
        <tooltip :docs="$store.state.docs.scores.evidenceScore">
          {{ header.text }}
        </tooltip>
      </template>
      <template v-slot:item.subject_term="{ item }">
        <div>
          <span class="font-weight-thin">Gwas:</span>
          &nbsp;
          <span>
            <code>{{ item.subject_id }}</code>
          </span>
          <br />
          <a :href="item.subject_url" target="_blank">
            <span>{{ item.subject_term }}</span>
          </a>
        </div>
      </template>
      <template v-slot:item.object_term="{ item }">
        <div>
          <span class="font-weight-thin">Gwas:</span>
          &nbsp;
          <span>
            <code>{{ item.object_id }}</code>
          </span>
          <br />
          <a :href="item.object_url" target="_blank">
            <span>{{ item.object_term }}</span>
          </a>
        </div>
      </template>
      <template v-slot:item.links="{ item }">
        <div v-if="item.topicUrl">
          <div>
            <span>
              <v-icon>mdi-open-in-new</v-icon>
              <a :href="item.topicUrl" target="_blank">EpiGraphDB topic view</a>
            </span>
          </div>
        </div>
        <div v-else>N/A</div>
      </template>
      <template v-slot:item.effect_size="{ item }">
        <div v-if="Math.abs(item.effect_size) <= 0.001">
          {{ item.effect_size.toExponential(4) }}
        </div>
        <div v-else>
          {{ item.effect_size.toFixed(4) }}
        </div>
      </template>
      <template v-slot:item.se="{ item }">
        <div v-if="Math.abs(item.se) <= 0.001">
          {{ item.se.toExponential(4) }}
        </div>
        <div v-else>
          {{ item.se.toFixed(4) }}
        </div>
      </template>
      <template v-slot:item.pval="{ item }">
        <div>
          {{ item.pval.toExponential(4) }}
        </div>
      </template>
      <template v-slot:item.mapping_score="{ item }">
        <div>
          {{ item.mapping_score.toFixed(4) }}
        </div>
      </template>
      <template v-slot:item.assoc_score="{ item }">
        <div>
          {{ item.assoc_score.toFixed(4) }}
        </div>
      </template>
      <template v-slot:item.evidence_score="{ item }">
        <div>
          {{ item.evidence_score.toFixed(4) }}
        </div>
      </template>
      <template v-slot:expanded-item="{ headers, item }">
        <td :colspan="headers.length">
          <div>
            <h5>Entity harmonization data</h5>
            <json-viewer
              theme="json-viewer-gruvbox-dark"
              :expand-depth="4"
              :value="item.mapping_data"
            />
            <h5>EpiGraphDB relationship data</h5>
            <json-viewer
              theme="json-viewer-gruvbox-dark"
              :expand-depth="9"
              :value="item.rel_data"
            />
          </div>
        </td>
      </template>
    </v-data-table>
    <div v-if="assocItems.length > 0">
      <h4>Plots</h4>
      <v-dialog v-model="focus" width="1080">
        <template v-slot:activator="{ on, attrs }">
          <v-btn small tile color="secondary" dark v-bind="attrs" v-on="on">
            Focus
          </v-btn>
        </template>
        <forest-plot :assoc-data="assocItems" />
      </v-dialog>
      <div>
        <forest-plot :assoc-data="assocItems" />
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from "vue";

import ForestPlot from "./AssocForestPlot.vue";
import AssocSummaryChart from "./AssocSummaryChart.vue";

export default Vue.extend({
  name: "EvidenceResults",
  components: {
    ForestPlot,
    AssocSummaryChart,
  },
  props: {
    docs: {
      type: String,
      default: "",
    },
    assocEvidence: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      focus: false,
      assocHeaders: [
        {
          text: "#",
          value: "idx",
        },
        {
          text: "Subject",
          value: "subject_term",
        },
        {
          text: "Object",
          value: "object_term",
        },
        {
          text: "Direction",
          value: "direction",
        },
        {
          text: "Source",
          value: "meta_rel",
        },
        {
          text: "Effect size",
          value: "effect_size",
        },
        {
          text: "SE",
          value: "se",
        },
        {
          text: "P-Value",
          value: "pval",
        },
        {
          text: "Entity harmonization score",
          value: "mapping_score",
        },
        {
          text: "Association strength score",
          value: "assoc_score",
        },
        {
          text: "Evidence score",
          value: "evidence_score",
        },
        {
          text: "Links",
          value: "links",
        },
        {
          text: "Detail data",
          value: "data-table-expand",
        },
      ],
    };
  },
  computed: {
    stat(): Record<string, number | string> {
      const evidenceEmpty =
        this.assocItems == null || this.assocItems.length == 0;
      const numEvidenceItems = evidenceEmpty ? 0 : this.assocItems.length;
      const aggEntHarmonizationScore = evidenceEmpty
        ? "N/A"
        : this._.chain(this.assocItems)
            .map((item) => item.mapping_score)
            .sum()
            .value()
            .toFixed(4);
      const aggAssocStrengthScore = evidenceEmpty
        ? "N/A"
        : this._.chain(this.assocItems)
            .map((item) => item.assoc_score)
            .sum()
            .value()
            .toFixed(4);
      const avgAssocStrengthScore = evidenceEmpty
        ? "NA"
        : (aggAssocStrengthScore / numEvidenceItems).toFixed(4);
      const aggEvidenceScore = evidenceEmpty
        ? "N/A"
        : this._.chain(this.assocItems)
            .map((item) => item.evidence_score)
            .sum()
            .value()
            .toFixed(4);
      const avgEvidenceScore = evidenceEmpty
        ? "NA"
        : (aggEvidenceScore / numEvidenceItems).toFixed(4);
      const res = {
        numEvidenceItems: numEvidenceItems,
        aggEntHarmonizationScore: aggEntHarmonizationScore,
        aggAssocStrengthScore: aggAssocStrengthScore,
        avgAssocStrengthScore: avgAssocStrengthScore,
        aggEvidenceScore: aggEvidenceScore,
        avgEvidenceScore: avgEvidenceScore,
      };
      return res;
    },
    assocItems(): Array<any> {
      const res = this._.chain(this.assocEvidence.data)
        .map((item) => {
          var larrow = "";
          var rarrow = "";
          if (item["direction"] == "forward") {
            larrow = "";
            rarrow = ">";
          } else if (item["direction"] == "reverse") {
            larrow = "<";
            rarrow = "";
          } else if (item["direction"] == "undirectional") {
            larrow = " ";
            rarrow = "";
          }
          const idx = item.idx;
          const critVal = 1.96;
          const label = `<b>${idx}</b> ${item.subject_term} ${larrow}-${rarrow} ${item.object_term}`;
          const lbound = item["effect_size"] - critVal * item["se"];
          const ubound = item["effect_size"] + critVal * item["se"];
          const topicUrl =
            item.meta_rel !== "MR_EVE_MR"
              ? null
              : this.mrUrlFormatter(
                  item.subject_term,
                  item.object_term,
                  item.pval,
                );
          const res = {
            ...item,
            lbound: lbound,
            ubound: ubound,
            label: label,
            topicUrl: topicUrl,
            links: null,
            idx: idx,
          };
          return res;
        })
        .value();
      return res;
    },
    histogramSeries(): Record<string, number> {
      const assocScores = this._.chain(this.assocItems)
        .map((e) => e.assoc_score)
        .value();
      const evidenceScores = this._.chain(this.assocItems)
        .map((e) => e.evidence_score)
        .value();
      const res = {
        assocScores: assocScores,
        evidenceScores: evidenceScores,
      };
      return res;
    },
  },
  methods: {
    mrUrlFormatter(
      subjectTerm: string,
      objectTerm: string,
      pval: number,
    ): string | null {
      if (pval > 0.1) return null;
      const subj = subjectTerm.replace(" ", "+");
      const obj = objectTerm.replace(" ", "+");
      const pvalStr = pval <= 0.01 ? "1e-2" : "1e-1";
      const url = "https://epigraphdb.org/mr/";
      const res = `${url}?exposure-query=${subj}&outcome-query=${obj}&pval=${pvalStr}`;
      return res;
    },
    toggleFullscreen(elemId) {
      const elem = this.$el.querySelector(elemId);
      this.$fullscreen.toggle(elem);
    },
  },
});
</script>

<style scoped></style>
