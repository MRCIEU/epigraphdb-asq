from typing import List, Optional

import pandera as pa
from pandera.typing import DataFrame
from pydantic import validate_arguments

from ..types import Config, ent_types, triples_types
from . import processing

ALLOWED_EVIDENCE_TYPE = ["supporting", "contradictory"]
EVIDENCE_TYPES = {
    "directional": ["supporting", "contradictory"],
    "undirectional": ["supporting"],
}


class TripleEvidenceProcessor:
    @validate_arguments
    def __init__(self, config: Config):
        self.config: Config = config
        self.empty_df = (
            triples_types.TripleEvidenceDf.example(size=1).iloc[:0, :].copy()
        )
        self.reset()

    def reset(self):
        self._evidence_df: Optional[
            DataFrame[triples_types.TripleEvidenceDf]
        ] = None

    @property  # type: ignore
    @pa.check_types
    def evidence_df(self) -> DataFrame[triples_types.TripleEvidenceDf]:
        if self._evidence_df is not None:
            return self._evidence_df
        else:
            return self.empty_df

    def process(
        self,
        evidence_type: str,
        subject_ents: List[ent_types.BaseEnt],
        object_ents: List[ent_types.BaseEnt],
        pred_term: str,
    ) -> bool:
        assert evidence_type in ALLOWED_EVIDENCE_TYPE
        subject_ids = [_["ent_id"] for _ in subject_ents]
        object_ids = [_["ent_id"] for _ in object_ents]
        if evidence_type == "supporting":
            evidence_df = processing.get_triples(
                subject_ids=subject_ids,
                object_ids=object_ids,
                umls_pred=pred_term,
                direction="forward",
                config=self.config,
            )
        elif evidence_type == "contradictory":
            evidence_df = processing.get_triples(
                subject_ids=object_ids,
                object_ids=subject_ids,
                umls_pred=pred_term,
                direction="reverse",
                config=self.config,
            )
        if evidence_df is None:
            return False
        self._evidence_df = evidence_df
        return True
