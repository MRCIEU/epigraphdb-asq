from typing import Dict, List, Optional, Union

import pandera as pa
from common_processing.types import Config, semrep_types
from loguru import logger
from pandera.typing import DataFrame
from pydantic import validate_arguments

from . import processing


class ClaimParser:
    @validate_arguments
    def __init__(self, config: Config, verbose: bool = True):
        self.config: Config = config
        self.verbose = verbose
        self._triple_df: Optional[DataFrame[semrep_types.TripleDfFinal]] = None
        self._invalid_triple_df: Optional[
            DataFrame[semrep_types.TripleDfFinal]
        ] = None
        self._triple_df_prefilter: Optional[
            DataFrame[semrep_types.TripleDf]
        ] = None

    @property  # type: ignore
    @pa.check_types
    def triple_df(self) -> Optional[DataFrame[semrep_types.TripleDfFinal]]:
        return self._triple_df

    @property  # type: ignore
    @pa.check_types
    def triple_df_prefilter(
        self,
    ) -> Optional[DataFrame[semrep_types.TripleDf]]:
        return self._triple_df_prefilter

    @property  # type: ignore
    def triple_items(self) -> List[semrep_types.TripleItem]:
        triple_items = (
            self._triple_df.to_dict(orient="records")
            if self._triple_df is not None and len(self._triple_df) > 0
            else []
        )
        return triple_items

    @property  # type: ignore
    def invalid_triple_items(self) -> List[semrep_types.TripleItem]:
        triple_items = (
            self._invalid_triple_df.to_dict(orient="records")
            if self._invalid_triple_df is not None
            and len(self._invalid_triple_df) > 0
            else []
        )
        return triple_items

    @property  # type: ignore
    def html_text(self) -> List[Dict[str, Union[int, str]]]:
        html_text: List[Dict[str, Union[int, str]]] = [
            {"idx": idx, "text": processing.format_ner(_)}
            for idx, _ in enumerate(self.triple_items)
        ]
        return html_text

    @validate_arguments
    def parse_claim(self, claim_text: str):
        if self.verbose:
            logger.info("Generate semrep_raw_results")
        self.claim_text = claim_text
        self.semrep_raw_results = processing.run_semrep(
            text=claim_text, config=self.config
        )
        if self.verbose:
            logger.info("Generate triple_df")
        self._triple_df_prefilter = processing.get_triple_df(
            self.semrep_raw_results
        )
        if len(self._triple_df_prefilter) == 0 and self.verbose:
            logger.warning(
                f"No triples identified, claim text: \n  {claim_text}"
            )
        self._triple_df = (
            processing.filter_preds(self._triple_df_prefilter)
            .reset_index(drop=True)
            .reset_index(drop=False)
            .rename(columns={"index": "idx"})
        )
        if self._triple_df is not None:  # ugly type coercion
            self._invalid_triple_df = (
                self._triple_df_prefilter[
                    ~self._triple_df_prefilter["triple_text"].isin(
                        self._triple_df["triple_text"]
                    )
                ]
                .pipe(processing._invalid_triple_df_p)
                .reset_index(drop=True)
                .reset_index(drop=False)
                .rename(columns={"index": "idx"})
            )
