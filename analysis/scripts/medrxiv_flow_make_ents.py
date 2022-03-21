import json
import sys
from typing import Any, Dict, List, Optional

import pandas as pd
import ray
from common_processing import ent_harmonization
from common_processing.types import Params
from metaflow import FlowSpec, Parameter, step

from analysis import utils
from analysis.funcs.generic import interval_str
from analysis.settings import config, params

from icecream import ic  # noqa
from loguru import logger  # noqa

DATA_ROOT = utils.find_data_root()
ECHO_STEP = 10


def _make_efo_ents(
    doi: str,
    subject_term: str,
    object_term: str,
    triple_text: str,
    context_text: str,
    pred_term: str,
    triple_data: Dict[str, Any],
    params: Params,
) -> Optional[Dict]:
    try:
        ontology_ent_harmonizer = ent_harmonization.OntologyEntHarmonizer(
            config=config
        )
        # subjects
        ontology_ent_harmonizer.reset()
        ontology_ent_harmonizer.harmonize(
            ent_id="",
            ent_term=subject_term,
            similarity_score_threshold=params.SIM_THRESHOLD_EFO,
            num_similarity_candidates=params.NUM_SIMILARITY_CANDIDATES_EFO,
            ic_score_threshold=params.IC_THRESHOLD_EFO,
            identity_score_threshold=params.IDENTITY_THRESHOLD,
        )
        subject_ents = ontology_ent_harmonizer.ents
        subject_candidates = ontology_ent_harmonizer.candidates
        # objects
        ontology_ent_harmonizer.reset()
        ontology_ent_harmonizer.harmonize(
            ent_id="",
            ent_term=object_term,
        )
        object_ents = ontology_ent_harmonizer.ents
        object_candidates = ontology_ent_harmonizer.candidates
        # finalize
        valid = len(subject_ents) > 0 and len(object_ents) > 0
        if not valid:
            return None
        res = {
            "triple_text": triple_text,
            "context_text": context_text,
            "query_subject_term": subject_term,
            "query_object_term": object_term,
            "subject_ents": subject_ents,
            "subject_candidates": subject_candidates,
            "object_candidates": object_candidates,
            "object_ents": object_ents,
            "pred_term": pred_term,
            "triple_data": triple_data,
        }
        return res
    except Exception as e:
        logger.warning(f"Error, {doi=}, {triple_text=}; {e}")
        return None


def _make_umls_ents(
    doi: str,
    triple_text: str,
    query_subject_term: str,
    query_object_term: str,
    subject_efo_ents: List[Dict],
    object_efo_ents: List[Dict],
    params: Params,
) -> Optional[Dict]:
    try:
        umls_ent_harmonizer = ent_harmonization.UmlsEntHarmonizer(
            config=config
        )
        # subjects
        umls_ent_harmonizer.reset()
        umls_ent_harmonizer.harmonize(
            umls_ent={"ent_id": "", "ent_term": query_subject_term},
            ontology_ents=[
                {
                    "ent_id": _["ent_id"],
                    "ent_term": _["ent_term"],
                }
                for _ in subject_efo_ents
            ],
            num_similarity_candidates=params.NUM_SIMILARITY_CANDIDATES_UMLS,
            similarity_score_threshold=params.SIM_THRESHOLD_UMLS,
        )
        subject_umls_ents = umls_ent_harmonizer.ents_df
        # objects
        umls_ent_harmonizer.reset()
        umls_ent_harmonizer.harmonize(
            umls_ent={"ent_id": "", "ent_term": query_object_term},
            ontology_ents=[
                {
                    "ent_id": _["ent_id"],
                    "ent_term": _["ent_term"],
                }
                for _ in object_efo_ents
            ],
            num_similarity_candidates=params.NUM_SIMILARITY_CANDIDATES_UMLS,
            similarity_score_threshold=params.SIM_THRESHOLD_UMLS,
        )
        object_umls_ents = umls_ent_harmonizer.ents_df
        # finalize
        valid = (
            subject_umls_ents is not None
            and len(subject_umls_ents) > 0
            and object_umls_ents is not None
            and len(object_umls_ents) > 0
        )
        if not valid:
            return None
        res = {
            "triple_text": triple_text,
            "subject_ents": subject_umls_ents.to_dict(orient="records"),
            "object_ents": object_umls_ents.to_dict(orient="records"),
        }
        return res
    except Exception as e:
        logger.warning(f"Error, {doi=}, {triple_text=}; {e}")
        return None


