<template>
  <v-container fluid>
    <loading-screen v-if="loading" :message="message" :stage="loadingStage" />
    <v-row v-if="!loading">
      <v-col>
        <h2
          id="evidence-summary"
          ref="evidence-summary"
          v-intersect="onIntersect"
        >
          Evidence summary
        </h2>
        <p class="blockquote">
          <vue-markdown
            :source="
              $store.state.docs.general.evidenceSummary
                .split('\n')
                .splice(1)
                .join('\n')
            "
            :breaks="false"
          />
        </p>
        <v-card>
          <v-card-title>
            <h3 id="summary-data" ref="summary-data" v-intersect="onIntersect">
              Summary data
            </h3>
          </v-card-title>
          <v-card-text>
            <evidence-summary
              v-if="queryAllDone && summaryData"
              :data="summaryData"
              @regen="getData"
            />
          </v-card-text>
        </v-card>
        <v-divider class="py-3" />
        <v-card>
          <v-card-title>
            <h3
              id="ontology-mapping"
              ref="ontology-mapping"
              v-intersect="onIntersect"
            >
              Ontology entity mapping
            </h3>
            <!-- TODO need text explanations -->
          </v-card-title>
          <v-card-text>
            <div v-if="ontologyMappingData">
              <ontology-summary :ontology-mapping-data="ontologyMappingData" />
            </div>
          </v-card-text>
        </v-card>
        <v-divider class="py-3" />
        <div class="py-5" />
        <h2
          id="triple-literature-evidence"
          ref="triple-literature-evidence"
          v-intersect="onIntersect"
        >
          Knowledge triple and literature evidence
        </h2>
        <p class="blockquote">
          <vue-markdown
            :source="
              $store.state.docs.general.tripleLiteratureEvidence
                .split('\n')
                .splice(1)
                .join('\n')
            "
            :breaks="false"
          />
        </p>
        <v-card>
          <v-card-title>
            <h3 id="umls-mapping" ref="umls-mapping" v-intersect="onIntersect">
              UMLS entity mapping
            </h3>
          </v-card-title>
          <v-card-text>
            <div v-if="umlsData">
              <v-row>
                <v-col>
                  <h4>Subject mapping</h4>
                  <mapping-table :data="umlsData.subjects.detailData" />
                </v-col>
                <v-col>
                  <h4>Object mapping</h4>
                  <mapping-table :data="umlsData.objects.detailData" />
                </v-col>
              </v-row>
            </div>
          </v-card-text>
        </v-card>
        <v-divider class="py-3" />
        <div v-if="queryAllDone">
          <div
            v-for="item in tripleEvidenceTypes.map((key) => ({ key: key }))"
            :key="item.key"
          >
            <v-card>
              <v-card-title>
                <h3
                  :id="`triple-${item.key}`"
                  :ref="`triple-${item.key}`"
                  v-intersect="onIntersect"
                >
                  {{ outlineTripleItems[`triple-${item.key}`].label }}
                </h3>
              </v-card-title>
              <v-card-text>
                <triple-evidence-results
                  v-if="tripleEvidence[item.key]"
                  :docs="tripleEvidenceDocs[item.key]"
                  :triple-evidence="tripleEvidence[item.key]"
                  :literature-evidence="literatureEvidence[item.key]"
                />
              </v-card-text>
            </v-card>
          </div>
        </div>
        <div class="py-5" />
        <h2 id="assoc-evidence" ref="assoc-evidence" v-intersect="onIntersect">
          Association evidence
        </h2>
        <p class="blockquote">
          <vue-markdown
            :source="
              $store.state.docs.general.assocEvidence
                .split('\n')
                .splice(1)
                .join('\n')
            "
            :breaks="false"
          />
        </p>
        <v-card>
          <v-card-title>
            <h3
              id="trait-mapping"
              ref="trait-mapping"
              v-intersect="onIntersect"
            >
              GWAS trait entity mapping
            </h3>
          </v-card-title>
          <div v-if="traitData">
            <v-row>
              <v-col>
                <h4>Subject mapping</h4>
                <mapping-table :data="traitData.subjects.detailData" />
              </v-col>
              <v-col>
                <h4>Object mapping</h4>
                <mapping-table :data="traitData.objects.detailData" />
              </v-col>
            </v-row>
          </div>
          <v-card-text></v-card-text>
        </v-card>
        <v-divider class="py-3" />
        <div v-if="queryAllDone">
          <div
            v-for="item in assocEvidenceTypes.map((key) => ({ key: key }))"
            :key="item.key"
          >
            <v-card>
              <v-card-title>
                <h3
                  :id="`assoc-${item.key}`"
                  :ref="`assoc-${item.key}`"
                  v-intersect="onIntersect"
                >
                  {{ outlineAssocItems[`assoc-${item.key}`].label }}
                </h3>
              </v-card-title>
              <v-card-text>
                <assoc-evidence-results
                  v-if="assocEvidence[item.key]"
                  :docs="assocEvidenceDocs[item.key]"
                  :assoc-evidence="assocEvidence[item.key]"
                />
              </v-card-text>
            </v-card>
            <v-divider class="py-3" />
          </div>
        </div>
      </v-col>
      <v-col cols="2">
        <toc v-if="outline" :outline="outline" @goto="jump" />
      </v-col>
    </v-row>
    <adjust-results v-if="!loading" @regen="updateData" />
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import _ from "lodash";

