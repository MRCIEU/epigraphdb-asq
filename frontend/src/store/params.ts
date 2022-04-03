import { State } from ".";

import { ActionContext } from "vuex";

export type paramsState = {
  claimTextMaxCharLen: number;
  ontologyNumCandidates: number;
  ontologySimilarityScoreThreshold: number;
  ontologyIdentityScoreThreshold: number;
  ontologyIcScoreThreshold: number;
  ontologyNumEnts: number;
  postOntologyNumCandidates: number;
  postOntologySimilarityScoreThreshold: number;
  assocPvalThreshold: string;
};

type Context = ActionContext<paramsState, State>;

type paramPayload = {
  key: string;
  value: string | number;
};

export const params = {
  namespaced: true,
  state: (): paramsState => ({
    claimTextMaxCharLen: 5000,
    ontologyNumCandidates: 15,
    ontologySimilarityScoreThreshold: 0.7,
    ontologyIdentityScoreThreshold: 1.5,
    ontologyIcScoreThreshold: 0.6,
    ontologyNumEnts: 5,
    postOntologyNumCandidates: 20,
    postOntologySimilarityScoreThreshold: 0.7,
    assocPvalThreshold: "1e-2",
  }),
  getters: {
    assocPval: (state: paramsState): number => {
      return parseFloat(state.assocPvalThreshold);
    },
  },
  mutations: {
    updateParam(state: paramsState, payload: paramPayload): void {
      state[payload.key] = payload.value;
    },
  },
  actions: {
    updateParam(context: Context, payload: paramPayload): void {
      context.commit("updateParam", payload);
    },
  },
};

export const analysisParams = {
  ontologyNumCandidates: 10,
  ontologySimilarityScoreThreshold: 0.7,
  ontologyIdentityScoreThreshold: 1.5,
  ontologyIcScoreThreshold: 0.6,
  postOntologyNumCandidates: 20,
  postOntologySimilarityScoreThreshold: 0.7,
  assocPvalThreshold: "1e-2",
};
