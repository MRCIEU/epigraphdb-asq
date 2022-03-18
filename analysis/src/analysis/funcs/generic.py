def interval_str(interval: str) -> str:
    return interval.replace("/", "__")


def format_doi_str(doi: str) -> str:
    doi_str = doi.replace("/", "__")
    return doi_str
