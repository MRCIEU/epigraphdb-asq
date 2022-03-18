from typing import Dict, List, Optional

import pandas as pd
import pandera as pa
import requests
from loguru import logger
from pandera.typing import DataFrame
from pydash import py_

from ..funcs import ner
from ..resources import epigraphdb, semrep_data_dict
from ..types import Config, semrep_types


def run_semrep(text: str, config: Config) -> List[str]:
    try:
        text = str(text)
        url = config.semrep_api_url
        r = requests.post(
            url=url,
            data=text.encode("utf-8"),
            headers={"Content-Type": "text/plain"},
            # time out in 60s
            timeout=60,
        )
        r.raise_for_status()
        res = r.content.decode().split("\n")
        return res
    except Exception as e:
        logger.warning(f"Error with semrep: {e} text: \n    {text}")
        return []


@pa.check_types
def get_triple_df(
    semrep_raw_results: List[str],
) -> DataFrame[semrep_types.TripleDf]:
    """semrep_raw_results is direct results from semrep_api of a text"""
    sents = []
    sent = []
    for idx, line in enumerate(semrep_raw_results):
        if line != "":
            sent.append(line.strip())
        else:
            sents.append(sent)
            sent = []
    sents = [_ for _ in sents if len(_) > 0]
    sents_triples = [_parse_semrep_sent(_) for _ in sents]
    sents_triples = [_ for _ in sents_triples if _ is not None and len(_) > 0]
    flatten_triples = py_.flatten(sents_triples)
    if len(flatten_triples) > 0:
        df = pd.DataFrame(flatten_triples).assign(
            sub_confidence_score=lambda df: df["sub_confidence_score"].astype(
                int
            ),
            obj_confidence_score=lambda df: df["sub_confidence_score"].astype(
                int
            ),
            triple_text=lambda df: df.apply(
                lambda row: "{subject}:{predicate}:{object}".format(
                    subject=row["sub_term"],
                    predicate=row["pred"],
                    object=row["obj_term"],
                ),
                axis=1,
            ),
        )
        return df
    else:
        example_df = semrep_types.TripleDf.example(size=1)
        empty_df = example_df.iloc[:0, :].copy()
        return empty_df


@pa.check_types
def filter_preds(
    triple_df: DataFrame[semrep_types.TripleDf],
) -> DataFrame[semrep_types.TripleDf]:
    allow_preds = epigraphdb.EPIGRAPHDB_SEMREP_PREDS
    logger.info(f"filter_preds: pre filter len {len(triple_df)}")
    res = triple_df[triple_df["pred"].isin(allow_preds)]

    logger.info(f"filter_preds: post filter len {len(res)}")
    return res


def format_ner(triple_item: semrep_types.TripleItem) -> str:
    sent = triple_item["text"]
    subject_term = "subj: " + triple_item["sub_term"]
    object_term = "obj: " + triple_item["obj_term"]
    predicate_term = "pred: " + triple_item["pred"]
    subject_pos = (triple_item["sub_start_pos"], triple_item["sub_end_pos"])
    object_pos = (triple_item["obj_start_pos"], triple_item["obj_end_pos"])
    predicate_pos = (
        triple_item["pred_start_pos"],
        triple_item["pred_end_pos"],
    )
    res = ner.format_triple_in_sent(
        sent=sent,
        subject_term=subject_term,
        object_term=object_term,
        predicate_term=predicate_term,
        subject_pos=subject_pos,
        object_pos=object_pos,
        predicate_pos=predicate_pos,
    )
    return res


def _get_triple(semrep_item, text_start_pos: int) -> Optional[Dict]:
    fields = semrep_item.split("|")
    cols = semrep_data_dict.relation_output_cols
    res = {col_key: fields[col_idx] for col_key, col_idx in cols.items()}
    res["sub_neg"] = True if res["sub_neg"] == 1 else False
    res["obj_neg"] = True if res["obj_neg"] == 1 else False
    res["pred_neg"] = True if res["pred_neg"] == "negation" else False
    # ensure all records being non empty
    for key, value in res.items():
        if value == "" or value is None:
            return None
    # adjust entity position to sentence level from document level
    pos_fields = [
        "sub_start_pos",
        "sub_end_pos",
        "pred_start_pos",
        "pred_end_pos",
        "obj_start_pos",
        "obj_end_pos",
    ]
    for field in pos_fields:
        res[field] = int(res[field])
        res[field] -= text_start_pos
    return res


def _parse_semrep_sent(sent) -> Optional[List[Dict]]:
    first_line_fields = sent[0].split("|")
    if (
        first_line_fields[semrep_data_dict.common_cols["output_type"]]
        != "text"
    ):
        return None
    orig_text = first_line_fields[semrep_data_dict.text_cols["text_field"]]
    text_dict = {"text": orig_text}
    text_start_pos = int(
        first_line_fields[semrep_data_dict.text_cols["text_start_pos"]]
    )
    # idxs of relation lines
    rel_idxs = []
    for idx, _ in enumerate(sent):
        fields = _.split("|")
        if fields[semrep_data_dict.common_cols["output_type"]] == "relation":
            rel_idxs.append(idx)
    semrep_triples = [
        _get_triple(sent[idx], text_start_pos=text_start_pos)
        for idx in rel_idxs
    ]
    if len(semrep_triples) == 0:
        return None
    # append text to triple dict
    semrep_triples = [
        dict(_, **text_dict) for _ in semrep_triples if _ is not None
    ]
    # NOTE: mypy fails to resolve early None
    return semrep_triples  # type: ignore