import * as types from "@/types/types";
import * as processing from "@/funcs/processing";

import LoadingScreen from "@/components/widgets/LoadingScreen.vue";
import MappingTable from "@/components/widgets/EntityMappingTable.vue";
import Toc from "@/components/widgets/Toc.vue";
import {
  ASSOC_EVIDENCE_DETAILS,
  TRIPLE_EVIDENCE_DETAILS,
} from "@/resources/evidence-types";
import {
  assocEvidenceTypes as assocEvidenceTypeDocs,
  tripleLiteratureEvidenceTypes as tripleEvidenceTypeDocs,
} from "@/resources/docs/evidence-types";

import EvidenceSummary from "./Summary.vue";
import AssocEvidenceResults from "./AssocEvidence.vue";
import TripleEvidenceResults from "./TripleLiteratureEvidence.vue";
import OntologySummary from "./OntologySummary.vue";
import AdjustResults from "./AdjustResultsPostQuery.vue";

export default Vue.extend({
  name: "Evidence",
  components: {
    LoadingScreen,
    EvidenceSummary,
    Toc,
    MappingTable,
    TripleEvidenceResults,
    AssocEvidenceResults,
    OntologySummary,
    AdjustResults,
  },
  data() {
    return {
      outline: null,
      message: "" as string,
      loading: false as boolean,
      loadingStage: 0 as number,
      maxLoadingStage: 6 as number,
      summaryData: null as any,
      plotData: null as any,
    };
  },
  computed: {
    outlineTripleItems(): any {
      const res = _.chain(TRIPLE_EVIDENCE_DETAILS[this.predGroup])
        .mapValues((v, k, ...rest) => {
          const res = {
            label: `Triples & literature: ${v["label"]}`,
            shortLabel: v["label"],
            lv: 2,
          };
          return res;
        })
        .mapKeys((v, k) => `triple-${k}`)
        .value();
      return res;
    },
    outlineAssocItems(): any {
      const res = _.chain(ASSOC_EVIDENCE_DETAILS[this.predGroup])
        .mapValues((v, k, ...rest) => {
          const res = {
            label: `Associations: ${v["label"]}`,
            shortLabel: v["label"],
            lv: 2,
          };
          return res;
        })
        .mapKeys((v, k) => `assoc-${k}`)
        .value();
      return res;
    },
    predGroup(): string {
      return this.$store.getters["ents/predGroup"] as string;
    },
    tripleEvidenceTypes(): string[] {
      const res = this.$store.getters[
        "evidence/tripleEvidenceTypes"
      ] as string[];
      return res;
    },
    assocEvidenceTypes(): string[] {
      const res = this.$store.getters[
        "evidence/assocEvidenceTypes"
      ] as string[];
      return res;
    },
    queryAllDone(): boolean {
      const entsDone = this.$store.getters["ents/allDone"];
      const evidenceDone = this.$store.getters["evidence/allDone"];
      const res: boolean = entsDone && evidenceDone;
      return res;
    },
    ontologyMappingData(): null | Record<string, Array<any>> {
      const ontologyData = this.$store.getters["ents/ontologyData"];
      const subjectQueryTerm = this.$store.state.ents.claimTriple.sub_term;
      const objectQueryTerm = this.$store.state.ents.claimTriple.obj_term;
      if (ontologyData == null) {
        return null;
      } else {
        const subjectData = _.chain(ontologyData.subjects.ents)
          .map((item) => ({ ...item, ref_ent_term: subjectQueryTerm }))
          .value();
        const objectData = _.chain(ontologyData.objects.ents)
          .map((item) => ({ ...item, ref_ent_term: objectQueryTerm }))
          .value();
        const res = {
          subjects: subjectData,
          objects: objectData,
        };
        return res;
      }
    },
    umlsData(): null | Record<string, types.StorePostOntologyEnts> {
      const res = this.$store.getters["ents/umlsData"];
      return res;
    },
    traitData(): null | Record<string, types.StorePostOntologyEnts> {
      const res = this.$store.getters["ents/traitData"];
      return res;
    },
    assocEvidence(): Record<string, types.AssocEvidence> {
      return this.$store.getters["evidence/assocEvidence"];
    },
    literatureEvidence(): Record<string, types.LiteratureLiteEvidence> {
      return this.$store.getters["evidence/literatureEvidence"];
    },
    tripleEvidence(): Record<string, types.TripleEvidence> {
      return this.$store.getters["evidence/tripleEvidence"];
    },
    assocEvidenceDocs(): Record<string, string> {
      return assocEvidenceTypeDocs[this.predGroup];
    },
    tripleEvidenceDocs(): Record<string, string> {
      return tripleEvidenceTypeDocs[this.predGroup];
    },
  },
  mounted: async function (): Promise<boolean> {
    this.outline = this.makeOutline();
    await this.getData();
    return true;
  },
  methods: {
    async getData(): Promise<boolean> {
      this.loading = true;

      this.message = "Mapping ontology entities to UMLS entities";
      this.loadingStage = 10;
      await processing.getUmlsEnts();

      this.message = "Mapping ontology entities to trait entities";
      this.loadingStage = 20;
      await processing.getTraitEnts();

      this.message = "Retrieving triple evidence";
      this.loadingStage = 30;
      await processing.getTripleEvidence();

      this.message = "Retrieving literature evidence";
      this.loadingStage = 60;
      await processing.getLiteratureLiteEvidence();

      this.message = "Retrieving association evidence";
      this.loadingStage = 80;
      await processing.getAssocEvidence();

      this.message = "Finishing up";
      this.loadingStage = 90;
      this.summaryData = processing.makeParamSummary();
      this.loading = false;
      return true;
    },
    async updateData(): Promise<boolean> {
      await this.getData();
      return true;
    },
    makeOutline(): any {
      const outlineTree = {
        "evidence-summary": {
          label: "Evidence summary",
          lv: 1,
        },
        "summary-data": {
          label: "Summary data",
          lv: 2,
        },
        "ontology-mapping": {
          label: "Ontology entity mapping",
          lv: 2,
        },
        "triple-literature-evidence": {
          label: "Knowledge triple and literature evidence",
          lv: 1,
        },
        "umls-mapping": {
          label: "UMLS entity mapping",
          lv: 2,
        },
        ...this.outlineTripleItems,
        "assoc-evidence": {
          label: "Association evidence",
          lv: 1,
        },
        "trait-mapping": {
          label: "GWAS trait entity mapping",
          lv: 2,
        },
        ...this.outlineAssocItems,
      };
      const res = _.chain(outlineTree)
        .mapValues((v, k, ...rest) => ({ ref: k, ...v, focus: false }))
        .value();
      return res;
    },
    onIntersect(entries): void {
      const focus = entries[0].isIntersecting;
      const id = entries[0].target.id;
      this.outline[id].focus = focus;
    },
    jump(ref): void {
      var target = this.$refs[ref];
      // NOTE: sometimes the ref is an array, causes unknown
      if (Array.isArray(target)) {
        target = target[0];
      }
      // @ts-ignore
      this.$vuetify.goTo(target);
    },
  },
});
</script>
