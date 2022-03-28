export const ent = `
**Entity representation**

In ASQ we denote a **taxonomy** as a catalog of biomedical terms in a specific domain, i.e. UMLS, EFO, as well as GWAS trait names from OpenGWAS and UK Biobank.
And in turn we refer to an <span class="mark">entity</span> as a member of a taxonomy, which contains an <code>ID</code> and a <code>label</code>.

A biomedical concept (e.g. "body mass index") can be represented by various entities in different taxonomies with different degrees of association and relevance. In ASQ we primarily measure such relevance by the semantic similarities between the concept and the entities, which are calculated as the cosine similarities of the text embeddings.
`;

export const triple = `
**Semantic knowledge triple**

A semantic knowledge triple (or simply "triple") is a representation of a *claim*
involving represented entities in the form of

<code>subject entity</code> - <code>predicate</code> - <code>object entity</code>,

which in turn can be introspected with structural query of
supporting and contradictory groups of evidence.
`;

export const claimTriple = `
**Query claim triple**

A triple that is parsed from the input query text.
`;

export const validTriple = `
**Valid claim triple**

In the context of ASQ, a valid claim triple is one that ASQ is able to find relevant evidence items, e.g. its predicate is a valid predicate that ASQ currently supports.
`;

export const invalidTriple = `
**Invalid claim triple**

In the context of ASQ, an invalid claim triple is one that ASQ is not able to proceed with further investigation, e.g. its predicate is not a valid predicate that ASQ currently supports.
`;
