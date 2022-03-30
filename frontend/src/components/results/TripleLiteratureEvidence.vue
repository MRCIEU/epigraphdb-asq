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
          <span>Aggregated triple strength score: &nbsp;</span>
          {{ stat.aggTripleStrengthScore }}
          <span>&nbsp; &nbsp; &nbsp; &nbsp;</span>
          <span>Average score: &nbsp;</span>
          <b>{{ stat.avgTripleStrengthScore }}</b>
          <br />
          <span>Aggregated evidence score: &nbsp;</span>
          {{ stat.aggEvidenceScore }}
          <span>&nbsp; &nbsp; &nbsp; &nbsp;</span>
          <span>Average score: &nbsp;</span>
          <b>{{ stat.avgEvidenceScore }}</b>
        </p>
        <div v-if="histogramSeries">
          <triple-summary-chart
            :triple-scores="histogramSeries.tripleScores"
            :evidence-scores="histogramSeries.evidenceScores"
          />
        </div>
      </v-col>
    </v-row>
    <h4>Triple evidence</h4>
    <v-data-table
      :headers="tripleHeaders"
      :items="tripleItems"
      show-expand
      item-key="idx"
    >
      <template v-slot:header.mapping_score="{ header }">
        <tooltip :docs="$store.state.docs.scores.mappingScore">
          {{ header.text }}
        </tooltip>
      </template>
      <template v-slot:header.triple_score="{ header }">
        <tooltip :docs="$store.state.docs.scores.tripleScore">
          {{ header.text }}
        </tooltip>
      </template>
      <template v-slot:header.evidence_score="{ header }">
        <tooltip :docs="$store.state.docs.scores.evidenceScore">
          {{ header.text }}
        </tooltip>
      </template>
      <template v-slot:item.triple_lower="{ item }">
        <div>
          <a :href="item.url" target="_blank">
            <span class="font-weight-bold">{{ item["triple_label"] }}</span>
          </a>
        </div>
      </template>
      <template v-slot:item.triple_subject="{ item }">
        <div>
          <span class="font-weight-thin">LiteratureTerm:</span>
          &nbsp;
          <span>
            <code>{{ item["triple_subject_id"] }}</code>
          </span>
          <br />
          <span>{{ item.triple_subject }}</span>
        </div>
      </template>
      <template v-slot:item.triple_object="{ item }">
        <div>
          <span class="font-weight-thin">LiteratureTerm:</span>
          &nbsp;
          <span>
            <code>{{ item["triple_object_id"] }}</code>
          </span>
          <br />
          <span>{{ item.triple_object }}</span>
        </div>
      </template>
      <template v-slot:item.literature_count="{ item }">
        <div>
          {{ item.literature_count }}
          <br />
          <literature-dialog
            :item="item"
            :triple="triplesForLiterature[item.idx]"
          />
        </div>
      </template>
      <template v-slot:item.mapping_score="{ item }">
        <div>
          {{ item.mapping_score.toFixed(4) }}
        </div>
      </template>
      <template v-slot:item.triple_score="{ item }">
        <div>
          {{ item.triple_score.toFixed(4) }}
        </div>
      </template>
      <template v-slot:item.evidence_score="{ item }">
        <div>
          {{ item.evidence_score.toFixed(4) }}
        </div>
      </template>
      <template v-slot:item.link="{ item }">
        <div>
          <span>
            <v-icon>mdi-open-in-new</v-icon>
            <a :href="item.url" target="_blank">EpiGraphDB entity view</a>
          </span>
          <br />
          <span>
            <v-icon>mdi-open-in-new</v-icon>
            <a :href="item.link" target="_blank">Evidence triple view</a>
          </span>
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
          </div>
        </td>
      </template>
    </v-data-table>
  </div>
</template>

<script lang="ts">
import Vue from "vue";

import LiteratureDialog from "@/components/widgets/LiteratureDialog.vue";
import TripleSummaryChart from "./TripleSummaryChart.vue";

