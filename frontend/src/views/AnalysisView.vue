<template lang="pug">
v-container
  h1 Systematic analysis on medRxiv submissions 2020-2021
  v-card
    v-card-title Options
    v-row.mx-5
      v-col
        div
          h3 General options
          v-subheader Primary terms
          multiselect(
            v-model="termSelect",
            :options="termOptions",
            :multiple="true",
            :close-on-select="true",
            placeholder="Select primary terms of interests or leave empty to pick top count"
          )
          v-subheader Predicate subset
          v-select(
            v-model="predModeSelect",
            :items="predModeOptions",
            outlined,
            dense
          )
      v-col
        div
          h3 Diagram options
          v-subheader Edge width calculation
          v-select(
            v-model="edgeModeSelect",
            :items="edgeModeOptions",
            outlined,
            dense
          )
    v-btn.my-5.mx-5(
      tile,
      color="primary",
      :disabled="btnState.disabled",
      @click="updateData"
    ) {{ btnState.label }}
  v-divider.py-5
  v-tabs(v-model="resultsTab", centered)
    v-tab
      v-tooltip(v-model="showDocsTooltip", top, color="success")
        template(v-slot:activator="{ on, attrs }")
          span(v-bind="attrs", v-on="on") About
        span Read documentation here
        br
        | for first time visitors
    v-tab-item
      .py-2
      v-container(fluid)
        vue-markdown(
          :source="$store.state.docs.analysis.about",
          :breaks="false"
        )
    v-tab Results
    v-tab-item
      v-row
        v-col(cols="5")
          v-card
            v-card-title
              span Network diagram
              v-spacer
              v-btn(
                small,
                tile,
                color="secondary",
                dark,
                @click="toggleFullscreen('#vis-network-plot')"
              ) Fullscreen
            network#vis-network-plot.vis-network-plot(
              v-if="plotData",
              :nodes="plotData.nodes",
              :edges="plotData.edges",
              :options="plotOptions"
            )
        v-col
          v-card(v-if="analysisData")
            v-card-title
              span Results table
              v-spacer
              v-text-field(
                v-model="search",
                append-icon="mdi-magnify",
                label="Search",
                single-line,
                hide-details
              )
              v-data-table(
                :headers="headers",
                :items="tblData",
                :search="search",
                :items-per-page="20",
                dense
              )
                template(v-slot:header.triple="{ header }")
                  tooltip(:docs="$store.state.docs.ents.validTriple") {{ header.text }}
                template(
                  v-slot:header.triple_evidence_supporting_score="{ header }"
                )
                  tooltip(
                    :docs="$store.state.docs.analysis.tripleEvidenceSupporting"
                  ) {{ header.text }}
                template(
                  v-slot:header.triple_evidence_reversal_score="{ header }"
                )
                  tooltip(
                    :docs="$store.state.docs.analysis.tripleEvidenceReversal"
                  ) {{ header.text }}
                template(
                  v-slot:header.assoc_evidence_supporting_score="{ header }"
                )
                  tooltip(
                    :docs="$store.state.docs.analysis.assocEvidenceSupporting"
                  ) {{ header.text }}
                template(
                  v-slot:header.assoc_evidence_reversal_score="{ header }"
                )
                  tooltip(
                    :docs="$store.state.docs.analysis.assocEvidenceReversal"
                  ) {{ header.text }}
                template(
                  v-slot:header.assoc_evidence_insufficient_score="{ header }"
                )
                  tooltip(
                    :docs="$store.state.docs.analysis.assocEvidenceInsufficient"
                  ) {{ header.text }}
                template(
                  v-slot:header.assoc_evidence_additional_score="{ header }"
                )
                  tooltip(
                    :docs="$store.state.docs.analysis.assocEvidenceAdditional"
                  ) {{ header.text }}
                template(v-slot:item.triple="{ item }")
                  .my-2
                    a(:href="item.url", target="_blank")
                      span {{ item.subject_term }}
                      br
                      | &nbsp; &nbsp;
                      span.font-italics {{ item.pred_term }}
                      br
                      span {{ item.object_term }}
                template(v-slot:item.doi_count="{ item }")
                  div
                    span {{ item.doi_count }}
                    literature-source(
                      :source-data="item.doi",
                      :triple="item.triple"
                    )
                template(
                  v-slot:item.triple_evidence_supporting_score="{ item }"
                )
                  span {{ item.triple_evidence_supporting_disp }}
                template(v-slot:item.triple_evidence_reversal_score="{ item }")
                  span {{ item.triple_evidence_reversal_disp }}
                template(
                  v-slot:item.assoc_evidence_supporting_score="{ item }"
                )
                  span {{ item.assoc_evidence_supporting_disp }}
                template(v-slot:item.assoc_evidence_reversal_score="{ item }")
                  span {{ item.assoc_evidence_reversal_disp }}
                template(
                  v-slot:item.assoc_evidence_insufficient_score="{ item }"
                )
                  span {{ item.assoc_evidence_insufficient_disp }}
                template(
                  v-slot:item.assoc_evidence_additional_score="{ item }"
                )
                  span {{ item.assoc_evidence_additional_disp }}
