import _ from "lodash";
import axios from "axios";

import store from "@/store/index";
import { web_backend_url } from "@/config";
import * as types from "@/types/types";
import { formatUrl } from "./utils";

function snackbarError(message: string | null = null): void {
  const generalWarningMessage = `
    Error occurred when requesting data.
    Please adjust your query settings.
  `;
  const warningMessage = message ? message : generalWarningMessage;
  store.commit("snackbar/showSnackbar", { text: warningMessage });
}

export async function parseClaim(
  claimText: string,
): Promise<types.ParseResults> {
  const url = `${web_backend_url}/claim_parsing/parse`;
  const payload = {
    claim_text: claimText,
  };
  const parseResults = (await axios
    .post(url, payload)
    .then((r) => {
      return r.data;
    })
    .catch((e) => {
      console.log({
        error: e,
        url: url,
        payload: payload,
      });
      snackbarError();
    })) as unknown;
  const res = parseResults as types.ParseResults;
  return res;
}

export async function requestOntologyEnts(
  entId: string,
  entTerm: string,
): Promise<types.OntologyResponse> {
  const url = `${web_backend_url}/ent_harmonization/ontology_ents`;
  const numCandidates = store.state.params.ontologyNumCandidates;
  const similarityThreshold =
    store.state.params.ontologySimilarityScoreThreshold;
  const payload = {
    ent_id: entId,
    ent_term: entTerm,
    num_ent_candidates: numCandidates,
    similarity_threshold: similarityThreshold,
  };
  const results = (await axios
    .post(url, payload)
    .then((r) => {
      return r.data;
    })
    .catch((e) => {
      console.log({
        error: e,
        url: url,
        payload: payload,
      });
      snackbarError();
    })) as unknown;
  const res = results as types.OntologyResponse;
  return res;
}

export async function requestTraitEnts(
  ontologyEnts: Array<types.BaseEnt>,
): Promise<types.PostOntologyEntResponse> {
  const url = `${web_backend_url}/ent_harmonization/trait_ents`;
  const predTerm = store.state.ents.claimTriple.pred;
  const numCandidates = store.state.params.postOntologyNumCandidates;
  const similarityScoreThreshold =
    store.state.params.postOntologySimilarityScoreThreshold;
  const payload = {
    ents: ontologyEnts,
    pred_term: predTerm,
    num_ent_candidates: numCandidates,
    similarity_threshold: similarityScoreThreshold,
  };
  const results = (await axios
    .post(url, payload)
    .then((r) => {
      return r.data;
    })
    .catch((e) => {
      console.log({
        error: e,
        url: url,
        payload: payload,
      });
      snackbarError();
    })) as unknown;
  const res = results as types.PostOntologyEntResponse;
  return res;
}

export async function requestUmlsEnts(
  queryUmlsEnt: types.BaseEnt,
  ontologyEnts: Array<types.BaseEnt>,
): Promise<types.PostOntologyEntResponse> {
  const url = `${web_backend_url}/ent_harmonization/umls_ents`;
  const numCandidates = store.state.params.postOntologyNumCandidates;
  const similarityScoreThreshold =
    store.state.params.postOntologySimilarityScoreThreshold;
  const payload = {
    query_umls_ent: queryUmlsEnt,
    ontology_ents: ontologyEnts,
    num_similarity_candidates: numCandidates,
    similarity_score_threshold: similarityScoreThreshold,
  };
  const results = (await axios
    .post(url, payload)
    .then((r) => {
      return r.data;
    })
    .catch((e) => {
      console.log({
        error: e,
        url: url,
        payload: payload,
      });
      snackbarError();
    })) as unknown;

  const res = results as types.PostOntologyEntResponse;
  return res;
}

export async function requestTripleEvidence(
  evidenceType: string,
): Promise<types.TripleEvidencePre> {
  const url = `${web_backend_url}/evidence/triples`;
  const subjectEnts = store.state.ents.umlsSubjectEnts.ents as types.BaseEnt[];
  const objectEnts = store.state.ents.umlsObjectEnts.ents as types.BaseEnt[];
  const predTerm = store.state.ents.claimTriple.pred as string;
  const payload = {
    subject_ents: subjectEnts,
    object_ents: objectEnts,
    pred_term: predTerm,
    evidence_type: evidenceType,
  };
  const results = (await axios
    .post(url, payload)
    .then((r) => {
      return r.data;
    })
    .catch((e) => {
      console.log({
        error: e,
        url: url,
        payload: payload,
      });
      snackbarError();
    })) as unknown;
  const annotatedResults = _.chain(results)
    .map((item, idx) => ({
      idx: idx,
      ...item,
      url: formatUrl(item["triple_id"], "LiteratureTriple"),
    }))
    .value();
  const res = annotatedResults as types.TripleEvidencePre;
  return res;
}

