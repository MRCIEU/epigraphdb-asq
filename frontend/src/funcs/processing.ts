import _ from "lodash";

import store from "@/store/index";
import * as types from "@/types/types";
import * as backendRequests from "@/funcs/backend_requests";
import {
  ASSOC_EVIDENCE_DETAILS,
  TRIPLE_EVIDENCE_DETAILS,
} from "@/resources/evidence-types";

export async function getOntologyEnts(triple: types.Triple): Promise<boolean> {
  const ontologySubjectResults = await backendRequests.requestOntologyEnts(
    triple.sub_id,
    triple.sub_term,
  );
  const ontologyObjectResults = await backendRequests.requestOntologyEnts(
    triple.obj_id,
    triple.obj_term,
  );
  if (
    ontologySubjectResults.candidates.length > 0 &&
    ontologyObjectResults.candidates.length > 0
  ) {
    const ontologySubjectEnts = ontologySubjectResults.ents;
    const ontologySubjectCandidates = ontologySubjectResults.candidates;
    const ontologyObjectEnts = ontologyObjectResults.ents;
    const ontologyObjectCandidates = ontologyObjectResults.candidates;
    await store.dispatch("ents/submitOntologyEnts", {
      ents: ontologySubjectCandidates,
      subject: true,
      entGroup: "candidates",
    });
    await store.dispatch("ents/submitOntologyEnts", {
      ents: ontologySubjectEnts,
      subject: true,
      entGroup: "ents",
    });
    await store.dispatch("ents/submitOntologyEnts", {
      ents: ontologyObjectCandidates,
      subject: false,
      entGroup: "candidates",
    });
    await store.dispatch("ents/submitOntologyEnts", {
      ents: ontologyObjectEnts,
      subject: false,
      entGroup: "ents",
    });
  }
  return true;
}

export async function getUmlsEnts(): Promise<boolean> {
  const tripleData = store.state.ents.claimTriple as types.Triple;
  const queryUmlsEntSubject = {
    ent_id: tripleData.sub_id,
    ent_term: tripleData.sub_term,
  } as types.BaseEnt;
  const queryUmlsEntObject = {
    ent_id: tripleData.obj_id,
    ent_term: tripleData.obj_term,
  } as types.BaseEnt;
  const ontologyEntSubjects = _.chain(store.state.ents.ontologySubjectEnts.ents)
    .map((item) => {
      return {
        ent_id: item.ent_id,
        ent_term: item.ent_term,
      };
    })
    .value() as Array<types.BaseEnt>;
  const ontologyEntObjects = _.chain(store.state.ents.ontologyObjectEnts.ents)
    .map((item) => {
      return {
        ent_id: item.ent_id,
        ent_term: item.ent_term,
      };
    })
    .value() as Array<types.BaseEnt>;
  // get umls ents
  const umlsSubjectResults = (await backendRequests.requestUmlsEnts(
    queryUmlsEntSubject,
    ontologyEntSubjects,
  )) as types.PostOntologyEntResponse;
  const umlsObjectResults = (await backendRequests.requestUmlsEnts(
    queryUmlsEntObject,
    ontologyEntObjects,
  )) as types.PostOntologyEntResponse;
  await store.dispatch("ents/submitPostOntologyData", {
    data: umlsSubjectResults,
    subject: true,
    entType: "umls",
  });
  await store.dispatch("ents/submitPostOntologyData", {
    data: umlsObjectResults,
    subject: false,
    entType: "umls",
  });
  return true;
}

export async function getTraitEnts(): Promise<boolean> {
  const ontologyEntSubjects = _.chain(store.state.ents.ontologySubjectEnts.ents)
    .map((item) => {
      return {
        ent_id: item.ent_id,
        ent_term: item.ent_term,
      };
    })
    .value() as Array<types.BaseEnt>;
  const ontologyEntObjects = _.chain(store.state.ents.ontologyObjectEnts.ents)
    .map((item) => {
      return {
        ent_id: item.ent_id,
        ent_term: item.ent_term,
      };
    })
    .value() as Array<types.BaseEnt>;
  const traitSubjectResults = (await backendRequests.requestTraitEnts(
    ontologyEntSubjects,
  )) as types.PostOntologyEntResponse;
  const traitObjectResults = (await backendRequests.requestTraitEnts(
    ontologyEntObjects,
  )) as types.PostOntologyEntResponse;
  await store.dispatch("ents/submitPostOntologyData", {
    data: traitSubjectResults,
    subject: true,
    entType: "trait",
  });
  await store.dispatch("ents/submitPostOntologyData", {
    data: traitObjectResults,
    subject: false,
    entType: "trait",
  });
  return true;
}

