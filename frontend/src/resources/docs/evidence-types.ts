type EvidenceDocs = Record<string, Record<string, string>>;

export const tripleLiteratureEvidenceTypes: EvidenceDocs = {
  directional: {
    supporting: `
**Supporting evidence (directional)**: <br/>
EpiGraphDB knowledge triple evidence (<code>LiteratureTriple</code>)
that supports the claim of the query triple.

Retrieved evidence takes the form of
<code>subject - predicate -> object</code> (*directional*), where

- subject is one of the mapped UMLS subject entities
- object is one of the mapped UMLS object entities
- predicate is the query predicate

Retrieved literature evidence is EpiGraphDB literature data
(<code>Literature</code>) that relate to the retrieved knowledge triples.
  `,
    contradictory: `
**Contradictory evidence (directional, reversal evidence)**: <br/>
EpiGraphDB knowledge triple evidence (<code>LiteratureTriple</code>)
that contradicts the supporting evidence by
the existence of reversal evidence.

Retrieved evidence takes the form of
<code>object - predicate -> subject</code> (*directional*), where

- subject is one of the mapped UMLS subject entities
- object is one of the mapped UMLS object entities
- predicate is the query predicate

In this case the contradictory evidence results should be treated
as the reverse of the supporting evidence results.

Retrieved literature evidence is EpiGraphDB literature data
(<code>Literature</code>)
that relate to the retrieved knowledge triples.
  `,
  },
  undirectional: {
    supporting: `
**Supporting evidence (undirectional)**: <br/>
EpiGraphDB knowledge triple evidence (<code>LiteratureTriple</code>)
that supports the claim of the query triple.

Retrieved evidence takes the form of
<code>subject - predicate - object</code> (*undirectional*), where

- subject is one of the mapped UMLS subject entities
- object is one of the mapped UMLS object entities
- predicate is the query predicate

Retrieved literature evidence is EpiGraphDB literature data
(<code>Literature</code>) that relate to the retrieved knowledge triples.

**NOTE**: In this case of an undirectional predicate, there is not
a *contradictory* evidence category.
  `,
  },
};

export const assocEvidenceTypes: EvidenceDocs = {
  undirectional: {
    supporting: `
**Supporting evidence (undirectional)**: <br/>
EpiGraphDB phenotype association evidence that
supports the claim of the query triple.

Retrieved evidence takes the form of
<code>subject - predicate - object</code> (*undirectional*), where

- subject is one of the mapped GWAS trait subject entities
- object is one of the mapped GWAS trait object entities
- predicate is one of the following evidence
  - MR-EvE (<code>MR_EVE_MR</code>)
  - Polygenic risk score association (<code>PRS</code>)
  - Genetic correlation (<code>GEN_COR</code>)
- P-Value of the evidence is *below* the specified threshold
    `,
    contradictory_undirectional: `
**Contradictory evidence (undirectional, absence)**: <br/>
EpiGraphDB phenotype association evidence that
contradicts the supporting evidence by
the existence of evidence which fails to qualify as "supporting evidence".

Retrieved evidence takes the form of
<code>subject - predicate - object</code> (*undirectional*), where

- subject is one of the mapped GWAS trait subject entities
- object is one of the mapped GWAS trait object entities
- predicate is one of the following evidence
  - MR-EvE (<code>MR_EVE_MR</code>)
  - Polygenic risk score association (<code>PRS</code>)
  - Genetic correlation (<code>GEN_COR</code>)
- P-Value of the evidence is *above* the specified threshold
    `,
  },
  directional: {
    supporting: `
**Supporting evidence (directional)**: <br/>
EpiGraphDB phenotype association evidence that
supports the claim of the query triple.

Retrieved evidence takes the form of
<code>subject - predicate - object</code> (*directional*), where

- subject is one of the mapped GWAS trait subject entities
- object is one of the mapped GWAS trait object entities
- predicate is one of the following evidence
  - MR-EvE (<code>MR_EVE_MR</code>)
- P-Value of the evidence is *below* the specified threshold
    `,
    contradictory_directional_type1: `
**Contradictory evidence (directional, reversal evidence)**: <br/>
EpiGraphDB phenotype association evidence that
contradicts the supporting evidence by
the existence of reversal evidence.

Retrieved evidence takes the form of
<code>object - predicate -> subject</code> (*directional*), where

- object is one of the mapped GWAS trait object entities
- subject is one of the mapped GWAS trait subject entities
- predicate is one of the following evidence
  - MR-EvE (<code>MR_EVE_MR</code>)
- P-Value of the evidence is *below* the specified threshold
    `,
    contradictory_directional_type2: `
**Insufficient evidence (directional)**: <br/>
EpiGraphDB phenotype association evidence that
complements the supporting evidence by
the existence of evidence which fails to qualify as "supporting evidence".

Retrieved evidence takes the form of
<code>subject - predicate -> object</code> (*directional*), where

- subject is one of the mapped GWAS trait subject entities
- object is one of the mapped GWAS trait object entities
- predicate is one of the following evidence
  - MR-EvE (<code>MR_EVE_MR</code>)
- P-Value of the evidence is *above* the specified threshold
    `,
    generic_directional: `
**Additional evidence (directional)**: <br/>
EpiGraphDB phenotype association evidence that shows correlation between the
phenotypes without causal assertion, which acts as additional information.

Retrieved evidence takes the form of
<code>subject - predicate - object</code> (*undirectional*), where

- subject is one of the mapped GWAS trait subject entities
- object is one of the mapped GWAS trait object entities
- predicate is one of the following evidence
  - Polygenic risk score association (<code>PRS</code>)
  - Genetic correlation (<code>GEN_COR</code>)
- P-Value is *not restricted*
    `,
  },
};
