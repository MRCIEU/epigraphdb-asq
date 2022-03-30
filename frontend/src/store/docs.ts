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

const aboutDocs = _.chain(about)
  .mapValues((o) => o)
  .value();
const generalDocs = _.chain(general)
  .mapValues((o) => o)
  .value();
const entsDocs = _.chain(ents)
  .mapValues((o) => o)
  .value();
const paramsDocs = _.chain(params)
  .mapValues((o) => o)
  .value();
const analysisDocs = _.chain(analysis)
  .mapValues((o) => o)
  .value();
const scoresDocs = _.chain(scores)
  .mapValues((o) => o)
  .value();
const evidenceDocs = {
  tripleLiteratureEvidenceTypes: evidence.tripleLiteratureEvidenceTypes,
  assocEvidenceTypes: evidence.assocEvidenceTypes,
};
const evidenceDocsFlat = _.chain([
  evidence.tripleLiteratureEvidenceTypes.directional,
  evidence.tripleLiteratureEvidenceTypes.undirectional,
  evidence.assocEvidenceTypes.undirectional,
  evidence.assocEvidenceTypes.directional,
])
  .map((item) => _.values(item))
  .flatten()
  .value();
const networkPlotDocs = makeNetworkPlotDocs();
const ontologyPlotDocs = makeOntologyPlotDocs();
const plotsDocs = {
  networkPlot: networkPlotDocs,
  ontologyPlot: ontologyPlotDocs,
};

export const docs = {
  namespaced: true,
  state: (): docsState => ({
    about: aboutDocs,
    general: generalDocs,
    ents: entsDocs,
    evidence: evidenceDocs,
    params: paramsDocs,
    scores: scores,
    plots: plotsDocs,
    analysis: analysisDocs,
  }),
  getters: {
    getFlattenDocs: (state: docsState): string[] => {
      return makeDocs();
    },
  },
};

function makeDocs(): string[] {
  const plotsDocsFlat = _.chain(plotsDocs).values().value();
  const docGroups = [
    aboutDocs,
    plotsDocsFlat,
    generalDocs,
    entsDocs,
    paramsDocs,
    evidenceDocsFlat,
    scoresDocs,
  ];
  const fullDocs = _.chain(docGroups)
    .flatten()
    .filter((e) => typeof e == "string")
    .value();
  return fullDocs;
}
