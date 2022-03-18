import _ from "lodash";

import * as types from "@/types/types";
import * as colors from "@/resources/colorscheme.json";
import { hexToRGB } from "@/funcs/network-plot";

const EDGE_COLOR_DEFAULT = "#BDBDBD";
const EDGE_COLOR_PRIMARY = "#E65100";
const NODE_COLOR_DEFAULT = "#757575";
const NODE_COLOR_PRIMARY = "#BF360C";

type NodeData = Record<string, any>;
type EdgeData = Record<string, any>;
export type EdgeModes = "default" | "triple" | "assoc";

function uniqSourceTarget(
  a: Record<string, any>,
  b: Record<string, any>,
): boolean {
  const res =
    a["subject_term"] == b["subject_term"] &&
    a["object_term"] == b["object_term"];
  return res;
}

function getSubjAndObj(node: Record<string, any>): Array<string> {
  const res = [node["subject_term"], node["object_term"]];
  return res;
}

function makeTermPair(e: Record<string, any>): string {
  const pair = _.sortBy([e["subject_term"], e["object_term"]]);
  const res = `${pair[0]}--${pair[1]}`;
  return res;
}

function formatNode(
  e: string,
  primaryNodes: Array<string>,
  nodeCount: Record<string, number>,
): NodeData {
  const color = primaryNodes.includes(e)
    ? NODE_COLOR_PRIMARY
    : NODE_COLOR_DEFAULT;
  const res = {
    id: e,
    label: e,
    title: `${e}`,
    value: nodeCount[e],
    color: {
      background: hexToRGB(color, 0.85),
      highlight: {
        background: hexToRGB(color, null),
      },
    },
  };
  return res;
}

function formatEdge(e: EdgeData, primaryNodes: Array<string>): EdgeData {
  const color =
    primaryNodes.includes(e["subject_term"]) ||
    primaryNodes.includes(e["object_term"])
      ? hexToRGB(EDGE_COLOR_PRIMARY, 0.8)
      : hexToRGB(EDGE_COLOR_DEFAULT, 0.8);
  const res = {
    from: e["subject_term"],
    to: e["object_term"],
    value: e["value"],
    color: {
      color: color,
    },
  };
  return res;
}

function prepDefaultInputData(baseData: Array<any>): Record<string, any> {
  const nodes = _.chain(baseData)
    .uniqWith(uniqSourceTarget)
    .map(getSubjAndObj)
    .flatten()
    .value();
  const nodeCount = _.chain(nodes).countBy().value();
  let topNodes = [];
  for (const threshold of [10, 8, 5, 3]) {
    if (topNodes.length > 3) break;
    topNodes = _.chain(nodeCount)
      .map((v, k) => ({ term: k, count: v }))
      .filter((e) => e.count > threshold && e.term !== "Disease")
      .map((e) => e.term)
      .values()
      .value();
  }
  const filterNodes = _.chain(nodeCount)
    .map((v, k) => ({ term: k, count: v }))
    .filter((e) => e.count == 1)
    .map((e) => e.term)
    .values()
    .value();
  const secondaryNodes = _.chain(baseData)
    .filter(
      (e) =>
        topNodes.includes(e["subject_term"]) ||
        topNodes.includes(e["object_term"]),
    )
    .map(getSubjAndObj)
    .flatten()
    .uniq()
    .filter((e) => !topNodes.includes(e) && nodeCount[e] > 3)
    .value();
  const validNodes = topNodes.concat(secondaryNodes);
  const inputData = _.chain(baseData)
    .filter(
      (e) =>
        (validNodes.includes(e["subject_term"]) ||
          validNodes.includes(e["object_term"])) &&
        !filterNodes.includes(e["subject_term"]) &&
        !filterNodes.includes(e["object_term"]),
    )
    .filter(
      (e) =>
        e["triple_evidence_supporting_score"] > 0 &&
        e["assoc_evidence_supporting_score"] > 0,
    )
    .value();
  const res = {
    inputData: inputData,
    primaryNodes: topNodes,
  };
  return res;
}

function prepInputDataWithPrimary(
  baseData: Array<any>,
  topNodes: Array<string>,
): Record<string, any> {
  const nodes = _.chain(baseData)
    .uniqWith(uniqSourceTarget)
    .map(getSubjAndObj)
    .flatten()
    .value();
  const nodeCount = _.chain(nodes).countBy().value();
  const secondaryNodes = _.chain(baseData)
    .filter(
      (e) =>
        topNodes.includes(e["subject_term"]) ||
        topNodes.includes(e["object_term"]),
    )
    .map(getSubjAndObj)
    .flatten()
    .uniq()
    .filter((e) => !topNodes.includes(e) && nodeCount[e] >= 2)
    .value();
  const tertiaryNodes = _.chain(baseData)
    .filter(
      (e) =>
        !topNodes.includes(e["subject_term"]) &&
        !topNodes.includes(e["object_term"]),
    )
    .filter(
      (e) =>
        secondaryNodes.includes(e["subject_term"]) &&
        secondaryNodes.includes(e["object_term"]),
    )
    .map(getSubjAndObj)
    .flatten()
    .uniq()
    .value();
  const validNodes = _.chain(topNodes)
    .concat(secondaryNodes)
    .concat(tertiaryNodes)
    .uniq()
    .value();
  const inputData = _.chain(baseData)
    .filter(
      (e) =>
        validNodes.includes(e["subject_term"]) &&
        validNodes.includes(e["object_term"]),
    )
    .value();
  const res = {
    inputData: inputData,
    primaryNodes: topNodes,
  };
  return res;
}

export function makePlot(
  baseData: Array<any>,
  primaryTerms: Array<string>,
  edgeMode: EdgeModes,
): Record<string, Array<any>> {
  const defaultInputData =
    primaryTerms.length == 0
      ? prepDefaultInputData(baseData)
      : prepInputDataWithPrimary(baseData, primaryTerms);
  const inputData = defaultInputData.inputData;
  const primaryNodes = defaultInputData.primaryNodes;
  const nodesInit = _.chain(inputData).map(getSubjAndObj).flatten().value();
  const nodeCount = _.chain(nodesInit).countBy().value();
  const nodes = _.chain(nodesInit)
    .uniq()
    .map((e) => formatNode(e, primaryNodes, nodeCount))
    .value();
  const edges = _.chain(inputData)
    .map((e) => ({ ...e, pair: makeTermPair(e) }))
    .groupBy("pair")
    .map((v, k) => {
      const assocScore = _.sumBy(v, "assoc_evidence_supporting_score");
      const tripleScore = _.sumBy(v, "triple_evidence_supporting_score");
      let value = (assocScore + tripleScore) / 2;
      if (edgeMode == "triple") {
        value = tripleScore;
      } else if (edgeMode == "assoc") {
        value = assocScore;
      }
      const res = {
        subject_term: v[0]["subject_term"],
        object_term: v[0]["object_term"],
        value: value,
      };
      return res;
    })
    .map((e) => formatEdge(e, primaryNodes))
    .value();
  const res = {
    nodes: nodes,
    edges: edges,
  };
  return res;
}
