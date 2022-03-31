export const mappingScore = `
**Mapping score**: <br/>

A score <code>[0, 1]</code> which measures the outcome of the entity harmonization process between the query claim term and the evidence term.
The mapping score is a constituent score to the final <code>evidence score</code> of the retrieved evidence.

The higher the mapping score is the closer the evidence term is to the query claim term in semantic similarity.
Therefore a mapping score very close to 1 denotes the evidence term is nearly identical to the query claim term, and in turn the retrieved evidence should receive minimal penalty from semantic deviation from the query claim.

The score is computed as the product of semantic similarities from all involved entities from multiple taxnomies. Therefore for situation A where the similarities scores are close to 1 versus situation B where similarities scores are about 0.7, the mapping score from B is much lower than that from A, and in turn the retrieved evidence from B suffers much larger penalty than that from A.

For further technical details refer to the ASQ paper.
`;

export const tripleScore = `
**Triple and literature strength score**: <br/>

A score <code>[1, inf)</code> which measures the innate strength of the retrieved evidence for triple and literature evidence.
The strength score is a constituent score to the final <code>evidence score</code> of the retrieved evidence.
A higher score denotes a strong evidence.

The score is computed based on the number of source literature that is associated with the triple, i.e. a triple that has more source literature where they contain such this semantic triple is stronger than another triple with fewer associated source literature.

The strength score is a constituent score to the final <code>evidence score</code> of the retrieved evidence.
`;

export const assocScore = `
**Association strength score**: <br/>

A score <code>[1, inf)</code> which measures the innate strength of the retrieved evidence for association evidence.
The strength score is a constituent score to the final <code>evidence score</code> of the retrieved evidence.
A higher score denotes a strong evidence.

The score is computed based on the absolute value of the standardized effect size (<code>|(effect size / SE)|</code>).
So an evidence item that has a higher score is stronger in statistical evidence then another evidence item with a lower score, in the sense that the former has a larger standardized effect size.
**However** caution should be taken in naively evaluating statistical results (within the same evidence sources or across multiple sources) with just simplifying statistics.

The strength score is a constituent score to the final <code>evidence score</code> of the retrieved evidence.
`;

export const evidenceScore = `
**Evidence score**: <br/>

The evidence score <code>[0, inf)</code> is computed as the product of the mapping score and the innate strength score, to measure the overall strength of the retrieved evidence item against the claim of interest, where a higher score denotes a stronger evidence to the claim.

The evidence score is primarily a metric to assist the evaluation of an evidence item against another item, or a group of evidence against another group, however researchers <b>should not</b> simply rely on overly simplified metrics as a substitute for the thorough investigation of the retrieved evidence.
`;
