import _ from "lodash";

import store from "@/store/index";

import * as types from "@/types/types";
import * as colors from "@/resources/colorscheme.json";

type Node = Record<string, any>;
type Edge = Record<string, any>;

const QUERY_BG = colors["red"]["900"];
const QUERY_FG = "white";
const EFO_BG = colors["lightgreen"]["600"];
const EFO_FG = "black";
const EFO_PARENT_BG = colors["green"]["900"];
const EFO_PARENT_FG = "#ebdbb2";
const EFO_CHILD_BG = colors["lightgreen"]["100"];
const EFO_CHILD_FG = "black";
const EFO_ANCESTOR_BG = colors["teal"]["900"];
const EFO_ANCESTOR_FG = "#ebdbb2";
const UMLS_BG = colors["lightblue"]["200"];
const UMLS_FG = "black";
const GWAS_BG = colors["blue"]["600"];
const GWAS_FG = "white";
const TRIPLE_BG = colors["lightblue"]["900"];
const TRIPLE_FG = "white";
const LITERATURE_BG = colors["pink"]["200"];
const LITERATURE_FG = "black";

export function hexToRGB(hex: string, alpha: number): string {
  const r = parseInt(hex.slice(1, 3), 16);
  const g = parseInt(hex.slice(3, 5), 16);
  const b = parseInt(hex.slice(5, 7), 16);
  if (alpha) {
    return `rgba(${r}, ${g}, ${b}, ${alpha})`;
  } else {
    return `rgb(${r}, ${g}, ${b})`;
  }
}

function formatLabel(label: string): string {
  const charLimit = 20;
  const truncated = label.substring(0, charLimit);
  const wrapLabel = _.chain(truncated.split(/(\s+)/))
    .filter((e) => /\S/.test(e))
    .map((e) => {
      const limit = 10;
      let res;
      if (e.length > limit) {
        res = e.substring(0, limit) + "...";
      } else {
        res = e;
      }
      return res;
    })
    .reduce((a, b) => a + "\n" + b)
    .value();
  const res = wrapLabel;
  return res;
}

function annotateQueryNode(node: Node): Node {
  const res = {
    ...node,
    meta_ent: "QueryUMLS",
    label: formatLabel(node.term),
    color: {
      background: hexToRGB(QUERY_BG, 0.9),
      highlight: {
        background: hexToRGB(QUERY_BG, null),
      },
    },
    font: {
      size: 36,
      color: QUERY_FG,
    },
  };
  return res;
}

function annotateQueryEdge(edge: Edge, queryPred: string): Edge {
  const res = {
    ...edge,
    arrows: { to: true },
    label: queryPred,
    value: 4,
    physics: false,
    color: {
      color: QUERY_BG,
    },
  };
  return res;
}

function annotateEfoNode(node: Node): Node {
  const res = {
    ...node,
    label: formatLabel(node.term),
    font: {
      size: 24,
      color: EFO_FG,
    },
    color: {
      background: hexToRGB(EFO_BG, 0.9),
      highlight: {
        background: hexToRGB(EFO_BG, null),
      },
    },
    meta_ent: "EpiGraphDB Efo",
  };
  return res;
}

function annotateOntologyEdge(edge: Edge): Edge {
  const res = {
    ...edge,
    value: 2,
    dashes: true,
    arrows: { to: true },
    color: {
      color: EFO_BG,
    },
  };
  return res;
}

function annotateUmlsNode(node: Node): Node {
  const res = {
    ...node,
    label: formatLabel(node.term),
    meta_ent: "EpiGraphDB LiteratureTerm (UMLS)",
    font: {
      color: UMLS_FG,
    },
    color: {
      background: hexToRGB(UMLS_BG, 0.7),
      highlight: {
        background: hexToRGB(UMLS_BG, null),
      },
    },
  };
  return res;
}

function annotateUmlsEdge(edge: Edge): Edge {
  const res = {
    ...edge,
    value: 1.5,
    dashes: true,
    arrows: { to: true },
    color: {
      color: UMLS_BG,
    },
  };
  return res;
}