</template>

<script lang="ts">
import Vue from "vue";
import Multiselect from "vue-multiselect";
import "@/plugins/vue-multiselect.css";
import { Network } from "vue-vis-network";

import * as backendRequests from "@/funcs/backend_requests";
import * as types from "@/types/types";
import * as networkPlot from "@/funcs/network-plot-study-analysis";
import { PRED_MAPPING, PRED_GROUP } from "@/store/ents";
import LiteratureSource from "@/components/widgets/AnalysisLiteratureDialog.vue";

import { State } from "@/store";
import { mapState } from "vuex";

const VIEW_TITLE = "ASQ: analysis";

export default Vue.extend({
  name: "AnalysisView",
  components: {
    Network,
    Multiselect,
    LiteratureSource,
  },
  data() {
    return {
      resultsTab: 1,
      showDocsTooltip: true,
      baseData: null,
      tblData: null,
      search: null,
      termOptions: [],
      termSelect: [],
      plotData: null,
      edgeModeSelect: "default",
      edgeModeOptions: [
        {
          value: "default",
          text: "Use combined supporting evidence score (default)",
        },
        {
          value: "triple",
          text: "Use triple and literature supporting evidence score",
        },
        { value: "assoc", text: "Use association supporting evidence score" },
      ],
      predModeSelect: "default",
      predModeOptions: [
        { value: "default", text: "Use all predicates (default)" },
        { value: "directional", text: "Use directional predicates" },
        { value: "undirectional", text: "Use non-directional predicates" },
        { value: "CAUSES", text: "Directional: CAUSES" },
        { value: "TREATS", text: "Directional: TREATS" },
        { value: "AFFECTS", text: "Directional: AFFECTS" },
        { value: "PRODUCES", text: "Directional: PRODUCES" },
        { value: "ASSOCIATED_WITH", text: "Non-directional: ASSOCIATED_WITH" },
        { value: "COEXISTS_WITH", text: "Non-directional: COEXISTS_WITH" },
        { value: "INTERACTS_WITH", text: "Non-directional: INTERACTS_WITH" },
      ],
      //
      plotOptions: {
        nodes: {
          shape: "dot",
        },
        edges: {
          smooth: false,
        },
        physics: {
          barnesHut: {
            gravitationalConstant: -5000,
            springLength: 120,
            avoidOverlap: 0.9,
            damping: 0.5,
          },
        },
        layout: {
          randomSeed: 42,
          improvedLayout: true,
        },
      },
      headers: [
        {
          value: "triple",
          text: "Claim triple",
        },
        {
          value: "doi_count",
          text: "Number of source literature",
        },
        {
          value: "triple_evidence_supporting_score",
          text: "T&L.: Supporting",
        },
        {
          value: "triple_evidence_reversal_score",
          text: "T&L.: Reversal",
        },
        {
          value: "assoc_evidence_supporting_score",
          text: "Assoc.: Supporting",
        },
        {
          value: "assoc_evidence_reversal_score",
          text: "Assoc.: Reversal",
        },
        {
          value: "assoc_evidence_insufficient_score",
          text: "Assoc.: Insufficient",
        },
        {
          value: "assoc_evidence_additional_score",
          text: "Assoc.: Additional",
        },
      ],
    };
  },
  computed: {
    ...mapState({
      analysisData: (state: State) => state.analysisData.mainData,
    }),
    btnState(): Record<string, boolean | string> {
      const primaryNodeLimit = 5;
      const limitReached =
        this.termSelect.length > primaryNodeLimit ? true : false;
      const labelLimitReached = `Number of primary terms should not exceed ${primaryNodeLimit}`;
      const labelDefault = "Update";
      const label = limitReached ? labelLimitReached : labelDefault;
      const disabled = limitReached;
      const res = {
        disabled: disabled,
        label: label,
      };
      return res;
    },
  },
  watch: {
    analysisData(newVal) {
      if (newVal !== null) {
        this.termOptions = this._.chain(newVal)
          .map((e) => [e["subject_term"], e["object_term"]])
          .flatten()
          .uniq()
          .value();
        this.updateData();
      }
    },
  },
  mounted: async function () {
    document.title = VIEW_TITLE;
    await this.$store.dispatch("queryStage/setQueryMode", "off");
    await this.$store.dispatch("analysisData/getData");
    this.timeoutTooltip();
  },
  methods: {
    timeoutTooltip(): void {
      setTimeout(
        function () {
          if (this.showDocsTooltip) {
            this.showDocsTooltip = false;
          }
        }.bind(this),
        5000,
      );
    },
    updateData(): void {
      this.baseData = this.makeBaseData();
      this.tblData = this.formatTblData(this.baseData);
      const edgeMode = this.edgeModeSelect as networkPlot.EdgeModes;
      this.plotData = networkPlot.makePlot(
        this.baseData,
        this.termSelect,
        edgeMode,
      );
    },
    makeBaseData(): Array<Record<string, any>> {
      const baseData = this._.chain(this.analysisData)
        .filter((e) => this.termSelectP(e))
        .filter((e) => this.predModeSelectP(e))
        .value();
      return baseData;
    },
    formatTblData(
      baseData: Array<Record<string, any>>,
    ): Array<Record<string, any>> {
      const res = this._.chain(baseData)
        .map((e) => {
          const subject = e.subject_term.replace(" ", "+");
          const object = e.object_term.replace(" ", "+");
          const predicate = e.pred_term;
          const res = {
            ...e,
            triple_evidence_supporting_disp: this.fmtScore(
              e.triple_evidence_supporting_score,
              e.triple_evidence_supporting_count,
            ),
            triple_evidence_reversal_disp: this.fmtScore(
              e.triple_evidence_reversal_score,
              e.triple_evidence_reversal_count,
            ),
            assoc_evidence_supporting_disp: this.fmtScore(
              e.assoc_evidence_supporting_score,
              e.assoc_evidence_supporting_count,
            ),
            assoc_evidence_reversal_disp: this.fmtScore(
              e.assoc_evidence_reversal_score,
              e.assoc_evidence_reversal_count,
            ),
            assoc_evidence_insufficient_disp: this.fmtScore(
              e.assoc_evidence_insufficient_score,
              e.assoc_evidence_insufficient_count,
            ),
            assoc_evidence_additional_disp: this.fmtScore(
              e.assoc_evidence_additional_score,
              e.assoc_evidence_additional_count,
            ),
            url: `/triple?subject=${subject}&object=${object}&predicate=${predicate}&analysis`,
          };
          return res;
        })
        .value();
      return res;
    },
    termSelectP(e: Record<string, any>): boolean {
      if (this.termSelect.length == 0) {
        return true;
      } else {
        const res =
          this.termSelect.includes(e["subject_term"]) ||
          this.termSelect.includes(e["object_term"]);
        return res;
      }
    },
    predModeSelectP(e: Record<string, any>): boolean {
      if (this.predModeSelect == "default") {
        return true;
      } else if (this.predModeSelect == "directional") {
        return PRED_GROUP["directional"].includes(e["pred_term"]);
      } else if (this.predModeSelect == "undirectional") {
        return PRED_GROUP["undirectional"].includes(e["pred_term"]);
      } else {
        return e["pred_term"] == this.predModeSelect;
      }
    },
    fmtScore(score, count): string {
      if (score == null) {
        return "N/A";
      } else {
        return `${score.toFixed(2)} (${count})`;
      }
    },
    toggleFullscreen(elemId) {
      const elem = this.$el.querySelector(elemId);
      this.$fullscreen.toggle(elem);
    },
  },
});
</script>

<style scoped>
.vis-network-plot {
  height: 50rem;
  background-color: #ffffff;
}
</style>
