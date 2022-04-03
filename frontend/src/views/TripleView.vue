<template>
  <v-container>
    <v-row justify="center">
      <v-expansion-panels v-model="panels" flat multiple>
        <!-- query -->
        <v-expansion-panel>
          <v-expansion-panel-header>
            <h1>{{ queryHeader }}</h1>
          </v-expansion-panel-header>
          <v-expansion-panel-content>
            <v-row>
              <v-switch
                v-model="useAc"
                label="Enable autocompletion from EpiGraphDB literature-triples"
              />
            </v-row>
            <v-row>
              <v-col>
                <div v-if="useAc">
                  <v-autocomplete
                    v-model="tripleSubjectTerm"
                    :items="promptSubjectItems"
                    :loading="isPromptSubjectLoading"
                    :search-input.sync="promptSubjectSearch"
                    hide-no-data
                    hide-selected
                    label="Subject term"
                    placeholder="Type to search EpiGraphDB entities"
                  />
                </div>
                <div v-else>
                  <v-text-field
                    v-model="tripleSubjectTerm"
                    label="Subject term"
                  />
                </div>
              </v-col>
              <v-col>
                <v-select
                  v-model="triplePredTerm"
                  :items="predicateOptions"
                  label="Predicate"
                />
              </v-col>
              <v-col>
                <div v-if="useAc">
                  <v-autocomplete
                    v-model="tripleObjectTerm"
                    :items="promptObjectItems"
                    :loading="isPromptObjectLoading"
                    :search-input.sync="promptObjectSearch"
                    hide-no-data
                    hide-selected
                    label="Object term"
                    placeholder="Type to search EpiGraphDB entities"
                  />
                </div>
                <div v-else>
                  <v-text-field
                    v-model="tripleObjectTerm"
                    label="Object term"
                  />
                </div>
              </v-col>
              <v-col>
                <v-btn
                  color="primary"
                  :disabled="btnState.disabled"
                  @click="update"
                >
                  {{ btnState.label }}
                </v-btn>
              </v-col>
            </v-row>
            <adjust-results />
            <loading v-if="loading" :message="loadingMessage" />
          </v-expansion-panel-content>
        </v-expansion-panel>
        <!-- query -->
        <!-- results -->
        <v-expansion-panel :disabled="resultPanelDisabled">
          <v-expansion-panel-header>
            <h1>{{ resultsHeader }}</h1>
          </v-expansion-panel-header>
          <v-expansion-panel-content>
            <v-lazy v-model="queryAllDone">
              <evidence :key="refresh" />
            </v-lazy>
          </v-expansion-panel-content>
        </v-expansion-panel>
        <!-- results -->
      </v-expansion-panels>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import _ from "lodash";

import * as backendRequests from "@/funcs/backend_requests";
import * as processing from "@/funcs/processing";
import * as types from "@/types/types.ts";
import { analysisParams } from "@/store/params";
import Evidence from "@/components/results/Evidence.vue";
import Loading from "@/components/widgets/Loading.vue";
import { PRED_MAPPING } from "@/store/ents";

import AdjustResults from "@/components/results/AdjustResultsPreQuery.vue";

type BtnState = {
  label: string;
  disabled: boolean;
};

const VIEW_TITLE = "ASQ: triple query";

