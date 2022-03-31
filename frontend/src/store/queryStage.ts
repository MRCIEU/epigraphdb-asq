import { ActionContext } from "vuex";
import { State } from ".";

export type queryStageState = {
  standardQueryMode: boolean;
  tripleQueryMode: boolean;
  currentStage: number;
  latestStage: number;
  maxStageStandard: number;
  maxStageTriple: number;
};

type Context = ActionContext<queryStageState, State>;
type QueryMode = "standard" | "triple" | "off";

export const queryStage = {
  namespaced: true,
  state: (): queryStageState => ({
    standardQueryMode: false,
    tripleQueryMode: false,
    currentStage: 1,
    latestStage: 1,
    maxStageStandard: 4,
    maxStageTriple: 2,
  }),
  getters: {
    queryAllDone(state: queryStageState): boolean {
      if (state.standardQueryMode) {
        return state.latestStage == state.maxStageStandard;
      } else if (state.tripleQueryMode) {
        return state.latestStage == state.maxStageTriple;
      } else {
        return true;
      }
    },
    stageAction(state: queryStageState): string {
      const idx = state.latestStage - 1;
      const standardActions = [
        `Query stage: insert query text.`,
        `Query stage: select a <code>claim triple</code> for further analysis.`,
        `Query stage: select <code>ontology entities</code>
that represent query subjects and objects.`,
        `Query finished. Browse evidence results.`,
      ];
      const tripleActions = [
        `Query stage: insert query triple.`,
        `Query finished. Browse evidence results.`,
      ];
      if (state.standardQueryMode) {
        return standardActions[idx];
      } else if (state.tripleQueryMode) {
        return tripleActions[idx];
      } else {
        return ``;
      }
    },
  },
  mutations: {
    setCurrentStage(state: queryStageState, stage: number): void {
      state.currentStage = stage;
    },
    completeStage(state: queryStageState, stage: number): void {
      const nextStage = stage + 1;
      state.currentStage = nextStage;
      if (state.latestStage < nextStage) {
        state.latestStage = nextStage;
      }
    },
    setQueryMode(state: queryStageState, mode: QueryMode): void {
      if (mode == "standard") {
        state.standardQueryMode = true;
        state.tripleQueryMode = false;
      } else if (mode == "triple") {
        state.standardQueryMode = false;
        state.tripleQueryMode = true;
      } else {
        state.standardQueryMode = false;
        state.tripleQueryMode = false;
      }
    },
  },
  actions: {
    setQueryMode(context: Context, mode: QueryMode): void {
      context.commit("setQueryMode", mode);
    },
    setCurrentStage(context: Context, stage: number): void {
      context.commit("setCurrentStage", stage);
    },
    completeStage(context: Context, stage: number): void {
      context.commit("completeStage", stage);
    },
  },
};