def _make_trait_ents(
    doi: str,
    triple_text: str,
    pred_term: str,
    subject_efo_ents: List[Dict],
    object_efo_ents: List[Dict],
    params: Params,
) -> Optional[Dict]:
    try:
        phenotype_ent_harmonizer = ent_harmonization.PhenotypeEntHarmonizer(
            config=config
        )
        # subjects
        phenotype_ent_harmonizer.reset()
        phenotype_ent_harmonizer.harmonize(
            ontology_ents=[
                {
                    "ent_id": _["ent_id"],
                    "ent_term": _["ent_term"],
                }
                for _ in subject_efo_ents
            ],
            pred_term=pred_term,
            num_similarity_candidates=params.NUM_SIMILARITY_CANDIDATES_TRAIT,
            similarity_score_threshold=params.SIM_THRESHOLD_TRAIT,
            verbose=False,
        )
        subject_trait_ents = phenotype_ent_harmonizer.ents_df
        # objects
        phenotype_ent_harmonizer.reset()
        phenotype_ent_harmonizer.harmonize(
            ontology_ents=[
                {
                    "ent_id": _["ent_id"],
                    "ent_term": _["ent_term"],
                }
                for _ in object_efo_ents
            ],
            pred_term=pred_term,
            num_similarity_candidates=params.NUM_SIMILARITY_CANDIDATES_TRAIT,
            similarity_score_threshold=params.SIM_THRESHOLD_TRAIT,
            verbose=False,
        )
        object_trait_ents = phenotype_ent_harmonizer.ents_df
        # finalize
        valid = (
            subject_trait_ents is not None
            and len(subject_trait_ents) > 0
            and object_trait_ents is not None
            and len(object_trait_ents) > 0
        )
        if not valid:
            return None
        res = {
            "triple_text": triple_text,
            "subject_ents": subject_trait_ents.to_dict(orient="records"),
            "object_ents": object_trait_ents.to_dict(orient="records"),
        }
        return res
    except Exception as e:
        logger.warning(f"Error, {doi=}, {triple_text=}; {e}")
        return None


@ray.remote
def make_efo_ents(
    idx: int,
    total: int,
    doi: str,
    triples: List[Dict],
    params: Params,
) -> Optional[Dict]:
    if idx % ECHO_STEP == 0:
        logger.info(f"#{idx}/{total}, {doi=}")
    # This is to clean out ents with same terms but different ids
    triples_clean = (
        pd.DataFrame(
            [
                {
                    "subject_term": _["sub_term"],
                    "object_term": _["obj_term"],
                    "context_text": _["text"],
                    "triple_text": _["triple_text"],
                    "pred_term": _["pred"],
                    "triple_data": _,
                }
                for _ in triples
            ]
        )
        .drop_duplicates(
            subset=[
                "subject_term",
                "object_term",
                "context_text",
                "triple_text",
                "pred_term",
            ]
        )
        .to_dict(orient="records")
    )
    ents = [
        _make_efo_ents(
            doi=doi,
            subject_term=_["subject_term"],
            object_term=_["object_term"],
            triple_text=_["triple_text"],
            context_text=_["context_text"],
            pred_term=_["pred_term"],
            triple_data=_["triple_data"],
            params=params,
        )
        for _ in triples_clean
    ]
    ents = [_ for _ in ents if _ is not None]
    if len(ents) == 0:
        return None
    else:
        res = {
            "doi": doi,
            "ents": ents,
        }
        return res


@ray.remote
def make_umls_ents(
    idx: int,
    total: int,
    doi: str,
    ents_data: List[Dict],
    params: Params,
) -> Optional[Dict]:
    if idx % ECHO_STEP == 0:
        logger.info(f"#{idx}/{total}, {doi=}")
    # there are cases where doi-triple is duplicated due to
    # same triple generated from multiple context text
    ents_data_unique = (
        pd.DataFrame(
            [
                {
                    "triple_text": _["triple_text"],
                    "query_subject_term": _["query_subject_term"],
                    "query_object_term": _["query_object_term"],
                    "subject_ents": _["subject_ents"],
                    "object_ents": _["object_ents"],
                }
                for _ in ents_data
            ]
        )
        .drop_duplicates(subset=["triple_text"])
        .to_dict(orient="records")
    )
    ents_results = [
        _make_umls_ents(
            doi=doi,
            triple_text=_["triple_text"],
            query_subject_term=_["query_subject_term"],
            query_object_term=_["query_object_term"],
            subject_efo_ents=_["subject_ents"],
            object_efo_ents=_["object_ents"],
            params=params,
        )
        for _ in ents_data_unique
    ]
    ents_results = [_ for _ in ents_results if _ is not None]
    res = {
        "doi": doi,
        "ents": ents_results,
    }
    return res


