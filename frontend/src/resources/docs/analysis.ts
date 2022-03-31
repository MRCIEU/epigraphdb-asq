export const about: string = `
# Systematic analysis on medRxiv submissions 2020-2021

We analysed the preprint submissions on medRxiv from 2020-01-01 to 2021-12-31 to demonstrate the use of ASQ to triangulating evidence in epidemiology.

Details on the analysis will be available in the forthcoming manuscript on ASQ.

## Results table

The analysis page reports the results organised by claim triples, where each entry shows the summaised metrics in the format of \`evidence score (evidence item count)\` for \`evidence groups\` and \`evidence types\`. Users to click on the claim triple to visit the results page.

## Network diagram

The network diagram shows the summary of the research topics and research interests of recent medRxiv submissions,
that have been parsed by ASQ and has available evidence from EpiGraphDB.

The size of a node is measured as the frequency of the term.
In the default unconfigured state, the highlighted nodes (\`primary nodes\`) are those that are among the most frequent terms from the results.
In the default unconfigured state, the size of an edge is measured by the aggregated supporting evidence score between the two terms from both evidence groups (triple and literature evidence, as well as association evidence).
`;

export const tripleEvidenceSupporting = `
Supporting evidence type for the triple and literature evidence group.

The column reports values in the format of <code>A (B)</code>,
where <code>A</code> denotes the aggregated score within the evidence type,
and <code>B</code> denotes the number of retrieved evidence items.

Further details can be found on the documentation page.
`;

export const tripleEvidenceReversal = `
Reversal evidence type for the triple and literature evidence group.

The column reports values in the format of <code>A (B)</code>,
where <code>A</code> denotes the aggregated score within the evidence type,
and <code>B</code> denotes the number of retrieved evidence items.

Further details can be found on the documentation page.
`;

export const assocEvidenceSupporting = `
Supporting evidence type for the association evidence group.

The column reports values in the format of <code>A (B)</code>,
where <code>A</code> denotes the aggregated score within the evidence type,
and <code>B</code> denotes the number of retrieved evidence items.

Further details can be found on the documentation page.
`;

export const assocEvidenceReversal = `
Reversal evidence type for the association evidence group.

The column reports values in the format of <code>A (B)</code>,
where <code>A</code> denotes the aggregated score within the evidence type,
and <code>B</code> denotes the number of retrieved evidence items.

Further details can be found on the documentation page.
`;

export const assocEvidenceInsufficient = `
Insufficient evidence type for the association evidence group.

The column reports values in the format of <code>A (B)</code>,
where <code>A</code> denotes the aggregated score within the evidence type,
and <code>B</code> denotes the number of retrieved evidence items.

Further details can be found on the documentation page.
`;

export const assocEvidenceAdditional = `
Additional evidence type for the association evidence group.

The column reports values in the format of <code>A (B)</code>,
where <code>A</code> denotes the aggregated score within the evidence type,
and <code>B</code> denotes the number of retrieved evidence items.

Further details can be found on the documentation page.
`;
