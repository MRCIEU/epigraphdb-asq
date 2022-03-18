from typing import List, Optional

import pandera as pa
from loguru import logger
from pandera.typing import DataFrame
from pydantic import validate_arguments

from ..resources import epigraphdb
from ..settings import params
from ..types import Config, assoc_types, ent_types
from . import processing

# - supporting:
#   subject is linked to object with a significant signal (pval)
#
# - contradictory_directional_type1:
#   object is linked to subject, no pval thresholding
#   "reverse evidence"
#
# - contradictory_directional_type2:
#   subject is linked to object, with an insignificant signal,
#   "evidence of absence"
#
# - contradictory_undirectional:
#   subject is linked to object, with an insignificant signal,
#   "evidence of absence"
#
# - generic_directional:
#   any info that might be of additional use
#   e.g. correlational evidence when the query is directional


ALLOWED_EVIDENCE_TYPE = [
    "supporting",
    "contradictory_directional_type1",
    "contradictory_directional_type2",
    "contradictory_undirectional",
    "generic_directional",
]
DIRECTIONAL_EVIDENCE_TYPE = [
    "supporting",
    "contradictory_directional_type1",
    "contradictory_directional_type2",
    "generic_directional",
]
UNDIRECTIONAL_EVIDENCE_TYPE = [
    "supporting",
    "contradictory_undirectional",
]
EVIDENCE_TYPES = {
    "directional": DIRECTIONAL_EVIDENCE_TYPE,
    "undirectional": UNDIRECTIONAL_EVIDENCE_TYPE,
}


class AssocEvidenceProcessor:
    @validate_arguments
    def __init__(self, config: Config):
        self.config: Config = config
        self.reset()

    def reset(self):
        self._evidence_df = None

    @property  # type: ignore
    @pa.check_types
    def evidence_df(self) -> Optional[DataFrame[assoc_types.AssocEvidenceDf]]:
        return self._evidence_df

    def process(
        self,
        evidence_type: str,
        subject_ents: List[ent_types.BaseEnt],
        object_ents: List[ent_types.BaseEnt],
        pred_term: str,
        pval_threshold: float = params.ASSOC_PVAL_THRESHOLD,
    ) -> bool:
        assert evidence_type in ALLOWED_EVIDENCE_TYPE
        assert pred_term in epigraphdb.EPIGRAPHDB_SEMREP_PREDS
        if pred_term in epigraphdb.EPIGRAPHDB_PRED_GROUP["directional"]:
            assert evidence_type in DIRECTIONAL_EVIDENCE_TYPE
        elif pred_term in epigraphdb.EPIGRAPHDB_PRED_GROUP["undirectional"]:
            assert evidence_type in UNDIRECTIONAL_EVIDENCE_TYPE
        subject_ids = [_["ent_id"] for _ in subject_ents]
        object_ids = [_["ent_id"] for _ in object_ents]
        evidence_df = processing.get_evidence_results(
            subject_ids=subject_ids,
            object_ids=object_ids,
            evidence_type=evidence_type,
            pred_term=pred_term,
            pval_threshold=pval_threshold,
            config=self.config,
        )
        if len(evidence_df) == 0:
            logger.debug("evidence_df is empty")
            return False
        self._evidence_df = evidence_df
        return True
