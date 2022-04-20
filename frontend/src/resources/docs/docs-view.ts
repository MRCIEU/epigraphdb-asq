export const aboutInit: string = `
The [EpiGraphDB-ASQ](https://asq.epigraphdb.org) (ASQ; \`/ɑːsk/\` i.e. "ask") interface is a natural language interface to query the integrated epidemiological evidence of the EpiGraphDB data and ecosystem.
The starting point of the query is either a short paragraph of text from which ASQ will derive and extract claim triples, or users can supply those claim triples directly.
ASQ will retrieve data from EpiGraphDB, both biomedical entities and evidence from various sources, to faciliate the triangulation of the evidence regarding a specific claim.

This page collects all the documentation fragments you see in the web interface.
`;

export const aboutPt0: string = `
## Main functionalities

The main functionalities of ASQ are offered via the following links

- <a href="/" target="_blank">https://asq.epigraphdb.org</a>:
  The primary entry point accepts a short text document where ASQ will attempt to derive claim triples and retrieves relevant evidence from EpiGraphDB for evidence triangulation
- <a href="/triple" target="_blank">https://asq.epigraphdb.org/triple</a>:
  A secondary entry point where users can instead put the query triple to initialize the processing
- <a href="/medrxiv-analysis" target="_blank">https://asq.epigraphdb.org/medrxiv-analysis</a>:
  Systematic analysis results on preprint submissions on medRxiv from 2020-01-01 to 2021-12-31
`;

export const aboutPt1: string = `
## Query stages

1. At the <a href="/" target="_blank">entry point of the web interface</a>, ASQ accepts a short text document where it will attempt to extract **claim triples** from the text.
You will then be asked to select a specific <span class="mark">claim triple</span> to proceed to the next step.
1. At the next **Entity harmonization** step, you will be asked to pick associated <span class="mark">ontology entities</span> (EFO) that can represent the subject and object terms of the claim triple.
1. ASQ will then retrieve associated <span class="mark">evidence entities</span> and <span class="mark">evidence items</span> regarding the claim triple.
1. You can now investigate the retrieved evidence or update the results with adjusted parameters.
`;

export const aboutPt2: string = `
## Key concepts

Retrieved eidence from EpiGraphDB are categorized according to the following groups.

**Evidence groups**

- <span class="mark1">Triple and literature evidence</span> consists of EpiGraphDB curated semantic knowledge triples derived from literature, and the source literature that supports them
- <span class="mark1">Association evidence</span> consits of EpiGraphDB curated statistical association analysis results on GWAS traits.

**Predicate groups**

- <span class="mark1">Directional</span> predicates that imply directionality, e.g. <code>CAUSES</code>, <code>TREATS</code>, <code>AFFECTS</code>, <code>PRODUCES</code>
- <span class="mark1">Non-directional</span> predicates that imply no directionality or bi-directionality, e.g. <code>ASSOCIATED_WITH</code>, <code>COEXISTS_WITH</code>, <code>INTERACTS_WITH</code>

**Evidence types**

- <span class="mark1">Supporting evidence</span> are those that support the query claim with sufficient level of strength
- <span class="mark1">Reversal evidence</span> are those that contradict the query claim, with idenfied evidence supporting a reversal claim, with sufficient level of strength
- <span class="mark1">Insufficient evidence</span> are those that fail to qualify as supporting and reversal evidence due the an insufficient level of strength. Insufficent evidence helps to determine the scope of evidence identification, and to distinguish situations of *evidence of absence* versus the *absence of evidence*.
- <span class="mark1">Addition evidence</span> are those that would not fit into the above categories but can still be evaluated by the users

Further details can be found at the respective documentation of these concepts.
`;

export const aboutCitation: string = `
## Citation

**Triangulating evidence in health sciences with Annotated Semantic Queries**,
Yi Liu, Tom R Gaunt,
medRxiv 2022.04.12.22273803; doi: https://doi.org/10.1101/2022.04.12.22273803

\`\`\`
@article{Liu-Gaunt-2022-ASQ,
  author = {Liu, Yi and Gaunt, Tom R},
  title = {Triangulating evidence in health sciences with Annotated Semantic Queries},
  elocation-id = {2022.04.12.22273803},
  year = {2022},
  doi = {10.1101/2022.04.12.22273803},
  publisher = {Cold Spring Harbor Laboratory Press},
  URL = {https://www.medrxiv.org/content/early/2022/04/16/2022.04.12.22273803},
  eprint = {https://www.medrxiv.org/content/early/2022/04/16/2022.04.12.22273803.full.pdf},
  journal = {medRxiv}
}
\`\`\`
`;
