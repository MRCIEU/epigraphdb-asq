// ---- basics ----

export type BaseEnt = {
  ent_id: string;
  ent_term: string;
};

export type OntologyEnt = {
  ent_id: string;
  ent_term: string;
  similarity_score: number;
  identity_score: number;
  ic_score: number;
  url: string | null;
};

export type PostOntologyEnt = {
  ent_id: string;
  ent_term: string;
  url: string | null;
};

export type PostOntologyEntDetailItem = {
  ent_id: string;
  ent_term: string;
  ent_url: string;
  meta_ent: string;
  meta_ent_url: string | null;
  ref_ent_id: string;
  ref_ent_term: string;
  ref_ent_url: string | null;
  ref_meta_ent: string;
  ref_meta_ent_url: string | null;
  similarity_score: number;
};

export type Triple = {
  idx: number;
  obj_confidence_score: number;
  obj_end_pos: number;
  obj_id: string;
  obj_neg: boolean;
  obj_start_pos: number;
  obj_term: string;
  obj_text: string;
  obj_type: string;
  pred: string;
  pred_end_pos: number;
  pred_start_pos: number;
  pred_type: string;
  sub_confidence_score: number;
  sub_end_pos: number;
  sub_id: string;
  sub_neg: boolean;
  sub_start_pos: number;
  sub_term: string;
  sub_text: string;
};

export type TripleHtmlDisplay = {
  idx: number;
  text: string;
};

// ---- claim ----

export type ParseResults = {
  data: Array<Triple>;
  html: Array<TripleHtmlDisplay>;
  invalid_triples: Array<Triple>;
  claim_text: Array<string>;
};

// ---- ent harmonization ---

export type OntologyResponse = {
  candidates: Array<OntologyEnt>;
  ents: Array<OntologyEnt>;
};

export type PostOntologyEntResponse = {
  ents: Array<PostOntologyEnt>;
  detail_data: Array<PostOntologyEntDetailItem>;
};

export type StoreOntologyEnts = {
  ents: null | Array<OntologyEnt>;
  candidates: null | Array<OntologyEnt>;
};

export type StorePostOntologyEnts = {
  ents: null | Array<PostOntologyEnt>;
  detailData: null | Array<PostOntologyEntDetailItem>;
};

export type SubmitOntologyEntsPayload = {
  ents: Array<OntologyEnt>;
  // subject, object
  subject: boolean;
  entGroup: "ents" | "candidates";
};

export type SubmitPostOntologyDataPayload = {
  data: PostOntologyEntResponse;
  // subject, object
  subject: boolean;
  entType: "trait" | "umls";
};

// ---- triple evidence ----

export type TripleItemRequest = {
  triple_id: string;
  triple_label: string;
  subject_term: string;
  object_term: string;
};

export type TripleEvidencePre = Array<{
  idx: number;
  triple_id: string;
  triple_label: string;
  triple_lower: string;
  triple_subject_id: string;
  triple_subject: string;
  triple_object_id: string;
  triple_object: string;
  triple_predicate: string;
  ent_subject_id: string;
  ent_object_id: string;
  ent_subject_term: string;
  ent_object_term: string;
  direction: string;
  literature_count: number;
  url: string;
}>;

export type ScoredTripleEvidence = {
  data: Array<{
    idx: number;
    ent_subject_id: string;
    ent_object_id: string;
    ent_subject_term: string;
    ent_object_term: string;
    literature_count: number;
    mapping_score: number;
    triple_score: number;
    evidence_score: number;
    mapping_data: Record<string, any>;
  }>;
};

export type TripleEvidence = Array<{
  idx: number;
  triple_id: string;
  triple_label: string;
  triple_lower: string;
  triple_subject_id: string;
  triple_subject: string;
  triple_object_id: string;
  triple_object: string;
  triple_predicate: string;
  ent_subject_id: string;
  ent_object_id: string;
  ent_subject_term: string;
  ent_object_term: string;
  direction: string;
  literature_count: number;
  url: string;
  mapping_score: number;
  triple_score: number;
  evidence_score: number;
  mapping_data: Record<string, any>;
}>;

// ---- literature evidence ----

export type LiteratureLiteEvidence = {
  data: Array<{
    pubmed_id: string;
    triple_id: string;
    triple_lower: string;
    url: string;
  }>;
};

export type LiteratureEvidence = {
  data: Array<{
    abstract: string;
    doi: string;
    pubmed_id: string;
    title: string;
    triple_id: string;
    triple_lower: string;
    type: string;
    year: number;
    url: string;
  }>;
  html_text: Array<{
    idx: number;
    title_text: string;
    abstract: string;
    sentence: string;
  }>;
};

// ---- assoc evidence ----

export type AssocEvidencePre = {
  data: Array<{
    idx: number;
    subject_id: string;
    subject_term: string;
    object_id: string;
    object_term: string;
    meta_rel: string;
    direction: string;
    effect_size: number;
    se: number;
    pval: number;
    rel_data: any;
    subject_url: string;
    object_url: string;
  }>;
};

export type ScoredAssocEvidence = {
  data: Array<{
    idx: number;
    subject_id: string;
    subject_term: string;
    object_id: string;
    object_term: string;
    effect_size: number;
    se: number;
    pval: number;
    mapping_score: number;
    assoc_score: number;
    evidence_score: number;
    mapping_data: Record<string, any>;
  }>;
};

export type AssocEvidence = {
  data: Array<{
    idx: number;
    subject_id: string;
    subject_term: string;
    object_id: string;
    object_term: string;
    meta_rel: string;
    direction: string;
    effect_size: number;
    se: number;
    pval: number;
    rel_data: any;
    subject_url: string;
    object_url: string;
    mapping_score: number;
    assoc_score: number;
    evidence_score: number;
    mapping_data: Record<string, any>;
  }>;
};

// ---- ontology data ----

export type EfoDataItem = {
  ent_id: string;
  ent_term: string;
  ent_url: string;
  ic_score: number;
  ent_type: string;
  ref_ent_id: string;
};

export type OntologyRequestData = Array<{
  ent_id: string;
  efo_data: Array<EfoDataItem>;
  query_ents: Array<BaseEnt>;
  similarity_scores: Array<{
    source_ent_id: string;
    source_ent_term: string;
    target_ent_id: string;
    target_ent_term: string;
    similarity_score: number;
  }>;
}>;

export type OntologyPlotItem = {
  efo_data: Array<EfoDataItem>;
  query_ents: Array<BaseEnt>;
  similarity_scores: Array<{
    source_ent_id: string;
    source_ent_term: string;
    target_ent_id: string;
    target_ent_term: string;
    similarity_score: number;
  }>;
};

export type OntologyPlotData = Record<string, OntologyPlotItem>;

// ---- analysis data ----

export type AnalysisResultsData = Array<{
  triple: string;
  subject_term: string;
  object_term: string;
  pred_term: string;
  directional: string;
  doi: Array<{
    doi: string;
    title: string;
    context: string;
  }>;
  doi_count: number;
  // triple
  triple_evidence_supporting_score: number | null;
  triple_evidence_supporting_count: number | null;
  triple_evidence_reversal_score: number | null;
  triple_evidence_reversal_count: number | null;
  // assoc
  assoc_evidence_supporting_score: number | null;
  assoc_evidence_supporting_count: number | null;
  assoc_evidence_reversal_score: number | null;
  assoc_evidence_reversal_count: number | null;
  assoc_evidence_insufficient_score: number | null;
  assoc_evidence_insufficient_count: number | null;
  assoc_evidence_additional_score: number | null;
  assoc_evidence_additional_count: number | null;
}>;
