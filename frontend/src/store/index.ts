import Vue from "vue";
import Vuex from "vuex";

import { claimData, claimDataState } from "./claimData";
import { queryStage, queryStageState } from "./queryStage";
import { ents, entsState } from "./ents";
import { params, paramsState } from "./params";
import { evidence, evidenceState } from "./evidence";
import { snackbar, snackbarState } from "./snackbar";

Vue.use(Vuex);

export type State = {
  snackbar: snackbarState;
  claimData: claimDataState;
  queryStage: queryStageState;
  ents: entsState;
  params: paramsState;
  evidence: evidenceState;
};

const store = new Vuex.Store<State>({
  modules: {
    snackbar: snackbar,
    claimData: claimData,
    queryStage: queryStage,
    ents: ents,
    params: params,
    evidence: evidence,
  },
});

export default store;