@ray.remote
def make_trait_ents(
    idx: int,
    total: int,
    doi: str,
    ents_data: List[Dict],
    params: Params,
) -> Optional[Dict]:
    if idx % ECHO_STEP == 0:
        logger.info(f"#{idx}/{total}, {doi=}")
    # there are cases where doi-triple is duplicated due to
    # same triple generated from multiple context text
    ents_data_unique = (
        pd.DataFrame(
            [
                {
                    "triple_text": _["triple_text"],
                    "query_subject_term": _["query_subject_term"],
                    "query_object_term": _["query_object_term"],
                    "subject_ents": _["subject_ents"],
                    "object_ents": _["object_ents"],
                    "pred_term": _["pred_term"],
                }
                for _ in ents_data
            ]
        )
        .drop_duplicates(subset=["triple_text"])
        .to_dict(orient="records")
    )
    ents_results = [
        _make_trait_ents(
            doi=doi,
            triple_text=_["triple_text"],
            subject_efo_ents=_["subject_ents"],
            object_efo_ents=_["object_ents"],
            pred_term=_["pred_term"],
            params=params,
        )
        for _ in ents_data_unique
    ]
    ents_results = [_ for _ in ents_results if _ is not None]
    if len(ents_results) == 0:
        return None
    res = {
        "doi": doi,
        "ents": ents_results,
    }
    return res


