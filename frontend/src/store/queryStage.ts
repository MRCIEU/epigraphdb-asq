import { ActionContext } from "vuex";
import { State } from ".";

export type queryStageState = {
  standardQueryMode: boolean;
  currentStage: number;
  latestStage: number;
  maxStageStandard: number;
  maxStageTriple: number;
};

type Context = ActionContext<queryStageState, State>;

export const queryStage = {
  namespaced: true,
  state: (): queryStageState => ({
    standardQueryMode: true,
    currentStage: 1,
    latestStage: 1,
    maxStageStandard: 4,
    maxStageTriple: 2,
  }),
  getters: {
    queryAllDone(state: queryStageState): boolean {
      if (state.standardQueryMode) {
        return state.latestStage == state.maxStageStandard;
      } else {
        return state.latestStage == state.maxStageTriple;
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
      } else {
        return tripleActions[idx];
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
    setNonStandardQuery(state: queryStageState): void {
      state.standardQueryMode = false;
    },
  },
  actions: {
    setNonStandardQuery(context: Context): void {
      context.commit("setNonStandardQuery");
    },
    setCurrentStage(context: Context, stage: number): void {
      context.commit("setCurrentStage", stage);
    },
    completeStage(context: Context, stage: number): void {
      context.commit("completeStage", stage);
    },
  },
};
