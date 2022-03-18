from typing import List, Optional

import pandera as pa
from pandera.typing import DataFrame
from pydantic import validate_arguments

from ..settings import params
from ..types import Config, ent_types
from . import processing

from icecream import ic  # noqa


class OntologyEntHarmonizer:
    @validate_arguments
    def __init__(self, config: Config):
        self.config = config
        self.reset()

    def reset(self):
        self._ents_df: Optional[DataFrame[ent_types.OntologyEntDf]] = None
        self._candidates_df: Optional[
            DataFrame[ent_types.OntologyEntDf]
        ] = None
        self._similarity_scores_df: Optional[
            DataFrame[processing.SimilarityScoresDf]
        ] = None
        self._ic_scores_df: Optional[DataFrame[processing.IcScoresDf]] = None
        self._identity_scores_df: Optional[
            DataFrame[processing.IdentityScoresDf]
        ] = None

    @property  # type: ignore
    @pa.check_types
    def candidates_df(self) -> Optional[DataFrame[ent_types.OntologyEntDf]]:
        return self._candidates_df

    @property  # type: ignore
    def candidates(self) -> List[ent_types.OntologyEnt]:
        if self._candidates_df is None:
            return []
        else:
            res: List[ent_types.OntologyEnt] = self._candidates_df.to_dict(
                orient="records"
            )
            return res

    @property  # type: ignore
    @pa.check_types
    def ents_df(self) -> Optional[DataFrame[ent_types.OntologyEntDf]]:
        return self._ents_df

    @property  # type: ignore
    def ents(self) -> List[ent_types.OntologyEnt]:
        if self._ents_df is None:
            return []
        else:
            res: List[ent_types.OntologyEnt] = self._ents_df.to_dict(
                orient="records"
            )
            return res

    @validate_arguments
    def harmonize(
        self,
        ent_id: str,
        ent_term: str,
        similarity_score_threshold: float = params.SIM_THRESHOLD_EFO,
        num_similarity_candidates: int = params.NUM_SIMILARITY_CANDIDATES_EFO,
        ic_score_threshold: float = params.IC_THRESHOLD_EFO,
        identity_score_threshold: float = params.IDENTITY_THRESHOLD,
    ) -> bool:
        similarity_scores_df = processing.efo_similarity_candidates(
            term=ent_term,
            limit=num_similarity_candidates,
            similarity_score_threshold=similarity_score_threshold,
            config=self.config,
        )
        if similarity_scores_df is None:
            return False
        ic_scores_df = processing.efo_ic_scores(
            ent_ids=similarity_scores_df["ent_id"].tolist(),
            ic_score_threshold=ic_score_threshold,
            config=self.config,
        )
        identity_scores_df = processing.efo_identity_scores(
            reference_term=ent_term,
            ents=ic_scores_df[["ent_id", "ent_term"]].to_dict(
                orient="records"
            ),
            config=self.config,
        )
        identity_valid = identity_scores_df[
            identity_scores_df.apply(
                lambda row: abs(row["identity_score"])
                <= identity_score_threshold,
                axis=1,
            )
        ]
        candidates_df = identity_scores_df.merge(
            ic_scores_df,
            left_on=["ent_id", "ent_term"],
            right_on=["ent_id", "ent_term"],
        ).merge(
            similarity_scores_df,
            left_on=["ent_id", "ent_term"],
            right_on=["ent_id", "ent_term"],
        )[
            [
                "ent_id",
                "ent_term",
                "similarity_score",
                "ic_score",
                "identity_score",
            ]
        ]
        ents_df = candidates_df[
            candidates_df["ent_id"].isin(identity_valid["ent_id"])
        ]
        # NOTE: this is for type inferencing
        self._similarity_scores_df = similarity_scores_df
        self._ic_scores_df = ic_scores_df
        self._identity_scores_df = identity_scores_df
        self._candidates_df = candidates_df
        self._ents_df = ents_df
        return True