function annotateTraitNode(node: Node): Node {
  const res = {
    ...node,
    label: formatLabel(node.term),
    meta_ent: "EpiGraphDB GWAS trait",
    font: {
      color: GWAS_FG,
    },
    color: {
      background: hexToRGB(GWAS_BG, 0.7),
      highlight: {
        background: hexToRGB(GWAS_BG, null),
      },
    },
  };
  return res;
}

function annotateTraitEdge(edge: Edge): Edge {
  const res = {
    ...edge,
    value: 1.5,
    dashes: true,
    arrows: { to: true },
    color: {
      color: GWAS_BG,
    },
  };
  return res;
}

function annotateTripleNode(node: Node): Node {
  const res = {
    ...node,
    label:
      formatLabel(node.subject_term) +
      "\n" +
      node.pred_term +
      "\n" +
      formatLabel(node.object_term),
    meta_ent: "EpiGraphDB LiteratureTriple",
    font: {
      size: 12,
      color: TRIPLE_FG,
    },
    color: {
      background: hexToRGB(TRIPLE_BG, 0.6),
      highlight: {
        background: hexToRGB(TRIPLE_BG, null),
      },
    },
  };
  return res;
}

function annotateTripleEdge(edge: Edge): Edge {
  const res = {
    ...edge,
    value: 1,
    color: {
      color: TRIPLE_BG,
    },
  };
  return res;
}

function annotateLiteratureNode(node: Node): Node {
  const res = {
    ...node,
    label: formatLabel(node.term),
    meta_ent: "EpiGraphDB Literature",
    font: {
      size: 9,
      color: LITERATURE_FG,
    },
    color: {
      background: hexToRGB(LITERATURE_BG, 0.6),
      highlight: {
        background: hexToRGB(LITERATURE_BG, null),
      },
    },
  };
  return res;
}

function annotateLiteratureEdge(edge: Edge): Edge {
  const res = {
    ...edge,
    value: 1,
    arrows: { to: true },
    color: {
      color: LITERATURE_BG,
    },
  };
  return res;
}

function annotateAssocEdge(edge: Edge): Edge {
  const res = {
    ...edge,
    value: 1,
    arrows: { to: true },
    color: {
      color: GWAS_BG,
    },
  };
  return res;
}

function makeNodeTitle(node: Node): Node {
  let title = `
    ${node.category}
    <br/>
    ${node.meta_ent}: <code>${node.id}</code>
    <br/>
    <b>${node.term}</b>
  `;
  if (node.url) {
    title =
      title +
      `
    <br /> <br />
    <div style="text-align:right;">
    <small>Double click on the node to redirect to source.</small></div>
    `;
  }
  const res = {
    ...node,
    title: title,
  };
  return res;
}

function makeOntologyNodeTitle(node: Node): Node {
  const title = `
    ${node.category}
    <br/>
    ${node.meta_ent}: <code>${node.id}</code>
    <br/>
    <b>${node.term}</b>
    <br /> <br />
    <div style="text-align:right;">
    Information content score: <code>${node.ic_score}</code>
    <br/>
    <small>Double click on the node to redirect to source.</small></div>
  `;
  const res = {
    ...node,
    title: title,
  };
  return res;
}

function annotateOntologyNodeSelf(node: Node): Node {
  const res = {
    ...node,
    id: node.ent_id,
    term: node.ent_term,
    url: node.ent_url,
    label: formatLabel(node.ent_term),
    font: {
      size: 24,
      color: EFO_FG,
    },
    color: {
      background: hexToRGB(EFO_BG, 0.9),
      highlight: {
        background: hexToRGB(EFO_BG, null),
      },
    },
    category: "Ontology entity",
    meta_ent: "EpiGraphDB Efo",
  };
  return res;
}

function annotateOntologyNodeParent(node: Node): Node {
  const res = {
    ...node,
    id: node.ent_id,
    term: node.ent_term,
    url: node.ent_url,
    label: formatLabel(node.ent_term),
    font: {
      size: 16,
      color: EFO_PARENT_FG,
    },
    color: {
      background: hexToRGB(EFO_PARENT_BG, 0.9),
      highlight: {
        background: hexToRGB(EFO_PARENT_BG, null),
      },
    },
    category: "Ontology parent",
    meta_ent: "EpiGraphDB Efo",
  };
  return res;
}

