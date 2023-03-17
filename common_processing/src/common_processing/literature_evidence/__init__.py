from typing import List, Optional

import pandera as pa
from loguru import logger
from pandera.typing import DataFrame
from pydantic import validate_arguments

from ..settings import params
from ..types import Config, literature_types
from . import processing


class LiteratureLiteEvidenceProcessor:
    @validate_arguments
    def __init__(self, config: Config):
        self.config = config
        self.reset()

    def reset(self):
        self._evidence_df: Optional[
            DataFrame[literature_types.LiteratureLiteEvidenceDf]
        ] = None

    @property  # type: ignore
    @pa.check_types
    def evidence_df(
        self,
    ) -> Optional[DataFrame[literature_types.LiteratureLiteEvidenceDf]]:
        return self._evidence_df

    def process(self, triples: List[literature_types.TripleItem]) -> bool:

        if len(triples) == 0:
            logger.debug("Empty triple items")
            empty_df = (
                literature_types.LiteratureLiteEvidenceDf.example(size=1)
                .iloc[:0, :]
                .copy()
            )
            self._evidence_df = empty_df
            return False

        self._literature_info_df = processing.get_literature_info_df(
            triple_items=triples, config=self.config
        )

        self._pubmed_df = processing.make_pubmed_df(
            literature_df=self._literature_info_df,
            num_items_per_triple=None,
        )
        if len(self._pubmed_df) == 0:
            logger.debug(f"empty pubmed_df {triples=}")
            empty_df = (
                literature_types.LiteratureLiteEvidenceDf.example(size=1)
                .iloc[:0, :]
                .copy()
            )
            self._evidence_df = empty_df
            return False
        else:
            self._evidence_df = self._pubmed_df
            return True


class LiteratureEvidenceProcessor:
    @validate_arguments
    def __init__(self, config: Config):
        self.config = config
        self.reset()

    def reset(self):
        self._evidence_df: Optional[
            DataFrame[literature_types.LiteratureEvidenceDf]
        ] = None

    @property  # type: ignore
    @pa.check_types
    def evidence_df(
        self,
    ) -> Optional[DataFrame[literature_types.LiteratureEvidenceDf]]:
        return self._evidence_df

    def process(
        self,
        triples: List[literature_types.TripleItem],
        num_items_per_triple: int = params.NUM_LITERATURE_ITEMS_PER_TRIPLE,
    ) -> bool:
        # NOTE: for now don't attempt that series of try except yet

        if len(triples) == 0:
            logger.debug("Empty triple items")
            empty_df = (
                literature_types.LiteratureEvidenceDf.example(size=1)
                .iloc[:0, :]
                .copy()
            )
            self._evidence_df = empty_df
            return False

        # step: get SEMMEDDB_TO_LIT links to literature nodes from triples
        self._literature_info_df = processing.get_literature_info_df(
            triple_items=triples, config=self.config
        )

        # step: intermediate pubmed_df linking pubmed id and triple id
        self._pubmed_df = processing.make_pubmed_df(
            literature_df=self._literature_info_df,
            num_items_per_triple=num_items_per_triple,
        )
        if len(self._pubmed_df) == 0:
            logger.debug(f"empty pubmed_df {triples=}")
            empty_df = (
                literature_types.LiteratureEvidenceDf.example(size=1)
                .iloc[:0, :]
                .copy()
            )
            self._evidence_df = empty_df
            return False
        # step: get sentence mentioning the triple
        self._sentence_df = processing.get_sentence_df(
            pubmed_df=self._pubmed_df, config=self.config
        )

        # step: get fulltext (abstract) involving the sentence
        self._fulltext_df = processing.get_fulltext_df(
            sentence_df=self._sentence_df, config=self.config
        )

        # step: combine together
        self._evidence_df = processing.make_literature_evidence_df(
            pubmed_df=self._pubmed_df,
            sentence_df=self._sentence_df,
            fulltext_df=self._fulltext_df,
        )
        return True
