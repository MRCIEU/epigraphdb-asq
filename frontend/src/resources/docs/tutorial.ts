export const introduction = `**Introduction**

Here we briefly cover how to use the ASQ platform.

The primary use of ASQ is to extract claims from your input text on scientific literature findings,
and then for a claim of interest ASQ will retrieve evidence from
[EpiGraphDB](https://epigraphdb.org)
and harmonize them into various categories
(by nature of the evidence source, by the relationship of the evidence against the query
in terms of whether the evidence support the claim or not)
for evidence triangulation.

The rough steps for using the ASQ platform are as follows:

1. The query stage
    1. [Extraction of claims](#text-qeury)
    1. [Harmonization of the query entities](#entity-harmonization)
1. The evidence comparison stage
    1. [Retrieval of evidence from EpiGraphDB](#evidence-retrieval)

Please also visit [the docs page](/docs) for further details of technical terms.
`;

export const textQuery = `**Text query input**

Insert a paragraph of text
(by enabling the <span style="color:green">"Custom claim text"</span> option)
that might contain some claims
of biomedical nature,
or use a predefined text as a demonstration.

<span style="color:blue">Confirm and proceed.</span>
The input text will be parsed to generate claim triples.

`;

export const claimTripleSelection = `**Claim triple selection**

From the parsed triples,
<span style="color:green">select a claim triple</span> to focus for further analysis.
This triple is then parsed to retrieve ontology entities in EpiGraphDB.

`;

export const claimEntitySelection = `**Select paired ontology entities for the claim triple**

Select <span style="color:orange">subject</span>
(<span style="color:green">object</span>) ontology entities that represent
the claim subject (object) entities, which will be used as
the basis of further entity harmonization and subsequent
evidence retrieval procedures.

By default, suitable candidates have been picked automatically.
`;

export const loading = `**Query stage done!**

ASQ will now retrieve evidence that can be associated with the user's claim query.

`;

export const evidenceSummary = `**Summary of the retrieved evidence**

This page view summarises the retrieved evidence:

- How many entities (ontology, UMLS, GWAS trait) have been retrieved
- How many evidence items have been retrieved, specifically:
    - For Triple and literature evidence, for association evidence
    - For supporting evidence, contradictory evidence, etc
- How the <span style="color:red">query triple</span> relates to
the retrieved evidence triples
`;

export const evidenceGroup = `**Evidence group**

This is an exemplar view of an evidence group,
which in this case is for **association** evidence items
that are **supporting** the claim.

There are further summary details for including item counts,
evidence scores and strength scores at the group level.

This page view also shows individual evidence item.
Each row comes with a link to the corresponding view in EpiGraphDB
for this item.
`;

export const parameters = `**Configure parameters**

At both the query stage and the evidence comparison stage
the user can adjust the various parameters regarding
the harmonization and retrieval of entities and evidence.

Clicking the <span style="color:blue">"UPDATE PARAMETERS"</span>
will trigger a refresh of the evidence retrieval session.

For further details regarding the parameters
please refer to [the docs page](/docs) for further details.
`;
