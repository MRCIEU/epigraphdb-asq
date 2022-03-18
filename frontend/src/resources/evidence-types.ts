export const ASSOC_EVIDENCE_DETAILS: Record<string, any> = {
  undirectional: {
    supporting: {
      label: "Supporting evidence",
    },
    contradictory_undirectional: {
      label: "Insufficient evidence",
    },
  },
  directional: {
    supporting: {
      label: "Supporting evidence",
    },
    contradictory_directional_type1: {
      label: "Contradictory evidence, reversal",
    },
    contradictory_directional_type2: {
      label: "Insufficient evidence",
    },
    generic_directional: {
      label: "Additional general evidence",
    },
  },
};

export const TRIPLE_EVIDENCE_DETAILS: Record<string, any> = {
  undirectional: {
    supporting: {
      label: "Supporting evidence",
    },
  },
  directional: {
    supporting: {
      label: "Supporting evidence",
    },
    contradictory: {
      label: "Contradictory evidence, reversal",
    },
  },
};
