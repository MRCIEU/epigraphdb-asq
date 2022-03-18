EPIGRAPHDB_SEMREP_PREDS = [
    "ASSOCIATED_WITH",
    "COEXISTS_WITH",
    "INTERACTS_WITH",
    "CAUSES",
    "TREATS",
    "AFFECTS",
]

EPIGRAPHDB_PRED_GROUP = {
    "directional": ["CAUSES", "TREATS", "AFFECTS", "PRODUCES"],
    "undirectional": ["ASSOCIATED_WITH", "COEXISTS_WITH", "INTERACTS_WITH"],
}

PRED_DIRECTIONAL_MAPPING = {
    "ASSOCIATED_WITH": "undirectional",
    "COEXISTS_WITH": "undirectional",
    "INTERACTS_WITH": "undirectional",
    "CAUSES": "directional",
    "TREATS": "directional",
    "AFFECTS": "directional",
    "PRODUCES": "directional",
}

MR_EVE_MR_TEMPLATE = """
    MATCH (source:Gwas)-[r:MR_EVE_MR]-{arrow}(target:Gwas)
    WHERE

        source._id IN [{source_id_list}]
        AND target._id IN [{target_id_list}]
        {pval_clause}
    RETURN
        source._id AS source_id,
        source._name AS source_term,
        target._id AS target_id,
        target._name AS target_term,
        type(r) AS meta_rel,
        r.b AS effect_size,
        r.se AS se,
        r.pval AS pval,
        r AS rel_data
"""


PRS_TEMPLATE = """
    MATCH (source:Gwas)-[r:PRS]-(target:Gwas)
    WHERE
        source._id IN [{source_id_list}]
        AND target._id IN [{target_id_list}]
        {pval_clause}
    RETURN
        source._id AS source_id,
        source._name AS source_term,
        target._id AS target_id,
        target._name AS target_term,
        type(r) AS meta_rel,
        r.beta AS effect_size,
        r.se AS se,
        r.p AS pval,
        r AS rel_data
"""


GEN_COR_TEMPLATE = """
    MATCH (source:Gwas)-[r:GEN_COR]-(target:Gwas)
    WHERE
        source._id IN [{source_id_list}]
        AND target._id IN [{target_id_list}]
        {pval_clause}
    RETURN
        source._id AS source_id,
        source._name AS source_term,
        target._id AS target_id,
        target._name AS target_term,
        type(r) AS meta_rel,
        r.rg AS effect_size,
        r.rg_SE AS se,
        r.p AS pval,
        r AS rel_data
"""

ENT_URL_TEMPLATE = (
    "https://epigraphdb.org/entity?meta_node={meta_ent}&id={ent_id}"
)
META_ENT_URL_TEMPLATE = "https://epigraphdb.org/meta-node/{meta_ent}"
