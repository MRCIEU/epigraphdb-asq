import json
import sys
from typing import Any, Dict, List, Optional

import pandas as pd
import ray
from common_processing import assoc_evidence, scores, triple_evidence
from common_processing.resources import epigraphdb
from common_processing.types import Params
from metaflow import FlowSpec, Parameter, step

from analysis import utils
from analysis.funcs.generic import interval_str
from analysis.settings import config, params

from icecream import ic  # noqa
from loguru import logger  # noqa

DATA_ROOT = utils.find_data_root()
ECHO_STEP = 10


def _make_triple_evidence(
    evidence_type: str,
    subject_ents: List[Dict],
    object_ents: List[Dict],
    pred_term: str,
) -> List[Dict]:
    processor = triple_evidence.TripleEvidenceProcessor(config=config)
    process_status = processor.process(
        evidence_type=evidence_type,
        subject_ents=subject_ents,
        object_ents=object_ents,
        pred_term=pred_term,
    )
    if process_status:
        res = processor.evidence_df.to_dict(orient="records")
    else:
        res = []
    return res


def _make_assoc_evidence(
    evidence_type: str,
    subject_ents: List[Dict],
    object_ents: List[Dict],
    pred_term: str,
    params: Params,
) -> List[Dict]:
    processor = assoc_evidence.AssocEvidenceProcessor(config=config)
    process_status = processor.process(
        evidence_type=evidence_type,
        subject_ents=subject_ents,
        object_ents=object_ents,
        pred_term=pred_term,
        pval_threshold=params.ASSOC_PVAL_THRESHOLD,
    )
    if process_status:
        df = processor.evidence_df.dropna()
        res = df.to_dict(orient="records")
    else:
        res = []
    return res


def _wrap_scored_triple(
    triple_evidence,
    query_subject_term,
    query_object_term,
    ontology_subject_mapping,
    ontology_object_mapping,
    umls_subject_mapping,
    umls_object_mapping,
):
    if len(triple_evidence) == 0:
        return []
    df = pd.DataFrame(triple_evidence).assign(idx=lambda df: range(len(df)))
    res = scores.make_triple_scores(
        triple_evidence=df,
        query_subject_term=query_subject_term,
        query_object_term=query_object_term,
        ontology_subject_mapping=ontology_subject_mapping,
        ontology_object_mapping=ontology_object_mapping,
        umls_subject_mapping=umls_subject_mapping,
        umls_object_mapping=umls_object_mapping,
    ).to_dict(orient="records")
    return res


def _wrap_scored_assoc(
    assoc_evidence,
    query_subject_term,
    query_object_term,
    ontology_subject_mapping,
    ontology_object_mapping,
    trait_subject_mapping,
    trait_object_mapping,
):
    if len(assoc_evidence) == 0:
        return []
    df = pd.DataFrame(assoc_evidence).assign(idx=lambda df: range(len(df)))
    res = scores.make_assoc_scores(
        assoc_evidence=df,
        query_subject_term=query_subject_term,
        query_object_term=query_object_term,
        ontology_subject_mapping=ontology_subject_mapping,
        ontology_object_mapping=ontology_object_mapping,
        trait_subject_mapping=trait_subject_mapping,
        trait_object_mapping=trait_object_mapping,
    ).to_dict(orient="records")
    return res