export async function getTripleEvidence(): Promise<boolean> {
  const evidenceTypes = store.getters[
    "evidence/tripleEvidenceTypes"
  ] as string[];
  const predGroup = store.getters["ents/predGroup"];
  const evidenceResults = await Promise.all(
    evidenceTypes.map((evidenceType) => {
      return backendRequests.requestTripleEvidence(evidenceType);
    }),
  );
  const evidenceScores = await Promise.all(
    evidenceTypes.map((evidenceType, idx) => {
      const evidencePre = evidenceResults[idx];
      if (evidencePre.length == 0) return { data: [] };
      const evidenceScored =
        backendRequests.requestScoredTripleEvidence(evidencePre);
      return evidenceScored;
    }),
  );
  const evidenceCombinedResults = evidenceTypes.map((evidenceType, idx) => {
    const evidencePre = evidenceResults[idx];
    const evidenceScored = evidenceScores[idx];
    const scoreData = _.chain(evidenceScored.data)
      .map((item) => ({ [item.idx]: item }))
      .reduce((a, b) => ({ ...a, ...b }), {})
      .value();
    const combined = _.chain(evidencePre)
      .map((item) => {
        const idx = item.idx;
        const score = {
          mapping_score: scoreData[idx].mapping_score,
          triple_score: scoreData[idx].triple_score,
          evidence_score: scoreData[idx].evidence_score,
          mapping_data: scoreData[idx].mapping_data,
        };
        const res = { ...item, ...score };
        return res;
      })
      .value();
    const res = combined;
    return res;
  });
  await evidenceTypes.map((evidenceType, idx) => {
    store.dispatch("evidence/submitTripleData", {
      data: evidenceCombinedResults[idx],
      evidenceType: evidenceType,
      predGroup: predGroup,
    });
  });
  return true;
}

export async function getLiteratureLiteEvidence(): Promise<boolean> {
  const evidenceTypes = store.getters[
    "evidence/tripleEvidenceTypes"
  ] as string[];
  const predGroup = store.getters["ents/predGroup"];
  const evidenceResults = await Promise.all(
    evidenceTypes.map((evidenceType) => {
      const tripleEvidence = store.getters["evidence/tripleEvidence"][
        evidenceType
      ] as types.TripleEvidence;
      return backendRequests.requestLiteratureLiteEvidence(tripleEvidence);
    }),
  );
  await evidenceTypes.map((evidenceType, idx) => {
    store.dispatch("evidence/submitLiteratureData", {
      data: evidenceResults[idx],
      evidenceType: evidenceType,
      predGroup: predGroup,
    });
  });
  return true;
}

export async function getAssocEvidence(): Promise<boolean> {
  const evidenceTypes = store.getters[
    "evidence/assocEvidenceTypes"
  ] as string[];
  const predGroup = store.getters["ents/predGroup"];
  const evidenceResults = await Promise.all(
    evidenceTypes.map((evidenceType) => {
      return backendRequests.requestAssocEvidence(evidenceType);
    }),
  );
  const evidenceScores = await Promise.all(
    evidenceTypes.map((evidenceType, idx) => {
      const evidencePre = evidenceResults[idx];
      // early return in case evidencePre is empty
      if (evidencePre.data.length == 0) return { data: [] };
      const evidenceScored =
        backendRequests.requestScoredAssocEvidence(evidencePre);
      return evidenceScored;
    }),
  );
  const evidenceCombinedResults = evidenceTypes.map((evidenceType, idx) => {
    const evidencePre = evidenceResults[idx];
    const evidenceScored = evidenceScores[idx];
    const scoreData = _.chain(evidenceScored.data)
      .map((item) => ({ [item.idx]: item }))
      .reduce((a, b) => ({ ...a, ...b }), {})
      .value();
    const combined = _.chain(evidencePre.data)
      .map((item) => {
        const idx = item.idx;
        const res = { ...item, ...scoreData[idx] };
        return res;
      })
      .value();
    const res = { data: combined };
    return res;
  });
  await evidenceTypes.map((evidenceType, idx) => {
    store.dispatch("evidence/submitAssocData", {
      data: evidenceCombinedResults[idx],
      evidenceType: evidenceType,
      predGroup: predGroup,
    });
  });
  return true;
}

