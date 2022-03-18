from typing import List, Optional

import pandas as pd
import pandera as pa
from pandera.typing import DataFrame
from pydantic import validate_arguments

from ..settings import params
from ..types import Config, ent_types
from . import processing

from icecream import ic  # noqa


class UmlsEntHarmonizer:
    @validate_arguments
    def __init__(self, config: Config):
        self.config = config
        self.reset()

    def reset(self):
        self._ents_df: Optional[DataFrame[ent_types.PhenotypeEntDf]] = None
        self._similarity_scores_df: Optional[
            DataFrame[ent_types.PhenotypeSimilarityScoreDf]
        ] = None

    @property  # type: ignore
    @pa.check_types
    def ents_df(self) -> Optional[DataFrame[ent_types.PhenotypeEntDf]]:
        return self._ents_df

    @property
    def ents(self) -> List[ent_types.BaseEnt]:
        if self._ents_df is None:
            return []
        else:
            res: List[ent_types.BaseEnt] = (
                self._ents_df[["ent_id", "ent_term"]]
                .drop_duplicates()
                .to_dict(orient="records")
            )
            return res

    def harmonize(
        self,
        umls_ent: ent_types.BaseEnt,
        ontology_ents: List[ent_types.BaseEnt],
        num_similarity_candidates: int = params.NUM_SIMILARITY_CANDIDATES_UMLS,
        similarity_score_threshold: float = params.SIM_THRESHOLD_UMLS,
        verbose: bool = False,
    ) -> bool:
        sim_scores = [
            _
            for _ in (
                [
                    self._process_similarity_on_umls(
                        umls_id=umls_ent["ent_id"],
                        umls_term=umls_ent["ent_term"],
                        num_similarity_candidates=num_similarity_candidates,
                        similarity_score_threshold=similarity_score_threshold,
                    )
                ]
                + [
                    self._process_similarity_on_efo(
                        _,
                        num_similarity_candidates=num_similarity_candidates,
                        similarity_score_threshold=similarity_score_threshold,
                    )
                    for _ in ontology_ents
                ]
            )
            if _ is not None
        ]
        if len(sim_scores) == 0:
            return False
        similarity_scores_df = pd.concat(sim_scores).reset_index(drop=True)
        ents = (
            similarity_scores_df[["ent_id", "ent_term"]]
            .drop_duplicates()
            .to_dict(orient="records")
        )
        # NOTE: PLACEHOLDER
        filtered_ents = ents
        ents_df = (
            similarity_scores_df[
                similarity_scores_df["ent_id"].isin(
                    [_["ent_id"] for _ in filtered_ents]
                )
            ]
            .assign(meta_ent="LiteratureTerm")
            .reset_index(drop=True)
        )
        self._similarity_scores_df = similarity_scores_df
        self._ents_df = ents_df
        return True

    @pa.check_types
    def _process_similarity_on_efo(
        self,
        ontology_ent: ent_types.BaseEnt,
        num_similarity_candidates: int,
        similarity_score_threshold: float,
    ) -> Optional[DataFrame[ent_types.PhenotypeSimilarityScoreDf]]:
        df = processing.umls_similarity_candidates_on_efo(
            ent_id=ontology_ent["ent_id"],
            limit=num_similarity_candidates,
            similarity_score_threshold=similarity_score_threshold,
            config=self.config,
        )
        if df is None:
            return None
        else:
            df = df.assign(
                ref_meta_ent="Efo",
                ref_ent_id=ontology_ent["ent_id"],
                ref_ent_term=ontology_ent["ent_term"],
            )
            return df

    @pa.check_types
    def _process_similarity_on_umls(
        self,
        umls_id: str,
        umls_term: str,
        num_similarity_candidates: int,
        similarity_score_threshold: float,
    ) -> Optional[DataFrame[ent_types.PhenotypeSimilarityScoreDf]]:
        df = processing.umls_similarity_candidates_on_umls(
            umls_term=umls_term,
            limit=num_similarity_candidates,
            similarity_score_threshold=similarity_score_threshold,
            config=self.config,
        )
        if df is None:
            return None
        else:
            df = df.assign(
                ref_meta_ent="QueryUMLS",
                ref_ent_id=umls_id,
                ref_ent_term=umls_term,
            )
            return df
