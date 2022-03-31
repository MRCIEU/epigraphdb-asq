import _ from "lodash";

import { ActionContext } from "vuex";
import * as types from "@/types/types.ts";
import { State } from ".";

import * as evidence from "@/resources/docs/evidence-types";
import * as params from "@/resources/docs/params";
import * as ents from "@/resources/docs/ents";
import * as general from "@/resources/docs/docs";
import * as about from "@/resources/docs/docs-view";
import * as scores from "@/resources/docs/scores";
import {
  makeNetworkPlotDocs,
  makeOntologyPlotDocs,
} from "@/funcs/network-plot";
import * as analysis from "@/resources/docs/analysis";

export type docsState = {
  about: Record<string, string>;
  general: Record<string, string>;
  ents: Record<string, string>;
  evidence: Record<string, Record<string, Record<string, string>>>;
  params: Record<string, string>;
  scores: Record<string, string>;
  plots: Record<string, string>;
  analysis: Record<string, string>;
};

type Context = ActionContext<docsState, State>;

const networkPlotDocs = makeNetworkPlotDocs();
const ontologyPlotDocs = makeOntologyPlotDocs();

export const docs = {
  namespaced: true,
  state: (): docsState => ({
    about: _.chain(about)
      .mapValues((o) => o)
      .value(),
    general: _.chain(general)
      .mapValues((o) => o)
      .value(),
    ents: _.chain(ents)
      .mapValues((o) => o)
      .value(),
    evidence: {
      tripleLiteratureEvidenceTypes: evidence.tripleLiteratureEvidenceTypes,
      assocEvidenceTypes: evidence.assocEvidenceTypes,
    },
    params: _.chain(params)
      .mapValues((o) => o)
      .value(),
    scores: _.chain(scores)
      .mapValues((o) => o)
      .value(),
    plots: {
      networkPlot: networkPlotDocs,
      ontologyPlot: ontologyPlotDocs,
    },
    analysis: _.chain(analysis)
      .mapValues((o) => o)
      .value(),
  }),
  getters: {
    getFlattenDocs: (state: docsState): string[] => {
      const evidenceDocsFlat = _.chain([
        evidence.tripleLiteratureEvidenceTypes.directional,
        evidence.tripleLiteratureEvidenceTypes.undirectional,
        evidence.assocEvidenceTypes.undirectional,
        evidence.assocEvidenceTypes.directional,
      ])
        .map((item) => _.values(item))
        .flatten()
        .value();
      const flatDocs = _.chain([
        "about",
        "general",
        "ents",
        "params",
        "scores",
        "plots",
      ])
        .map((k) => _.chain(state[k]).values().value())
        .flatten()
        .filter((e) => typeof e == "string")
        .value();
      const otherFlatDocs = evidenceDocsFlat.concat([state.analysis.about]);
      const fullDocs = flatDocs.concat(otherFlatDocs);
      return fullDocs;
    },
  },
};