@ray.remote
def make_assoc_evidence(
    idx: int,
    total: int,
    doi: str,
    data: Dict[str, Any],
    params: Params,
) -> Optional[Dict]:
    if idx % ECHO_STEP == 0:
        logger.info(f"#{idx}/{total}, {doi=}")
    try:
        subject_ents = [
            {"ent_id": _["ent_id"], "ent_term": _["ent_term"]}
            for _ in data["trait_ents"]["subject_ents"]
        ]
        object_ents = [
            {"ent_id": _["ent_id"], "ent_term": _["ent_term"]}
            for _ in data["trait_ents"]["object_ents"]
        ]
        pred_term = data["pred_term"]
        pred_directional_type = epigraphdb.PRED_DIRECTIONAL_MAPPING[pred_term]
        evidence_types = assoc_evidence.EVIDENCE_TYPES[pred_directional_type]
        evidence = {
            _: _make_assoc_evidence(
                evidence_type=_,
                subject_ents=subject_ents,
                object_ents=object_ents,
                pred_term=pred_term,
                params=params,
            )
            for _ in evidence_types
        }
        res = {
            "doi": doi,
            "triple": data["triple"],
            "assoc_evidence": evidence,
        }
        return res
    except Exception as e:
        logger.warning(f"Error, {doi=}; {e}")
        return None


@ray.remote
def make_triple_evidence(
    idx: int,
    total: int,
    doi: str,
    data: Dict[str, Any],
) -> Optional[Dict]:
    if idx % ECHO_STEP == 0:
        logger.info(f"#{idx}/{total}, {doi=}")
    subject_ents = [
        {"ent_id": _["ent_id"], "ent_term": _["ent_term"]}
        for _ in data["umls_ents"]["subject_ents"]
    ]
    object_ents = [
        {"ent_id": _["ent_id"], "ent_term": _["ent_term"]}
        for _ in data["umls_ents"]["object_ents"]
    ]
    pred_term = data["pred_term"]
    pred_directional_type = epigraphdb.PRED_DIRECTIONAL_MAPPING[pred_term]
    evidence_types = triple_evidence.EVIDENCE_TYPES[pred_directional_type]
    evidence = {
        _: _make_triple_evidence(
            evidence_type=_,
            subject_ents=subject_ents,
            object_ents=object_ents,
            pred_term=pred_term,
        )
        for _ in evidence_types
    }
    res = {
        "doi": doi,
        "triple": data["triple"],
        "triple_evidence": evidence,
    }
    return res


@ray.remote
def make_combined_score(
    idx: int,
    total: int,
    doi: str,
    data: Dict[str, Any],
) -> Optional[Dict]:
    if idx % ECHO_STEP == 0:
        logger.info(f"#{idx}/{total}, {doi=}")

    ontology_subject_mapping = pd.DataFrame(data["efo_ents"]["subject_ents"])
    ontology_object_mapping = pd.DataFrame(data["efo_ents"]["object_ents"])
    umls_subject_mapping = pd.DataFrame(data["umls_ents"]["subject_ents"])
    umls_object_mapping = pd.DataFrame(data["umls_ents"]["object_ents"])
    trait_subject_mapping = pd.DataFrame(data["trait_ents"]["subject_ents"])
    trait_object_mapping = pd.DataFrame(data["trait_ents"]["object_ents"])
    pred_term = data["pred_term"]
    pred_directional_type = epigraphdb.PRED_DIRECTIONAL_MAPPING[pred_term]
    assoc_evidence_types = assoc_evidence.EVIDENCE_TYPES[pred_directional_type]
    triple_evidence_types = triple_evidence.EVIDENCE_TYPES[
        pred_directional_type
    ]
    try:
        scored_triple_evidence = {
            _: _wrap_scored_triple(
                triple_evidence=data["triple_evidence"][_],
                query_subject_term=data["subject_term"],
                query_object_term=data["object_term"],
                ontology_subject_mapping=ontology_subject_mapping,
                ontology_object_mapping=ontology_object_mapping,
                umls_subject_mapping=umls_subject_mapping,
                umls_object_mapping=umls_object_mapping,
            )
            for _ in triple_evidence_types
        }
        scored_assoc_evidence = {
            _: _wrap_scored_assoc(
                assoc_evidence=data["assoc_evidence"][_],
                query_subject_term=data["subject_term"],
                query_object_term=data["object_term"],
                ontology_subject_mapping=ontology_subject_mapping,
                ontology_object_mapping=ontology_object_mapping,
                trait_subject_mapping=trait_subject_mapping,
                trait_object_mapping=trait_object_mapping,
            )
            for _ in assoc_evidence_types
        }
    except Exception as e:
        logger.warning(f"Error, {idx=}, {doi=}; {e}")
        return None
    res = {
        "doi": data["doi"],
        "triple": data["triple"],
        "efo_ents": data["efo_ents"],
        "umls_ents": data["umls_ents"],
        "trait_ents": data["trait_ents"],
        "subject_term": data["subject_term"],
        "object_term": data["object_term"],
        "pred_term": data["pred_term"],
        "triple_evidence": scored_triple_evidence,
        "assoc_evidence": scored_assoc_evidence,
    }
    return res