export async function requestLiteratureLiteEvidence(
  tripleEvidence: types.TripleEvidence,
): Promise<types.LiteratureLiteEvidence> {
  const url = `${web_backend_url}/evidence/literature-lite`;
  const claim_triple = store.state.ents.claimTriple;
  const triple_items = _.chain(tripleEvidence)
    .map((item) => {
      return {
        triple_id: item["triple_id"],
        triple_label: item["triple_lower"],
      };
    })
    .value();
  const payload = {
    triple_items: triple_items,
    claim_subject_term: claim_triple.sub_term,
    claim_object_term: claim_triple.obj_term,
  };
  const results = (await axios
    .post(url, payload)
    .then((r) => {
      return r.data;
    })
    .catch((e) => {
      console.log({
        error: e,
        url: url,
        payload: payload,
      });
      snackbarError();
    })) as unknown;
  const annotatedResults = results as any;
  const res = results as types.LiteratureLiteEvidence;
  annotatedResults.data = _.chain(annotatedResults.data)
    .map((item) => ({
      ...item,
      url: formatUrl(item.pubmed_id, "Literature"),
    }))
    .value();
  return res;
}

export async function requestScoredTripleEvidence(
  evidencePre: types.TripleEvidencePre,
): Promise<types.ScoredTripleEvidence> {
  const url = `${web_backend_url}/scores/triples`;
  const querySubjectTerm = store.state.ents.claimTriple.sub_term;
  const queryObjectTerm = store.state.ents.claimTriple.obj_term;
  const ontologyMapping = store.getters["ents/ontologyData"];
  const ontologySubjectMapping = ontologyMapping.subjects.ents;
  const ontologyObjectMapping = ontologyMapping.objects.ents;
  const umlsMapping = store.getters["ents/umlsData"];
  const umlsSubjectMapping = umlsMapping.subjects.detailData;
  const umlsObjectMapping = umlsMapping.objects.detailData;
  const tripleEvidence = _.chain(evidencePre)
    .map((item) => ({
      idx: item.idx,
      ent_subject_id: item["ent_subject_id"],
      ent_object_id: item["ent_object_id"],
      ent_subject_term: item["ent_subject_term"],
      ent_object_term: item["ent_object_term"],
      literature_count: item["literature_count"],
    }))
    .value();
  const payload = {
    triple_evidence: tripleEvidence,
    query_subject_term: querySubjectTerm,
    query_object_term: queryObjectTerm,
    ontology_subject_mapping: ontologySubjectMapping,
    ontology_object_mapping: ontologyObjectMapping,
    umls_subject_mapping: umlsSubjectMapping,
    umls_object_mapping: umlsObjectMapping,
  };
  const results = (await axios
    .post(url, payload)
    .then((r) => {
      return r.data;
    })
    .catch((e) => {
      console.log({
        error: e,
        url: url,
        payload: payload,
      });
      snackbarError();
    })) as unknown;
  const res = results as types.ScoredTripleEvidence;
  return res;
}

export async function requestLiteratureEvidence(
  triple: types.TripleItemRequest,
  numItems: number,
): Promise<types.LiteratureEvidence> {
  const url = `${web_backend_url}/evidence/literature`;
  const claim_triple = store.state.ents.claimTriple;
  const triple_items = [
    {
      triple_id: triple["triple_id"],
      triple_label: triple["triple_label"],
    },
  ];
  const payload = {
    triple_items: triple_items,
    num_literature_items_per_triple: numItems,
    triple_subject_term: triple.subject_term,
    triple_object_term: triple.object_term,
    claim_subject_term: claim_triple.sub_term,
    claim_object_term: claim_triple.obj_term,
  };
  const results = (await axios
    .post(url, payload)
    .then((r) => {
      return r.data;
    })
    .catch((e) => {
      console.log({
        error: e,
        url: url,
        payload: payload,
      });
      snackbarError();
    })) as unknown;
  const annotatedResults = results as any;
  annotatedResults.data = _.chain(annotatedResults.data)
    .map((item) => ({
      ...item,
      url: formatUrl(item.pubmed_id, "Literature"),
    }))
    .value();
  const res = results as types.LiteratureEvidence;
  return res;
}

