from functools import partial
from typing import Callable, Dict, List, Optional, Tuple

import pandas as pd
import pandera as pa
from pandera.typing import DataFrame
from pydantic import validate_arguments

from ..funcs import ent_filters
from ..resources import epigraphdb
from ..settings import params
from ..types import Config, ent_types
from . import processing

from icecream import ic  # noqa

filter_funcs: Dict[str, List[Callable]] = {
    "directional": [
        ent_filters.exist_with_epigraphdb_mr_eve_mr,
        ent_filters.prefix_filter,
    ],
    "undirectional": [
        ent_filters.exist_with_epigraphdb_undirectional_assoc,
        ent_filters.prefix_filter,
    ],
}


class PhenotypeEntHarmonizer:
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
        ontology_ents: List[ent_types.BaseEnt],
        pred_term: str,
        num_similarity_candidates: int = params.NUM_SIMILARITY_CANDIDATES_TRAIT,
        similarity_score_threshold: float = params.SIM_THRESHOLD_TRAIT,
        verbose: bool = True,
    ) -> bool:
        sim_scores = [
            _
            for _ in (
                [
                    self._process_similarity(
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
        pre_partial_funcs: List[Callable] = filter_funcs[
            epigraphdb.PRED_DIRECTIONAL_MAPPING[pred_term]
        ]
        filter_funcs_partialed: List[ent_types.FilterFunc] = [
            partial(_, config=self.config, verbose=verbose)
            for _ in pre_partial_funcs
        ]
        ents = (
            similarity_scores_df[["ent_id", "ent_term"]]
            .drop_duplicates()
            .to_dict(orient="records")
        )
        filtered_ents = processing.traits_filter_ents_by_predicates(
            ents=ents, funcs=filter_funcs_partialed,
        )
        ents_df = (
            similarity_scores_df[
                similarity_scores_df["ent_id"].isin(
                    [_["ent_id"] for _ in filtered_ents]
                )
            ]
            .assign(meta_ent="Gwas")
            .reset_index(drop=True)
        )
        self._similarity_scores_df = similarity_scores_df
        self._ents_df = ents_df
        return True

    @pa.check_types
    def _process_similarity(
        self,
        ontology_ent: ent_types.BaseEnt,
        num_similarity_candidates: int,
        similarity_score_threshold: float,
    ) -> Optional[DataFrame[ent_types.PhenotypeSimilarityScoreDf]]:
        df = processing.gwas_similarity_candidates(
            ent_id=ontology_ent["ent_id"],
            limit=num_similarity_candidates,
            similarity_score_threshold=similarity_score_threshold,
            config=self.config,
        )
        if df is None:
            return None
        else:
            df = df.assign(
                ref_ent_id=ontology_ent["ent_id"],
                ref_ent_term=ontology_ent["ent_term"],
                ref_meta_ent="Efo",
            )
            return df

    def _format_ent_from_df(
        self, index: Tuple[str, str], df: DataFrame[ent_types.PhenotypeEntDf]
    ):
        ontology_ent: ent_types.BaseEnt = {
            "ent_id": index[0],
            "ent_term": index[1],
        }
        phenotype_ents: List[ent_types.PhenotypeEnt] = df[
            ["ent_id", "ent_term", "similarity_score"]
        ].to_dict(orient="records")
        res: ent_types.GroupedTraitEnts = {
            "ontology_ent": ontology_ent,
            "ents": phenotype_ents,
        }
        return res
