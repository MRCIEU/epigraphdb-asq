export const paramSimilarityScore = `
  **Similarity score**: <br/>
  A score (<code>[0, 1]</code>) measuring the semantic similarity
  between this entity and the target entity,
  where a higher score denotes higher degree of similarity.
  <br/> <br/>
  In ASQ we compute semantic similarity score as the cosine similarity between the text embeddings of two labels.
  <br/> <br/>
  This score is used for candidate retrieval.
  `;
export const paramIdentityScore = `
  **Identity score**: <br/>
  A score (<code>[0, Inf]</code>) measuring the semantic identity
  between this entity and the target entity,
  where a score closer to 0 denotes the two entities being
  almost identical in terms of ontology concept.
  <br/> <br/>
  For ontology entites, this score is used to to determine
  whether this entity is the EFO equivalent of the query entity.
  `;
export const paramIcScore = `
  **IC (information content) score**: <br/>
  A score (<code>[0, 1]</code>) measuring the information content
  of this ontology term,
  where a score closer to 0 denotes that this term
  is a generic term that is close to the base "EFO" term ,
  and a score closer to 1 denotes that this term
  is a specific term.
  <br/> <br/>
  For ontology entities, this score is used to filter out
  terms that are overly generic.
  `;

export const paramNumOntologyEntCandidates = `
 **Max number of ontology candidates**: <br />
 Maximum number of ontology (EFO) entity candidates to retrieve
 for the specific claim subject / object.
`;

export const postOntologyNumCandidates = `
**Max number of UMLS/GWAS trait entity candidates**: <br />
Maximum number of UMLS/GWAS trait entity candidates to retrieve
which are semantically similar to the reference ontology term.
`;

export const assocPvalThreshold = `
**P-Value threshold for association evidence retrieval**: <br />

Statistical significance measured in P-Value which is used to
classify the evidence groups a specific piece of evidence belongs to
(refer to documentation on the details).
`;
