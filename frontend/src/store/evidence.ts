import { ActionContext } from "vuex";
import * as types from "@/types/types.ts";
import { State } from ".";

const ASSOC_EVIDENCE_TYPES = {
  undirectional: ["supporting", "contradictory_undirectional"],
  directional: [
    "supporting",
    "contradictory_directional_type1",
    "contradictory_directional_type2",
    "generic_directional",
  ],
};

const TRIPLE_EVIDENCE_TYPES = {
  undirectional: ["supporting"],
  directional: ["supporting", "contradictory"],
};

export type evidenceState = {
  tripleEvidence: {
    undirectional: {
      supporting: null | types.TripleEvidence;
    };
    directional: {
      supporting: null | types.TripleEvidence;
      contradictory: null | types.TripleEvidence;
    };
  };
  literatureEvidence: {
    undirectional: {
      supporting: null | types.LiteratureLiteEvidence;
    };
    directional: {
      supporting: null | types.LiteratureLiteEvidence;
      contradictory: null | types.LiteratureLiteEvidence;
    };
  };
  assocEvidence: {
    undirectional: {
      supporting: null | types.AssocEvidence;
      contradictory_undirectional: null | types.AssocEvidence;
    };
    directional: {
      supporting: null | types.AssocEvidence;
      contradictory_directional_type1: null | types.AssocEvidence;
      contradictory_directional_type2: null | types.AssocEvidence;
      generic_directional: null | types.AssocEvidence;
    };
  };
};

type Context = ActionContext<evidenceState, State>;

type submitDataPayload = {
  data: types.AssocEvidence | types.LiteratureEvidence | types.TripleEvidence;
  dataGroup: string; // assoc, literature, triple
  evidenceGroup: string; // directional, undirectional,
  evidenceType: string; // specific types, supporting, etc
};

type Payload = {
  data: types.AssocEvidence | types.LiteratureEvidence | types.TripleEvidence;
  predGroup: string; // directional, undirectional,
  evidenceType: string; // specific types, supporting, etc
};

export const evidence = {
  namespaced: true,
  state: (): evidenceState => ({
    tripleEvidence: {
      undirectional: {
        supporting: null,
      },
      directional: {
        supporting: null,
        contradictory: null,
      },
    },
    literatureEvidence: {
      undirectional: {
        supporting: null,
      },
      directional: {
        supporting: null,
        contradictory: null,
      },
    },
    assocEvidence: {
      undirectional: {
        supporting: null,
        contradictory_undirectional: null,
      },
      directional: {
        supporting: null,
        contradictory_directional_type1: null,
        contradictory_directional_type2: null,
        generic_directional: null,
      },
    },
  }),
  getters: {
    allDone(
      state: evidenceState,
      getters: unknown,
      rootState: unknown,
      rootGetters: unknown,
    ): boolean {
      const predGroup = rootGetters["ents/predGroup"];
      const tripleTypes = getters["tripleEvidenceTypes"];
      const assocTypes = getters["assocEvidenceTypes"];
      const tripleDone = tripleTypes
        .map((evidenceType) =>
          Boolean(state["tripleEvidence"][predGroup][evidenceType]),
        )
        .reduce((a, b) => a && b) as boolean;
      const literatureDone = tripleTypes
        .map((evidenceType) =>
          Boolean(state["literatureEvidence"][predGroup][evidenceType]),
        )
        .reduce((a, b) => a && b) as boolean;
      const assocDone = assocTypes
        .map((evidenceType) =>
          Boolean(state["assocEvidence"][predGroup][evidenceType]),
        )
        .reduce((a, b) => a && b) as boolean;
      const res = tripleDone && literatureDone && assocDone;
      return res;
    },
    tripleEvidenceTypes(
      state: evidenceState,
      getters: unknown,
      rootState: unknown,
      rootGetters: unknown,
    ): null | string[] {
      // directional, undirectional,
      const predGroup = rootGetters["ents/predGroup"];
      if (!predGroup) {
        return null;
      } else {
        const res = TRIPLE_EVIDENCE_TYPES[predGroup];
        return res;
      }
    },
    assocEvidenceTypes(
      state: evidenceState,
      getters: unknown,
      rootState: unknown,
      rootGetters: unknown,
    ): null | string[] {
      const predGroup = rootGetters["ents/predGroup"];
      if (!predGroup) {
        return null;
      } else {
        const res = ASSOC_EVIDENCE_TYPES[predGroup];
        return res;
      }
    },
    tripleEvidence(
      state: evidenceState,
      getters: unknown,
      rootState: unknown,
      rootGetters: unknown,
    ): Record<string, types.TripleEvidence> {
      const predGroup = rootGetters["ents/predGroup"];
      const res = state.tripleEvidence[predGroup];
      return res;
    },
    literatureEvidence(
      state: evidenceState,
      getters: unknown,
      rootState: unknown,
      rootGetters: unknown,
    ): Record<string, types.LiteratureEvidence> {
      const predGroup = rootGetters["ents/predGroup"];
      const res = state.literatureEvidence[predGroup];
      return res;
    },
    assocEvidence(
      state: evidenceState,
      getters: unknown,
      rootState: unknown,
      rootGetters: unknown,
    ): Record<string, types.TripleEvidence> {
      const predGroup = rootGetters["ents/predGroup"];
      const res = state.assocEvidence[predGroup];
      return res;
    },
  },
  mutations: {
    submitData(state: evidenceState, payload: submitDataPayload): void {
      const dataGroup = payload.dataGroup;
      const evidenceGroup = payload.evidenceGroup;
      const evidenceType = payload.evidenceType;
      const data = payload.data;
      state[dataGroup][evidenceGroup][evidenceType] = data;
    },
  },
  actions: {
    submitTripleData(context: Context, payload: Payload): void {
      const submitPayload = {
        data: payload.data,
        dataGroup: "tripleEvidence",
        evidenceGroup: payload.predGroup,
        evidenceType: payload.evidenceType,
      } as submitDataPayload;
      context.commit("submitData", submitPayload);
    },
    submitLiteratureData(context: Context, payload: Payload): void {
      const submitPayload = {
        data: payload.data,
        dataGroup: "literatureEvidence",
        evidenceGroup: payload.predGroup,
        evidenceType: payload.evidenceType,
      } as submitDataPayload;
      context.commit("submitData", submitPayload);
    },
    submitAssocData(context: Context, payload: Payload): void {
      const submitPayload = {
        data: payload.data,
        dataGroup: "assocEvidence",
        evidenceGroup: payload.predGroup,
        evidenceType: payload.evidenceType,
      } as submitDataPayload;
      context.commit("submitData", submitPayload);
    },
  },
};
