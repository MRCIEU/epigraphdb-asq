from common_processing.funcs.component_query import medline_query

from app.settings import config

PMIDS = [
    "21782230",
    "30516548",
    "24300417",
    "31516639",
    "31703832",
    "25405952",
    "24142648",
]


def test_get_fulltext_df():
    res = medline_query(lit_id_list=PMIDS, url=config.medline_api_url)
    assert res is not None
    print(len(res))
    print(res.to_dict(orient="records")[0])
    assert len(res) > 0
