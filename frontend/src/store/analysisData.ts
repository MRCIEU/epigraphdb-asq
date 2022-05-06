import * as backendRequests from "@/funcs/backend_requests";
import * as types from "@/types/types.ts";

import { ActionContext } from "vuex";
import { State } from ".";

export type analysisDataState = {
  mainData: types.AnalysisResultsData | null;
};

type Context = ActionContext<analysisDataState, State>;

export const analysisData = {
  namespaced: true,
  state: (): analysisDataState => ({
    mainData: null,
  }),
  getters: {
    //
  },
  mutations: {
    async getData(state: analysisDataState): Promise<void> {
      if (state.mainData === null) {
        state.mainData = await backendRequests.getAnalysisData();
      }
    },
  },
  actions: {
    async getData(context: Context): Promise<void> {
      await context.commit("getData");
    },
  },
};