export function makeParamSummary(): any {
  // query
  const queryTriple = {
    "Subject term": {
      "UMLS id": store.state.ents.claimTriple.sub_id,
      "UMLS term": store.state.ents.claimTriple.sub_term,
    },
    "Predicate term": {
      "Predicate type": store.state.ents.claimTriple.pred_type,
      "Predicate term": store.state.ents.claimTriple.pred,
    },
    "Object term": {
      "UMLS id": store.state.ents.claimTriple.obj_id,
      "UMLS term": store.state.ents.claimTriple.obj_term,
    },
  };
  // params
  const params = {
    "Query harmonization stage": {
      "Number of entity candidates": store.state.params.ontologyNumCandidates,
      "Semantic similarity threshold":
        store.state.params.ontologySimilarityScoreThreshold,
      "Information content score": store.state.params.ontologyIcScoreThreshold,
      "Identity score": store.state.params.ontologyIdentityScoreThreshold,
    },
    "Evidence retrieval stage": {
      "Number of entity candidates":
        store.state.params.postOntologyNumCandidates,
      "Semantic similarity threshold":
        store.state.params.postOntologySimilarityScoreThreshold,
      "Association evidence: P-Value threshold":
        store.state.params.assocPvalThreshold,
    },
  };
  // mapping
  const ontologyMapping = {
    subjects: {
      "Number of candidates":
        store.state.ents.ontologySubjectEnts.candidates.length,
      "Number of entities": store.state.ents.ontologySubjectEnts.ents.length,
    },
    objects: {
      "Number of candidates":
        store.state.ents.ontologyObjectEnts.candidates.length,
      "Number of entities": store.state.ents.ontologyObjectEnts.ents.length,
    },
  };
  const umlsMapping = {
    subjects: {
      "Number of entities": store.state.ents.umlsSubjectEnts.ents.length,
    },
    objects: {
      "Number of entities": store.state.ents.umlsObjectEnts.ents.length,
    },
  };
  const traitMapping = {
    subjects: {
      "Number of entities": store.state.ents.traitSubjectEnts.ents.length,
    },
    objects: {
      "Number of entities": store.state.ents.traitObjectEnts.ents.length,
    },
  };
  const mapping = {
    "Mapping query to ontology entities": ontologyMapping,
    "Mapping ontology entities to UMLS entities": umlsMapping,
    "Mapping ontology entities to GWAS trait entites": traitMapping,
  };
  // evidence
  const predGroup = store.getters["ents/predGroup"];
  const tripleTypes = store.getters["evidence/tripleEvidenceTypes"];
  const assocTypes = store.getters["evidence/assocEvidenceTypes"];
  const tripleEvidence = store.getters["evidence/tripleEvidence"];
  const literatureEvidence = store.getters["evidence/literatureEvidence"];
  const assocEvidence = store.getters["evidence/assocEvidence"];
  const tripleEvidenceSummary = _.chain(tripleTypes)
    .map((evidenceType) => {
      const numTripleItems = tripleEvidence[evidenceType].length;
      const numLiteratureItems = literatureEvidence[evidenceType].data.length;
      const label = TRIPLE_EVIDENCE_DETAILS[predGroup][evidenceType].label;
      const res = {
        "Evidence type": label,
        "Triple evidence: number of evidence items": numTripleItems,
        "Literature evidence: number of evidence items": numLiteratureItems,
      };
      return res;
    })
    .value();
  const assocEvidenceSummary = _.chain(assocTypes)
    .map((evidenceType) => {
      const numAssocItems = assocEvidence[evidenceType].data.length;
      const label = ASSOC_EVIDENCE_DETAILS[predGroup][evidenceType].label;
      const res = {
        "Evidence type": label,
        "Association evidence: number of evidence items": numAssocItems,
      };
      return res;
    })
    .value();
  const evidence = {
    "Triple and literature evidence": tripleEvidenceSummary,
    "Association evidence": assocEvidenceSummary,
  };
  // res
  const res = {
    "Query triple": queryTriple,
    "Parameter settings": params,
    "Entity mapping": mapping,
    "Retrieved evidence": evidence,
  };
  return res;
}

export async function makeOntologyPlotData(
  ontologyEnts: Array<types.BaseEnt>,
  queryTerms: Array<string>,
): Promise<types.OntologyPlotData> {
  const entIds = _.chain(ontologyEnts)
    .mapValues((item) => item.ent_id)
    .values()
    .value();
  const ontologyData = await backendRequests.requestOntologyData(
    entIds,
    queryTerms,
  );
  const res = _.chain(ontologyData)
    .map((item) => ({ [item.ent_id]: item }))
    .reduce((prev, item) => ({ ...prev, ...item }), {})
    .value();
  return res;
}