export default Vue.extend({
  name: "TripleView",
  components: {
    Evidence,
    Loading,
    AdjustResults,
  },
  data() {
    return {
      panels: [0],
      loading: false,
      loadingMessage: null,
      resultPanelDisabled: true,
      refresh: 0,
      predicateOptions: _.chain(PRED_MAPPING)
        .map((v, k) => k)
        .value(),
      queryTriple: null,
      tripleObjectTerm: null,
      tripleSubjectTerm: null,
      triplePredTerm: null,
      ontologyEntSubject: null,
      ontologyEntObject: null,
      useAnalysisParams: false,
      analysisParams: analysisParams,
      // ac
      useAc: false,
      isPromptSubjectLoading: false,
      isPromptObjectLoading: false,
      promptSubjectItems: [],
      promptSubjectSearch: null,
      promptObjectItems: [],
      promptObjectSearch: null,
    };
  },
  computed: {
    predicateValid(): boolean {
      return this.predicateOptions.includes(this.triplePredTerm);
    },
    tripleValid(): boolean {
      const valid =
        this.tripleSubjectTerm && this.tripleObjectTerm && this.triplePredTerm;
      return valid;
    },
    btnState(): BtnState {
      var label = "Generate evidence";
      var disabled = false;
      if (this.loading) {
        disabled = true;
        label = "Loading";
      } else if (!this.tripleValid) {
        disabled = true;
        label = "Need meaningful triple elements";
      } else if (!this.predicateValid) {
        disabled = true;
        label = "Predicate term not supported";
      }
      const res = {
        label: label,
        disabled: disabled,
      };
      return res;
    },
    queryAllDone(): boolean {
      const res = this.$store.getters["queryStage/queryAllDone"];
      return res;
    },
    queryHeader(): string {
      if (this.queryAllDone) {
        return "Triple query (complete)";
      } else {
        return "Triple query";
      }
    },
    resultsHeader(): string {
      if (this.queryAllDone) {
        return "Evidence results";
      } else {
        return "";
      }
    },
  },
  watch: {
    queryAllDone(newVal) {
      if (newVal) {
        this.panels = [1];
        this.resultPanelDisabled = false;
      }
    },
    async promptSubjectSearch(val): Promise<void> {
      if (!val) return;
      if (val.length < 3) return;
      if (this.isPromptSubjectLoading) return;
      this.isPromptSubjectLoading = true;
      this.promptSubjectItems =
        await backendRequests.requestLiteratureTermPrompt(val);
      this.isPromptSubjectLoading = false;
    },
    async promptObjectSearch(val): Promise<void> {
      if (!val) return;
      if (val.length < 3) return;
      if (this.isPromptObjectLoading) return;
      this.isPromptObjectLoading = true;
      this.promptObjectItems =
        await backendRequests.requestLiteratureTermPrompt(val);
      this.isPromptObjectLoading = false;
    },
  },
  mounted: async function (): Promise<boolean> {
    document.title = VIEW_TITLE;
    await this.$store.dispatch("queryStage/setQueryMode", "triple");
    await this.configParams();
    if (this.tripleValid) {
      const allGood = await this.getData();
      if (allGood) {
        this.updatePageTitle();
        await this.$store.dispatch("queryStage/completeStage", 1);
      }
    }
    return true;
  },
  methods: {
    async update(): Promise<boolean> {
      const nonAnalysisParams = {
        subject: this.tripleSubjectTerm,
        predicate: this.triplePredTerm,
        object: this.tripleObjectTerm,
      };
      const analysisParams = {
        subject: this.tripleSubjectTerm,
        predicate: this.triplePredTerm,
        object: this.tripleObjectTerm,
        analysis: null,
      };
      const queryParams =
        this.$route.query["analysis"] !== undefined
          ? analysisParams
          : nonAnalysisParams;
      this.$router.push({
        name: "TripleView",
        query: queryParams,
      });
      await this.configParams();
      const allGood = await this.getData();
      if (allGood) {
        await this.$store.dispatch("queryStage/completeStage", 1);
        this.updatePageTitle();
        this.refresh = this.refresh + 1;
      }
      return true;
    },
    async configParams(): Promise<boolean> {
      // config params
      this.tripleSubjectTerm = this.$route.query["subject"]
        ? this.$route.query["subject"]
        : null;
      this.tripleObjectTerm = this.$route.query["object"]
        ? this.$route.query["object"]
        : null;
      this.promptSubjectSearch = this.tripleSubjectTerm;
      this.promptObjectSearch = this.tripleObjectTerm;
      this.triplePredTerm = this.$route.query["predicate"]
        ? this.$route.query["predicate"]
        : null;
      this.useAnalysisParams =
        this.$route.query["analysis"] !== undefined ? true : false;
      // fake query ent
      this.queryTriple = this.makeQueryTriple();
      // submit data
      await this.$store.dispatch("ents/submitClaimTriple", this.queryTriple);
      if (this.useAnalysisParams) {
        _.chain(this.analysisParams)
          .forEach((value, key) => {
            if (value !== null) {
              this.$store.dispatch("params/updateParam", {
                key: key,
                value: value,
              });
            }
          })
          .value();
      }
      return true;
    },
    async getData(): Promise<boolean> {
      this.loading = true;
      this.loadingMessage = "Ontology entity harmonization";
      await this.getOntologyEnts();
      this.loading = false;
      this.loadingMessage = "";
      const subjectValid =
        this.ontologyEntSubject !== null && this.ontologyEntSubject.length > 0;
      const objectValid =
        this.ontologyEntObject !== null && this.ontologyEntObject.length > 0;
      if (subjectValid && objectValid) {
        await this.submitOntologyEnts();
        return true;
      } else {
        const message = "Empty ontology entities; please adjust your query";
        this.$store.commit("snackbar/showSnackbar", {
          text: message,
          color: "error",
        });
        return false;
      }
    },
    async getOntologyEnts(): Promise<boolean> {
      await processing.getOntologyEnts(this.queryTriple);
      const ontologyEntSubject =
        this.$store.state.ents.ontologySubjectEnts.ents;
      if (ontologyEntSubject) {
        this.ontologyEntSubject = ontologyEntSubject;
      }
      const ontologyEntObject = this.$store.state.ents.ontologyObjectEnts.ents;
      if (ontologyEntObject) {
        this.ontologyEntObject = ontologyEntObject;
      }
      return true;
    },
    async submitOntologyEnts(): Promise<boolean> {
      await this.$store.dispatch("ents/submitOntologyEnts", {
        ents: this.ontologyEntSubject,
        subject: true,
        entGroup: "ents",
      });
      await this.$store.dispatch("ents/submitOntologyEnts", {
        ents: this.ontologyEntObject,
        subject: false,
        entGroup: "ents",
      });
      return true;
    },
    updatePageTitle(): void {
      if (this.tripleValid) {
        const subj = this.tripleSubjectTerm;
        const obj = this.tripleObjectTerm;
        const pred = this.triplePredTerm;
        const title = `ASQ: ${subj} ${pred} ${obj}`;
        document.title = title;
      }
    },
    makeQueryTriple(): types.Triple {
      const queryTriple = {
        idx: 0,
        obj_confidence_score: 0,
        obj_end_pos: 0,
        obj_id: "query-triple-obj",
        obj_neg: false,
        obj_start_pos: 0,
        obj_term: this.tripleObjectTerm,
        obj_text: "",
        obj_type: "",
        pred: this.triplePredTerm,
        pred_end_pos: 0,
        pred_start_pos: 0,
        pred_type: "",
        sub_confidence_score: 0,
        sub_end_pos: 0,
        sub_id: "query-triple-subj",
        sub_neg: false,
        sub_start_pos: 0,
        sub_term: this.tripleSubjectTerm,
        sub_text: "",
      };
      return queryTriple;
    },
  },
});
</script>