function annotateOntologyNodeAncestor(node: Node): Node {
  const res = {
    ...node,
    id: node.ent_id,
    term: node.ent_term,
    url: node.ent_url,
    label: formatLabel(node.ent_term),
    font: {
      size: 16,
      color: EFO_ANCESTOR_FG,
    },
    color: {
      background: hexToRGB(EFO_ANCESTOR_BG, 0.9),
      highlight: {
        background: hexToRGB(EFO_ANCESTOR_BG, null),
      },
    },
    category: "Ontology ancestor",
    meta_ent: "EpiGraphDB Efo",
  };
  return res;
}

function annotateOntologyNodeChild(node: Node): Node {
  const res = {
    ...node,
    id: node.ent_id,
    term: node.ent_term,
    url: node.ent_url,
    label: formatLabel(node.ent_term),
    font: {
      size: 16,
      color: EFO_CHILD_FG,
    },
    color: {
      background: hexToRGB(EFO_CHILD_BG, 0.9),
      highlight: {
        background: hexToRGB(EFO_CHILD_BG, null),
      },
    },
    category: "Ontology child",
    meta_ent: "EpiGraphDB Efo",
  };
  return res;
}

function annotateOntologyParentEdge(edge: Edge): Edge {
  const res = {
    ...edge,
    // value: 0.1,
    dashes: false,
    arrows: { to: true },
    color: {
      color: EFO_BG,
    },
  };
  return res;
}

function annotateOntologyAncestorEdge(edge: Edge): Edge {
  const res = {
    ...edge,
    // value: 0.1,
    dashes: false,
    arrows: { to: true },
    color: {
      color: EFO_PARENT_BG,
    },
  };
  return res;
}

function annotateOntologyChildEdge(edge: Edge): Edge {
  const res = {
    ...edge,
    // value: 0.1,
    dashes: false,
    arrows: { to: true },
    color: {
      color: EFO_CHILD_BG,
    },
  };
  return res;
}