export default Vue.extend({
  name: "TripleLiteratureEvidenceResults",
  components: {
    LiteratureDialog,
    TripleSummaryChart,
  },
  props: {
    docs: {
      type: String,
      default: "",
    },
    tripleEvidence: {
      type: Array,
      required: true,
    },
    literatureEvidence: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      tripleHeaders: [
        {
          text: "#",
          value: "idx",
        },
        {
          text: "Triple",
          value: "triple_lower",
        },
        {
          text: "Subject term",
          value: "triple_subject",
        },
        {
          text: "Object term",
          value: "triple_object",
        },
        {
          text: "Direction",
          value: "direction",
        },
        {
          text: "Number of associated literature",
          value: "literature_count",
        },
        {
          text: "Mapping score",
          value: "mapping_score",
        },
        {
          text: "Triple strength score",
          value: "triple_score",
        },
        {
          text: "Evidence score",
          value: "evidence_score",
        },
        {
          text: "Links",
          value: "link",
        },
        {
          text: "Detail data",
          value: "data-table-expand",
        },
      ],
      showLiteratureDialog: false,
      tripleSelect: null,
      tripleToRender: null,
      numLiteratureItemsSelect: 10,
      numLiteratureItemsOptions: [10, 20, 50],
    };
  },
  computed: {
    stat(): Record<string, number | string> {
      const evidenceEmpty =
        this.tripleItems == null || this.tripleItems.length == 0;
      const numEvidenceItems = evidenceEmpty ? 0 : this.tripleItems.length;
      const aggEntHarmonizationScore = evidenceEmpty
        ? "NA"
        : this._.chain(this.tripleItems)
            .map((item) => item.mapping_score)
            .sum()
            .value()
            .toFixed(4);
      const aggTripleStrengthScore = evidenceEmpty
        ? "NA"
        : this._.chain(this.tripleItems)
            .map((item) => item.triple_score)
            .sum()
            .value()
            .toFixed(4);
      const avgTripleStrengthScore = evidenceEmpty
        ? "NA"
        : (aggTripleStrengthScore / numEvidenceItems).toFixed(4);
      const aggEvidenceScore = evidenceEmpty
        ? "NA"
        : this._.chain(this.tripleItems)
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
        aggTripleStrengthScore: aggTripleStrengthScore,
        avgTripleStrengthScore: avgTripleStrengthScore,
        aggEvidenceScore: aggEvidenceScore,
        avgEvidenceScore: avgEvidenceScore,
      };
      return res;
    },
    tripleItems(): Array<any> {
      const res = this._.chain(this.tripleEvidence)
        .map((item) => {
          const subj = item.triple_subject.replace(" ", "+");
          const obj = item.triple_object.replace(" ", "+");
          const pred = item.triple_predicate;
          const link = `triple?subject=${subj}&object=${obj}&predicate=${pred}`;
          const res = {
            ...item,
            link: link,
          };
          return res;
        })
        .value();
      return res;
    },
    tripleOptions(): Array<any> {
      const res = this._.chain(this.tripleEvidence)
        .map((item) => ({
          triple_id: item.triple_id,
          triple_label: item.triple_label,
          idx: item.idx,
        }))
        .value();
      return res;
    },
    histogramSeries(): Record<string, number> {
      const tripleScores = this._.chain(this.tripleItems)
        .map((e) => e.triple_score)
        .value();
      const evidenceScores = this._.chain(this.tripleItems)
        .map((e) => e.evidence_score)
        .value();
      const res = {
        tripleScores: tripleScores,
        evidenceScores: evidenceScores,
      };
      return res;
    },
    triplesForLiterature(): Array<Record<string, string>> {
      const items = this._.chain(this.tripleEvidence)
        .map((item) => ({
          triple_id: item.triple_id,
          triple_label: item.triple_lower,
          subject_term: item.triple_subject,
          object_term: item.triple_object,
        }))
        .value();
      return items;
    },
  },
  methods: {
    toggleFullscreen(elemId) {
      const elem = this.$el.querySelector(elemId);
      this.$fullscreen.toggle(elem);
    },
  },
});
</script>
