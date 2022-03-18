import { ActionContext } from "vuex";
import * as types from "@/types/types.ts";
import { State } from ".";
import _ from "lodash";

const ontologyEntInit: types.StoreOntologyEnts = {
  ents: null,
  candidates: null,
};

const postOntologyEntInit: types.StorePostOntologyEnts = {
  ents: null,
  detailData: null,
};

export type entsState = {
  claimTriple: null | types.Triple;
  ontologySubjectEnts: types.StoreOntologyEnts;
  ontologyObjectEnts: types.StoreOntologyEnts;
  traitSubjectEnts: types.StorePostOntologyEnts;
  traitObjectEnts: types.StorePostOntologyEnts;
  umlsSubjectEnts: types.StorePostOntologyEnts;
  umlsObjectEnts: types.StorePostOntologyEnts;
};

type Context = ActionContext<entsState, State>;

const ONTOLOGY_ENT_GROUP_MAPPING = {
  candidates: "candidates",
  ents: "ents",
};

const ONTOLOGY_ENT_TYPE_MAPPING = ["ontologyObjectEnts", "ontologySubjectEnts"];

const POST_ONTOLOGY_ENT_TYPE_MAPPING = [
  // false
  {
    trait: "traitObjectEnts",
    umls: "umlsObjectEnts",
  },
  // true
  {
    trait: "traitSubjectEnts",
    umls: "umlsSubjectEnts",
  },
];

export const PRED_MAPPING = {
  ASSOCIATED_WITH: "undirectional",
  COEXISTS_WITH: "undirectional",
  INTERACTS_WITH: "undirectional",
  CAUSES: "directional",
  TREATS: "directional",
  AFFECTS: "directional",
  PRODUCES: "directional",
};

export const PRED_GROUP = {
  directional: ["CAUSES", "TREATS", "AFFECTS", "PRODUCES"],
  undirectional: ["ASSOCIATED_WITH", "COEXISTS_WITH", "INTERACTS_WITH"],
};

export const ents = {
  namespaced: true,
  state: (): entsState => ({
    claimTriple: null,
    ontologySubjectEnts: _.cloneDeep(ontologyEntInit),
    ontologyObjectEnts: _.cloneDeep(ontologyEntInit),
    traitSubjectEnts: _.cloneDeep(postOntologyEntInit),
    traitObjectEnts: _.cloneDeep(postOntologyEntInit),
    umlsSubjectEnts: _.cloneDeep(postOntologyEntInit),
    umlsObjectEnts: _.cloneDeep(postOntologyEntInit),
  }),
  getters: {
    predGroup: (state: entsState): null | string => {
      if (!state.claimTriple) {
        return null;
      } else {
        const res = PRED_MAPPING[state.claimTriple.pred];
        return res;
      }
    },
    allDone: (state: entsState): boolean => {
      const groups = [
        "ontologySubjectEnts",
        "ontologyObjectEnts",
        "traitSubjectEnts",
        "traitObjectEnts",
        "umlsSubjectEnts",
        "umlsObjectEnts",
      ];
      const allDone = groups
        .map((group) => Boolean(state[group].ents))
        .reduce((a, b) => a && b) as boolean;
      return allDone;
    },
    ontologyCandidatesDone: (state: entsState): boolean => {
      const subjectDone =
        state.ontologySubjectEnts.candidates &&
        state.ontologySubjectEnts.candidates.length > 0;
      const objectDone =
        state.ontologyObjectEnts.candidates &&
        state.ontologyObjectEnts.candidates.length > 0;
      const res = Boolean(subjectDone && objectDone);
      return res;
    },
    ontologyEntsDone: (state: entsState): boolean => {
      const subjectDone =
        state.ontologySubjectEnts.ents &&
        state.ontologySubjectEnts.ents.length > 0;
      const objectDone =
        state.ontologyObjectEnts.ents &&
        state.ontologyObjectEnts.ents.length > 0;
      const res = Boolean(subjectDone && objectDone);
      return res;
    },
    ontologyData: (
      state: entsState,
    ): null | Record<string, types.StoreOntologyEnts> => {
      const subjects = state.ontologySubjectEnts;
      const objects = state.ontologyObjectEnts;
      const populated = Boolean(subjects.ents) && Boolean(objects.ents);
      if (!populated) {
        return null;
      } else {
        return {
          subjects: subjects,
          objects: objects,
        };
      }
    },
    traitData: (
      state: entsState,
    ): null | Record<string, types.StorePostOntologyEnts> => {
      const subjects = state.traitSubjectEnts;
      const objects = state.traitObjectEnts;
      const populated = Boolean(subjects.ents) && Boolean(objects.ents);
      if (!populated) {
        return null;
      } else {
        return {
          subjects: subjects,
          objects: objects,
        };
      }
    },
    umlsData: (
      state: entsState,
    ): null | Record<string, types.StorePostOntologyEnts> => {
      const subjects = state.umlsSubjectEnts;
      const objects = state.umlsObjectEnts;
      const populated = Boolean(subjects.ents) && Boolean(objects.ents);
      if (!populated) {
        return null;
      } else {
        return {
          subjects: subjects,
          objects: objects,
        };
      }
    },
  },
  mutations: {
    submitClaimTriple(state: entsState, triple: types.Triple): void {
      state.claimTriple = triple;
    },
    submitOntologyEnts(
      state: entsState,
      payload: types.SubmitOntologyEntsPayload,
    ): void {
      const ents = payload.ents;
      const entGroup = ONTOLOGY_ENT_GROUP_MAPPING[payload.entGroup];
      const entType = ONTOLOGY_ENT_TYPE_MAPPING[Number(payload.subject)];
      console.log(`entGroup: ${entGroup}; entType: ${entType}`);
      state[entType][entGroup] = ents;
    },
    submitPostOntologyData(
      state: entsState,
      payload: types.SubmitPostOntologyDataPayload,
    ): void {
      const ents = payload.data.ents;
      const detailData = payload.data.detail_data;
      const entType =
        POST_ONTOLOGY_ENT_TYPE_MAPPING[Number(payload.subject)][
          payload.entType
        ];
      console.log(`entType: ${entType}`);
      state[entType]["detailData"] = detailData;
      state[entType]["ents"] = ents;
    },
  },
  actions: {
    submitClaimTriple(context: Context, payload: types.Triple): void {
      context.commit("submitClaimTriple", payload);
    },
    submitOntologyEnts(
      context: Context,
      payload: types.SubmitOntologyEntsPayload,
    ): void {
      context.commit("submitOntologyEnts", payload);
    },
    submitPostOntologyData(
      context: Context,
      payload: types.SubmitPostOntologyDataPayload,
    ): void {
      context.commit("submitPostOntologyData", payload);
    },
  },
};