export async function makeNetworkPlotData(
  filterEmpty: boolean,
): Promise<Record<string, Array<any>>> {
  // query ents
  const tripleData = store.state.ents.claimTriple;
  const querySubjId = `query-${tripleData.sub_id}`;
  const queryObjId = `query-${tripleData.obj_id}`;
  const queryPred = tripleData.pred;
  const queryNodes = [
    { id: querySubjId, term: tripleData.sub_term, category: "subject" },
    { id: queryObjId, term: tripleData.obj_term, category: "object" },
  ].map(annotateQueryNode);
  const queryEdges = [{ from: querySubjId, to: queryObjId }].map((edge) =>
    annotateQueryEdge(edge, queryPred),
  );
  // ontology ents
  const ontologyData = store.getters["ents/ontologyData"];
  const ontologyNodes = _.chain([
    ontologyData["subjects"].ents,
    ontologyData["objects"].ents,
  ])
    .flatten()
    .map((item) => ({
      id: item.ent_id,
      term: item.ent_term,
      url: item.url,
      category: "Harmonized ontology entity",
    }))
    .map(annotateEfoNode)
    .value();
  const ontologyEdges = _.chain([
    _.chain(ontologyData["subjects"].ents)
      .map((item) => ({ from: querySubjId, to: item.ent_id }))
      .value(),
    _.chain(ontologyData["objects"].ents)
      .map((item) => ({ from: queryObjId, to: item.ent_id }))
      .value(),
  ])
    .flatten()
    .map(annotateOntologyEdge)
    .value();
  // umls ents
  const umlsData = store.getters["ents/umlsData"];
  const umlsNodes = _.chain([
    umlsData["subjects"].detailData,
    umlsData["objects"].detailData,
  ])
    .flatten()
    .map((item) => ({
      id: item.ent_id,
      term: item.ent_term,
      url: item.ent_url,
      category: "Harmonized UMLS entity",
    }))
    .map(annotateUmlsNode)
    .value();
  const umlsEdges = _.chain([
    umlsData["subjects"].detailData,
    umlsData["objects"].detailData,
  ])
    .flatten()
    .map((item) => {
      const fromId =
        item.ref_meta_ent == "QueryUMLS" ? queryObjId : item.ref_ent_id;
      const res = {
        from: fromId,
        to: item.ent_id,
      };
      return res;
    })
    .map(annotateUmlsEdge)
    .value();
  // trait ents
  const traitData = store.getters["ents/traitData"];
  const traitNodes = _.chain([
    traitData["subjects"].detailData,
    traitData["objects"].detailData,
  ])
    .flatten()
    .map((item) => ({
      id: item.ent_id,
      term: item.ent_term,
      url: item.ent_url,
      category: "Harmonized Phenotype entity",
    }))
    .uniqWith(_.isEqual)
    .map(annotateTraitNode)
    .value();
  const traitEdges = _.chain([
    traitData["subjects"].detailData,
    traitData["objects"].detailData,
  ])
    .flatten()
    .map((item) => {
      const res = {
        from: item.ref_ent_id,
        to: item.ent_id,
      };
      return res;
    })
    .map(annotateTraitEdge)
    .value();
  // triple evidence
  const tripleEvidence = store.getters["evidence/tripleEvidence"];
  const tripleNodes = _.chain(tripleEvidence)
    .values()
    .flatten()
    .map((item) => {
      const regex = /:(.*):/gm;
      const match = regex.exec(item["triple_id"]);
      const predTerm = match[1];
      const res = {
        id: item["triple_id"],
        subject_term: item["triple_subject"],
        pred_term: predTerm,
        object_term: item["triple_object"],
        url: item["url"],
        category: "Evidence node",
      };
      return res;
    })
    .map(annotateTripleNode)
    .value();
  const tripleEdges = _.chain(tripleEvidence)
    .values()
    .flatten()
    .map((item) => {
      const res = [
        {
          from: item["triple_subject_id"],
          to: item["triple_id"],
          arrows: { to: false },
        },
        {
          from: item["triple_id"],
          to: item["triple_object_id"],
          arrows: { to: true },
        },
      ];
      return res;
    })
    .flatten()
    .map(annotateTripleEdge)
    .value();
  // literature evidence
  const literatureEvidence = store.getters["evidence/literatureEvidence"];
  const literatureNodes = _.chain(literatureEvidence)
    .mapValues((v, k, o) => v.data)
    .values()
    .flatten()
    .map((item) => {
      const res = {
        id: String(item.pubmed_id),
        term: String(item.pubmed_id),
        url: item.url,
        category: "Evidence node",
      };
      return res;
    })
    .map(annotateLiteratureNode)
    .value();
  const literatureEdges = _.chain(literatureEvidence)
    .mapValues((v, k, o) => v.data)
    .values()
    .flatten()
    .map((item) => {
      const res = {
        from: item.triple_id,
        to: item.pubmed_id,
      };
      return res;
    })
    .map(annotateLiteratureEdge)
    .value();
  // assoc evidence
  const assocEvidence = store.getters["evidence/assocEvidence"];
  const assocPval = store.getters["params/assocPval"];
  const assocEdges = _.chain(assocEvidence)
    .mapValues((v, k, o) => v.data)
    .values()
    .flatten()
    .map((item) => {
      const res = {
        from: item.subject_id,
        to: item.object_id,
        pval: item.pval,
      };
      return res;
    })
    .filter((item) => item["pval"] < assocPval)
    .map(annotateAssocEdge)
    .value();
  // finish up
  let nodesList, edgesList;
  if (filterEmpty) {
    const tripleInvolvedUmlsIds = _.chain(tripleEdges)
      .map((e) => [e.from, e.to])
      .values()
      .flatten()
      .uniq()
      .value();
    const umlsNodesFilter = _.chain(umlsNodes)
      .flatten()
      .filter((node) => tripleInvolvedUmlsIds.includes(node.id))
      .value();
    const umlsInvolvedIds = _.chain(umlsNodes)
      .map((node) => node.id)
      .values()
      .value();
    const umlsEdgesFilter = _.chain(umlsEdges)
      .flatten()
      .filter((edge) => umlsInvolvedIds.includes(edge.to))
      .value();
    const assocInvolvedTraitIds = _.chain(assocEdges)
      .map((e) => [e.from, e.to])
      .flatten()
      .uniq()
      .value();
    const traitNodesFilter = _.chain(traitNodes)
      .flatten()
      .filter((node) => assocInvolvedTraitIds.includes(node.id))
      .value();
    const traitEdgesFilter = _.chain(traitEdges)
      .flatten()
      .filter((e) => assocInvolvedTraitIds.includes(e.to))
      .value();
    nodesList = [
      queryNodes,
      ontologyNodes,
      umlsNodesFilter,
      traitNodesFilter,
      tripleNodes,
      literatureNodes,
    ];
    edgesList = [
      queryEdges,
      ontologyEdges,
      umlsEdgesFilter,
      traitEdgesFilter,
      tripleEdges,
      literatureEdges,
      assocEdges,
    ];
  } else {
    nodesList = [
      ontologyNodes,
      umlsNodes,
      traitNodes,
      tripleNodes,
      literatureNodes,
    ];
    edgesList = [
      queryEdges,
      ontologyEdges,
      umlsEdges,
      traitEdges,
      tripleEdges,
      literatureEdges,
      assocEdges,
    ];
  }
  const nodes = _.chain(nodesList)
    .flatten()
    .uniqWith(_.isEqual)
    .map(makeNodeTitle)
    .reverse()
    .value();
  const edges = _.chain(edgesList)
    .flatten()
    .uniqWith(_.isEqual)
    .reverse()
    .value();
  const res = {
    nodes: nodes,
    edges: edges,
  };
  return res;
}

