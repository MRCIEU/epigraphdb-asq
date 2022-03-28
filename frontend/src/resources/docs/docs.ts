export const queryParsing = `**Insert query text**:

<span class="mark">Insert a paragraph of text</span>
that might contain some claims
of **biomedical nature**,
or <span class="mark1">use a predefined text</span>
as a demonstration.

The input text will be parsed to generate claim triples.`;

export const tripleSelect = `**Select a claim triple**:

From the parsed triples,
<span class="mark">select a claim triple</span> to focus for further analysis.
This triple is then parsed to retrieve ontology entities in EpiGraphDB.
`;

export const entHarmonizationOntology = `**Entity harmonization**:

<span class="mark">Select subject (object) ontology entities</span> that represent
the claim subject (object) entities, which will be used as
the basis of further entity harmonization and subsequent
evidence retrieval procedures.

By default, suitable candidates have been <span class="mark1">picked automatically</span>.
`;

export const evidenceSummary = `**Evidence summary**:

This section shows the following:

- Summary metrics on the entity harmonization
  and evidence retrieval results
- Overview diagram representing the involved entities
  of different types and associated evidence
- Adjust parameter settings and regenerate the retrieval results`;

export const tripleLiteratureEvidence = `**Knowledge triple and literature evidence**:

This section shows the following:

- Summary of UMLS subject/object entities that
  have been mapped from the ontology entities
- Supporting and contradictory groups of retrieved evidence.
  **NOTE**: The specific definition of a evidence group is
  contingent on type of query predicate
  (refer to the specific evidence sections).
  If the query predicate is non-directional (e.g. <code>ASSOC_WITH</code>),
  then only a supporting group is retrieved.`;

export const assocEvidence = `**Association evidence**:

This section shows the following:

- Summary of GWAS trait subject/object entities that
  have been mapped from the ontology entities
- Supporting and contradictory groups of retrieved evidence.
  **NOTE**: The specific definition of a evidence group is
  contingent on type of query predicate
  (refer to the specific evidence sections).`;