export async function requestAssocEvidence(
  evidenceType: string,
): Promise<types.AssocEvidencePre> {
  const url = `${web_backend_url}/evidence/association`;
  const predTerm = store.state.ents.claimTriple.pred as string;
  const subjectEnts = _.chain(store.state.ents.traitSubjectEnts.ents)
    .map((item) => ({
      ent_id: item["ent_id"],
      ent_term: item["ent_term"],
    }))
    .value();
  const objectEnts = _.chain(store.state.ents.traitObjectEnts.ents)
    .map((item) => ({
      ent_id: item["ent_id"],
      ent_term: item["ent_term"],
    }))
    .value();
  const pvalThreshold = store.state.params.assocPvalThreshold;
  const payload = {
    subject_ents: subjectEnts,
    object_ents: objectEnts,
    pred_term: predTerm,
    pval_threshold: pvalThreshold,
    evidence_type: evidenceType,
  };
  const results = (await axios
    .post(url, payload)
    .then((r) => {
      return r.data;
    })
    .catch((e) => {
      console.log({
        error: e,
        url: url,
        payload: payload,
      });
      snackbarError();
    })) as unknown;
  const annotatedResults = results as any;
  annotatedResults.data = _.chain(annotatedResults.data)
    .map((item, idx) => ({
      idx: idx,
      ...item,
      subject_url: formatUrl(item.subject_id, "Gwas"),
      object_url: formatUrl(item.object_id, "Gwas"),
    }))
    .value();
  const res = annotatedResults as types.AssocEvidencePre;
  return res;
}

export async function requestScoredAssocEvidence(
  evidencePre: types.AssocEvidencePre,
): Promise<types.ScoredAssocEvidence> {
  const url = `${web_backend_url}/scores/assoc`;
  const querySubjectTerm = store.state.ents.claimTriple.sub_term;
  const queryObjectTerm = store.state.ents.claimTriple.obj_term;
  const ontologyMapping = store.getters["ents/ontologyData"];
  const ontologySubjectMapping = ontologyMapping.subjects.ents;
  const ontologyObjectMapping = ontologyMapping.objects.ents;
  const traitMapping = store.getters["ents/traitData"];
  const traitSubjectMapping = traitMapping.subjects.detailData;
  const traitObjectMapping = traitMapping.objects.detailData;
  const payload = {
    assoc_evidence: evidencePre.data,
    query_subject_term: querySubjectTerm,
    query_object_term: queryObjectTerm,
    ontology_subject_mapping: ontologySubjectMapping,
    ontology_object_mapping: ontologyObjectMapping,
    trait_subject_mapping: traitSubjectMapping,
    trait_object_mapping: traitObjectMapping,
  };
  const results = (await axios
    .post(url, payload)
    .then((r) => {
      return r.data;
    })
    .catch((e) => {
      console.log({
        error: e,
        url: url,
        payload: payload,
      });
      snackbarError();
    })) as unknown;
  const res = results as types.ScoredAssocEvidence;
  return res;
}

export async function requestOntologyData(
  entIds: Array<string>,
  queryTerms: Array<string>,
): Promise<types.OntologyRequestData> {
  const url = `${web_backend_url}/data/ontology`;
  const payload = {
    ent_ids: entIds,
    query_terms: queryTerms,
  };
  const results = (await axios
    .post(url, payload)
    .then((r) => {
      return r.data;
    })
    .catch((e) => {
      console.log({
        error: e,
        url: url,
        payload: payload,
      });
      snackbarError();
    })) as unknown;
  const res = results as types.OntologyRequestData;
  return res;
}

export async function requestLiteratureTermPrompt(
  q: string,
): Promise<Array<string>> {
  const url = `${web_backend_url}/data/prompt/literature-term`;
  const params = {
    q: q,
  };
  const r_data = (await axios.get(url, { params: params }).then((r) => {
    return r.data;
  })) as Array<types.BaseEnt>;
  const res = _.chain(r_data)
    .map((item) => ({ value: item["ent_term"], text: item["ent_term"] }))
    .value();
  return res;
}

export async function getAnalysisData(): Promise<types.AnalysisResultsData> {
  const url = `${web_backend_url}/data/analysis-results`;
  const r_data = (await axios
    .get(url)
    .then((r) => r.data)) as types.AnalysisResultsData;
  const res = r_data;
  return res;
}