export async function makeOntologyPlotData(
  ontologyData: Array<types.EfoDataItem>,
): Promise<Record<string, Array<any>>> {
  const selfNode = _.chain(ontologyData)
    .filter((item) => item.ent_type == "ontology_self")
    .map(annotateOntologyNodeSelf)
    .value();
  const parentNodes = _.chain(ontologyData)
    .filter((item) => item.ent_type == "ontology_parent")
    .map(annotateOntologyNodeParent)
    .value();
  const ancestorNodes = _.chain(ontologyData)
    .filter((item) => item.ent_type == "ontology_ancestor")
    .map(annotateOntologyNodeAncestor)
    .value();
  const childNodes = _.chain(ontologyData)
    .filter((item) => item.ent_type == "ontology_child")
    .map(annotateOntologyNodeChild)
    .value();
  const parentEdges = _.chain(ontologyData)
    .filter((item) => item.ent_type == "ontology_parent")
    .map((item) => ({
      from: item.ent_id,
      to: item.ref_ent_id,
    }))
    .map(annotateOntologyParentEdge)
    .value();
  const ancestorEdges = _.chain(ontologyData)
    .filter((item) => item.ent_type == "ontology_ancestor")
    .map((item) => ({
      from: item.ent_id,
      to: item.ref_ent_id,
    }))
    .map(annotateOntologyAncestorEdge)
    .value();
  const childEdges = _.chain(ontologyData)
    .filter((item) => item.ent_type == "ontology_child")
    .map((item) => ({
      from: item.ref_ent_id,
      to: item.ent_id,
    }))
    .map(annotateOntologyChildEdge)
    .value();
  const nodesList = [selfNode, parentNodes, ancestorNodes, childNodes];
  const edgesList = [parentEdges, ancestorEdges, childEdges];
  const res = {
    nodes: _.chain(nodesList)
      .flatten()
      .uniqWith((ent1, ent2) => ent1.ent_id == ent2.ent_id)
      .map(makeOntologyNodeTitle)
      .reverse()
      .value(),
    edges: _.chain(edgesList)
      .flatten()
      .uniqWith((ent1, ent2) => ent1.from == ent2.from && ent1.to == ent2.to)
      .reverse()
      .value(),
  };
  return res;
}