class MakeEntsFlow(FlowSpec):

    INTERVAL = Parameter(
        "interval",
        help="period interval",
        default="2020-10-01/2020-10-31",
    )
    PROFILE = Parameter(
        "profile",
        help="profile",
        default="default",
    )
    OVERWRITE = Parameter(
        "overwrite",
        help="overwrite",
        is_flag=True,
    )
    NUM_WORKERS = Parameter(
        "num_workers",
        help="Number of cpu workers",
        default=4,
    )

    @step
    def start(self):
        self.interval_str = interval_str(self.INTERVAL)
        self.data_dir = DATA_ROOT / "medrxiv_experiments" / self.interval_str
        profile_dir = self.data_dir / self.PROFILE
        if self.PROFILE == "default":
            profile_dir.mkdir(parents=True, exist_ok=True)
            self.params = params
        else:
            profile_params_file = profile_dir / "params.json"
            if not profile_params_file.exists():
                sys.exit(f"File {profile_params_file} does not exist.")
            else:
                with profile_params_file.open() as f:
                    profile_params = json.load(f)
                    self.params = Params(**profile_params)
        self.output_dir = profile_dir / "ents"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        logger.info(
            f"""Params
        {self.INTERVAL=}
        {self.OVERWRITE=}
        {self.data_dir=}
        {self.output_dir=}
        {self.params}
        """
        )
        self.next(self.setup)

    @step
    def setup(self):
        ray.init(num_cpus=self.NUM_WORKERS)
        self.next(self.make_efo_ents)

    @step
    def make_efo_ents(self):
        self.efo_out_file = self.output_dir / "efo_ents.json"
        if self.OVERWRITE or not self.efo_out_file.exists():
            triples_file = self.data_dir / "triples.json"
            assert triples_file.exists()
            with triples_file.open("r") as f:
                triples = json.load(f)
            efo_ents_futures = [
                make_efo_ents.remote(
                    idx=idx,
                    total=len(triples),
                    doi=_["doi"],
                    triples=_["triples"],
                    params=self.params,
                )
                for idx, _ in enumerate(triples)
                if len(_["triples"]) > 0
            ]
            self.efo_ents = [
                _ for _ in ray.get(efo_ents_futures) if _ is not None
            ]
            with self.efo_out_file.open("w") as f:
                json.dump(self.efo_ents, f)
        else:
            with self.efo_out_file.open("r") as f:
                self.efo_ents = json.load(f)
        self.next(self.make_umls_ents)  # MAYBE: could branch next steps?

    @step
    def make_umls_ents(self):
        self.umls_out_file = self.output_dir / "umls_ents.json"
        if self.OVERWRITE or not self.umls_out_file.exists():
            umls_ents_futures = [
                make_umls_ents.remote(
                    idx=idx,
                    total=len(self.efo_ents),
                    doi=_["doi"],
                    ents_data=_["ents"],
                    params=self.params,
                )
                for idx, _ in enumerate(self.efo_ents)
            ]
            self.umls_ents = [
                _ for _ in ray.get(umls_ents_futures) if _ is not None
            ]
            with self.umls_out_file.open("w") as f:
                json.dump(self.umls_ents, f)
        else:
            with self.umls_out_file.open("r") as f:
                self.umls_ents = json.load(f)
        self.next(self.make_trait_ents)

    @step
    def make_trait_ents(self):
        self.trait_out_file = self.output_dir / "trait_ents.json"
        if self.OVERWRITE or not self.trait_out_file.exists():
            trait_ents_futures = [
                make_trait_ents.remote(
                    idx=idx,
                    total=len(self.efo_ents),
                    doi=_["doi"],
                    ents_data=_["ents"],
                    params=self.params,
                )
                for idx, _ in enumerate(self.efo_ents)
            ]
            self.trait_ents = [
                _ for _ in ray.get(trait_ents_futures) if _ is not None
            ]
            with self.trait_out_file.open("w") as f:
                json.dump(self.trait_ents, f)
        else:
            with self.trait_out_file.open("r") as f:
                self.trait_ents = json.load(f)
        self.next(self.make_combined)

    @step
    def make_combined(self):
        self.combined_out_file = self.output_dir / "combined_ents.json"
        if self.OVERWRITE or not self.combined_out_file.exists():
            efo_ents_flat = (
                pd.DataFrame(
                    [
                        {
                            "doi": _["doi"],
                            "triple": __["triple_text"],
                            "efo_ents": __,
                        }
                        for _ in self.efo_ents
                        for __ in _["ents"]
                    ]
                )
                .drop_duplicates(subset=["doi", "triple"])
                .reset_index(drop=True)
            )
            umls_ents_flat = pd.DataFrame(
                [
                    {
                        "doi": _["doi"],
                        "triple": __["triple_text"],
                        "umls_ents": __,
                    }
                    for _ in self.umls_ents
                    for __ in _["ents"]
                ]
            )
            trait_ents_flat = pd.DataFrame(
                [
                    {
                        "doi": _["doi"],
                        "triple": __["triple_text"],
                        "trait_ents": __,
                    }
                    for _ in self.trait_ents
                    for __ in _["ents"]
                ]
            )
            self.combined_ents = (
                efo_ents_flat.merge(umls_ents_flat, on=["doi", "triple"])
                .merge(trait_ents_flat, on=["doi", "triple"])
                .reset_index(drop=True)
                .assign(
                    subject_term=lambda df: df["efo_ents"].apply(
                        lambda item: item["query_subject_term"]
                    ),
                    object_term=lambda df: df["efo_ents"].apply(
                        lambda item: item["query_object_term"]
                    ),
                    pred_term=lambda df: df["efo_ents"].apply(
                        lambda item: item["pred_term"]
                    ),
                )
                .to_dict(orient="records")
            )
            with self.combined_out_file.open("w") as f:
                json.dump(self.combined_ents, f)
        else:
            with self.combined_out_file.open("r") as f:
                self.combined_ents = json.load(f)
        print("Length combined ents", len(self.combined_ents))
        self.next(self.summary)

    @step
    def summary(self):
        print("# EFO")
        print("Total num dois with efo ents", len(self.efo_ents))
        efo_doi_triple_pairs = (
            pd.DataFrame(
                [
                    {
                        "doi": _["doi"],
                        "triple": __["triple_text"],
                    }
                    for _ in self.efo_ents
                    for __ in _["ents"]
                ]
            )
            .drop_duplicates()
            .reset_index(drop=True)
        )
        print(
            "Total num unique doi-triple with efo ents",
            len(efo_doi_triple_pairs),
        )
        print("# UMLS")
        print("Total num dois with umls ents", len(self.umls_ents))
        umls_doi_triple_pairs = (
            pd.DataFrame(
                [
                    {
                        "doi": _["doi"],
                        "triple": __["triple_text"],
                    }
                    for _ in self.umls_ents
                    for __ in _["ents"]
                ]
            )
            .drop_duplicates()
            .reset_index(drop=True)
        )
        print(
            "Total num unique doi-triple with umls ents",
            len(umls_doi_triple_pairs),
        )
        print("# Traits")
        print("Total num dois with trait ents", len(self.trait_ents))
        trait_doi_triple_pairs = (
            pd.DataFrame(
                [
                    {
                        "doi": _["doi"],
                        "triple": __["triple_text"],
                    }
                    for _ in self.trait_ents
                    for __ in _["ents"]
                ]
            )
            .drop_duplicates()
            .reset_index(drop=True)
        )
        print(
            "Total num unique doi-triple with trait ents",
            len(trait_doi_triple_pairs),
        )
        print(
            "Total num unique doi-triple intersect of efo, umls, trait",
            len(
                trait_doi_triple_pairs.merge(
                    efo_doi_triple_pairs, on=["doi", "triple"]
                ).merge(umls_doi_triple_pairs, on=["doi", "triple"])
            ),
        )
        self.next(self.end)

    @step
    def end(self):
        "Done."


if __name__ == "__main__":
    MakeEntsFlow()
