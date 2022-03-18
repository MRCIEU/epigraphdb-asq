import { Triple, TripleHtmlDisplay, ParseResults } from "@/types/types.ts";
import { ActionContext } from "vuex";
import { State } from ".";

export type claimDataState = {
  text: string;
  sents: Array<string>;
  claimTriples: Array<Triple>;
  htmlDisplay: Array<TripleHtmlDisplay>;
  invalidTriples: Array<Triple>;
};

type Context = ActionContext<claimDataState, State>;

export const claimData = {
  namespaced: true,
  state: (): claimDataState => ({
    text: "",
    sents: [],
    claimTriples: [],
    htmlDisplay: [],
    invalidTriples: [],
  }),
  getters: {
    claimParsed(state: claimDataState): boolean {
      if (!state.claimTriples) {
        return false;
      } else {
        return state.claimTriples.length > 0;
      }
    },
  },
  mutations: {
    updateClaimText(state: claimDataState, text: string): void {
      state.text = text;
    },
    updateParseResults(state: claimDataState, payload: ParseResults): void {
      state.claimTriples = payload.data;
      state.htmlDisplay = payload.html;
      state.invalidTriples = payload.invalid_triples;
      state.sents = payload.claim_text;
    },
  },
  actions: {
    updateClaimText(context: Context, text: string): void {
      context.commit("updateClaimText", text);
    },
    updateParseResults(context: Context, payload: ParseResults): void {
      context.commit("updateParseResults", payload);
    },
  },
};