export function makeNetworkPlotDocs(): string {
  const queryEnt = `<span style="background-color:${QUERY_BG};color:${QUERY_FG}">
  &nbsp; Query entity &nbsp;</span>`;
  const ontologyEnt = `<span style="background-color:${EFO_BG};color:${EFO_FG}">
  &nbsp; Ontology entity &nbsp;</span>`;
  const umlsEnt = `<span style="background-color:${UMLS_BG};color:${UMLS_FG}">
  &nbsp; UMLS entity &nbsp;</span>`;
  const traitEnt = `<span style="background-color:${GWAS_BG};color:${GWAS_FG}">
  &nbsp; GWAS trait entity &nbsp;</span>`;
  const tripleEvidence = `<span style="background-color:${TRIPLE_BG};color:${TRIPLE_FG}">
  &nbsp; Knowledge triple evidence &nbsp;</span>`;
  const literatureEvidence = `<span style="background-color:${LITERATURE_BG};color:${LITERATURE_FG}">
  &nbsp; Literature evidence &nbsp;</span>`;
  const assocEvidence = `<span style="background-color:${GWAS_BG};color:${GWAS_FG}">
  &nbsp; association evidence &nbsp;</span>`;
  const res = `**Summary diagram** <br/>
This diagram summarises the state of entity harmonization and evidence retrieval.

*Diagram legend*:
- ${queryEnt}: The <code>subject</code> - <code>predicate</code> - <code>object</code>
  UMLS query triple that is generated from the claim text
- ${ontologyEnt}: The retrieved ontology entities which act as reference entities and
  represent the query subject / object
  entities throughout the rest of the retrieval process, which in turn are used to retrieve
  other types of entities
- ${umlsEnt}: UMLS entities that are mapped to the reference ontology entities by semantic similarity,
  or mapped to the query entities if the query entities are found in EpiGraphDB
- ${traitEnt}: GWAS trait entities that are mapped to the reference ontology entities
  by semantic similarity,
  and ${assocEvidence} will be represented as edges between a pair of trait entities
- ${tripleEvidence}: knowledge triple
  (<code>subject</code> - <code>predicate</code> - <code>object</code>) represented as a
  node, which will then in turn be used to retrieve literature evidence
- ${literatureEvidence}: a published / preprint article that is identified to support
  a knowledge triple

<br/>
For further detailed information please refer to the documentation and manuscript.
  `;
  return res;
}

export function makeOntologyPlotDocs(): string {
  const ontologyEnt = `<span style="background-color:${EFO_BG};color:${EFO_FG}">
  &nbsp; Ontology entity &nbsp;</span>`;
  const ontologyAncestor = `<span style="background-color:${EFO_ANCESTOR_BG};color:${EFO_ANCESTOR_FG}">
  &nbsp; Ancestor ontology entity &nbsp;</span>`;
  const ontologyParent = `<span style="background-color:${EFO_PARENT_BG};color:${EFO_PARENT_FG}">
  &nbsp; Parent ontology entity &nbsp;</span>`;
  const ontologyChild = `<span style="background-color:${EFO_CHILD_BG};color:${EFO_CHILD_FG}">
  &nbsp; Child ontology entity &nbsp;</span>`;

  const res = `**Ontology diagram**: <br/>
This diagram shows how the reference ontology entity is located in the Experimental Factor Ontology and the sematic specificity of the ontology term.

*Diagram legend*:
- ${ontologyEnt}: The retrieved ontology entities which act as reference entities and
  represent the query subject / object
  entities throughout the rest of the retrieval process, which in turn are used to retrieve
  other types of entities
- ${ontologyParent}: Ontology entities that are parent to the reference ontology entity in the EFO (Experimental Factor Ontology) tree
- ${ontologyAncestor}: Ontology entities that are further back to the origin of the ontology tree (to the "experimental factor" node) and thus are ancestors to the reference entity
- ${ontologyChild}: Ontology entities that are children to the reference ontology entity in the EFO (Experimental Factor Ontology) tree

<br/>
The diagram is generated by getting the direct parents and children
ontology nodes of the reference node, and then the *shortest paths*
of the parents nodes to the origin node.
Therefore the diagram is not an exhaustive representation of the graph paths
between the origin node and the reference entity node,
but a simplified representation.

<br/>
For further detailed information please refer to the documentation and manuscript.
  `;
  return res;
}