class MakeEvidenceFlow(FlowSpec):

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
    LITE = Parameter(
        "lite",
        help="lite",
        is_flag=True,
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
        lite_str = "_lite" if self.LITE else ""
        self.output_dir = profile_dir / f"evidence{lite_str}"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        logger.info(
            f"""Params
        {self.INTERVAL=}
        {self.OVERWRITE=}
        {self.LITE=}
        {self.data_dir=}
        {self.output_dir=}
        """
        )
        self.next(self.setup)

    @step
    def setup(self):
        combined_ents_file = (
            self.data_dir / self.PROFILE / "ents" / "combined_ents.json"
        )
        assert combined_ents_file.exists()
        with combined_ents_file.open("r") as f:
            self.combined_ents = json.load(f)
        if self.LITE:
            self.combined_ents = self.combined_ents[:10]
        print("Len combined ents", len(self.combined_ents))

        ray.init(num_cpus=self.NUM_WORKERS)
        self.next(self.make_triple_evidence)

    @step
    def make_triple_evidence(self):
        self.triple_evidence_file = self.output_dir / "triple_evidence.json"
        if self.OVERWRITE or not self.triple_evidence_file.exists():
            triple_evidence_futures = [
                make_triple_evidence.remote(
                    idx=idx,
                    total=len(self.combined_ents),
                    doi=_["doi"],
                    data=_,
                )
                for idx, _ in enumerate(self.combined_ents)
            ]
            self.triple_evidence = [
                _ for _ in ray.get(triple_evidence_futures) if _ is not None
            ]
            with self.triple_evidence_file.open("w") as f:
                json.dump(self.triple_evidence, f)
        else:
            with self.triple_evidence_file.open("r") as f:
                self.triple_evidence = json.load(f)
        self.next(self.make_assoc_evidence)

    @step
    def make_assoc_evidence(self):
        self.assoc_evidence_file = self.output_dir / "assoc_evidence.json"
        if self.OVERWRITE or not self.assoc_evidence_file.exists():
            assoc_evidence_futures = [
                make_assoc_evidence.remote(
                    idx=idx,
                    total=len(self.combined_ents),
                    doi=_["doi"],
                    data=_,
                    params=self.params,
                )
                for idx, _ in enumerate(self.combined_ents)
            ]
            self.assoc_evidence = [
                _ for _ in ray.get(assoc_evidence_futures) if _ is not None
            ]
            with self.assoc_evidence_file.open("w") as f:
                json.dump(self.assoc_evidence, f)
        else:
            with self.assoc_evidence_file.open("r") as f:
                self.assoc_evidence = json.load(f)
        self.next(self.combine)

    @step
    def combine(self):
        self.combined_evidence_file = (
            self.output_dir / "combined_evidence.json"
        )
        if self.OVERWRITE or not self.combined_evidence_file.exists():
            self.combined_evidence = (
                pd.DataFrame(self.combined_ents)
                .merge(
                    pd.DataFrame(self.triple_evidence), on=["doi", "triple"]
                )
                .merge(pd.DataFrame(self.assoc_evidence), on=["doi", "triple"])
                .reset_index(drop=True)
            )
            with self.combined_evidence_file.open("w") as f:
                json.dump(self.combined_evidence.to_dict(orient="records"), f)
        else:
            with self.combined_evidence_file.open("r") as f:
                self.combined_evidence = pd.DataFrame(json.load(f))
        self.next(self.combine_score)

    @step
    def combine_score(self):
        self.combined_score_file = self.output_dir / "combined_score.json"
        if self.OVERWRITE or not self.combined_score_file.exists():
            combined_score_futures = [
                make_combined_score.remote(
                    idx=idx,
                    total=len(self.combined_evidence),
                    doi=_["doi"],
                    data=_,
                )
                for idx, _ in enumerate(
                    self.combined_evidence.to_dict(orient="records")
                )
            ]
            self.combined_score = pd.DataFrame(
                [_ for _ in ray.get(combined_score_futures) if _ is not None]
            )
            with self.combined_score_file.open("w") as f:
                json.dump(self.combined_score.to_dict(orient="records"), f)
        else:
            with self.combined_score_file.open() as f:
                self.combined_score = pd.DataFrame(json.load(f))
        self.next(self.summary_echo)

    @step
    def summary_echo(self):
        print("# Simple len counts")
        print("Len doi-triples pre-evidence", len(self.combined_ents))
        print(
            "Len doi-triples with triple evidence", len(self.triple_evidence)
        )
        print("Len doi-triples with assoc evidence", len(self.assoc_evidence))
        print(
            "Len doi-triples intersect assoc, triple evidence",
            len(self.combined_evidence),
        )
        self.next(self.summary_artifacts)

    @step
    def summary_artifacts(self):
        for (
            pred_group_key,
            pred_group_value,
        ) in epigraphdb.EPIGRAPHDB_PRED_GROUP.items():
            output_file = (
                self.output_dir
                / f"evidence_count_summary_{pred_group_key}.csv"
            )
            summary_df = self.combined_evidence[
                self.combined_evidence["pred_term"].isin(pred_group_value)
            ].assign(
                num_efo_ents_subj=lambda df: df["efo_ents"].apply(
                    lambda x: len(x["subject_ents"])
                ),
                num_efo_ents_obj=lambda df: df["efo_ents"].apply(
                    lambda x: len(x["object_ents"])
                ),
                num_umls_ents_subj=lambda df: df["umls_ents"].apply(
                    lambda x: len(x["subject_ents"])
                ),
                num_umls_ents_obj=lambda df: df["umls_ents"].apply(
                    lambda x: len(x["object_ents"])
                ),
                num_trait_ents_subj=lambda df: df["trait_ents"].apply(
                    lambda x: len(x["subject_ents"])
                ),
                num_trait_ents_obj=lambda df: df["trait_ents"].apply(
                    lambda x: len(x["object_ents"])
                ),
            )[
                [
                    "doi",
                    "triple",
                    "subject_term",
                    "pred_term",
                    "object_term",
                    "num_efo_ents_subj",
                    "num_efo_ents_obj",
                    "num_umls_ents_subj",
                    "num_umls_ents_obj",
                    "num_trait_ents_subj",
                    "num_trait_ents_obj",
                ]
            ]
            count_df = pd.json_normalize(
                [
                    {
                        "doi": _["doi"],
                        "triple": _["triple"],
                        "triple_evidence": {
                            k: len(v) for k, v in _["triple_evidence"].items()
                        },
                        "assoc_evidence": {
                            k: len(v) for k, v in _["assoc_evidence"].items()
                        },
                    }
                    for _ in self.combined_evidence.to_dict(orient="records")
                ]
            ).fillna(0)
            summary_df = summary_df.merge(count_df, on=["doi", "triple"])
            logger.info(f"Write summary file to {output_file}")
            summary_df.to_csv(output_file, index=False)
        self.next(self.end)

    @step
    def end(self):
        pass


if __name__ == "__main__":
    MakeEvidenceFlow()
