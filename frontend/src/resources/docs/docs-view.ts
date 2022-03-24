export const aboutPt0: string = `
# Annotated Semantic Queries (ASQ)

The [EpiGraphDB-ASQ](https://asq.epigraphdb.org) (ASQ; \`/ɑːsk/\` i.e. "ask") interface serves as a natural language interface to query the integrated epidemiological evidence of the EpiGraphDB data and ecosystem.

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
## Key concepts

TODO

## Citation

Propoer citation details will be available shortly.
Until then please cite this website https://asq.epigraphdb.org
if you use ASQ.

`;

export const analysisAbout: string = `
# Systematic analysis on medRxiv submissions 2020-2021

TODO
`;

export const sectionDocs: Record<string, string> = {
  entities: `TODO`,
  params: `Parameters used in ASQ.`,
  stages: `
The various stages of the web interface queries of ASQ.
The following are what you see as instruction text on the query stages.
`,
  components: `Component widgets used on the web interface`,
  tripleEvidence: `TODO`,
  assocEvidence: `TODO`,
};
