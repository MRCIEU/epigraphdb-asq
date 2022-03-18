# col idx are 0-based idx, not 1-based as in semrep's docs

common_cols = {
    "output_type": 5,
}

text_cols = {
    "text_start_pos": 6,
    "text_end_pos": 7,
    "text_field": 8,
}

# this is not in used yet
relation_input_cols = {
    "sub_id": 8,
    "sub_name": 9,
    "sub_type": 11,
    "sub_gene_id": 12,
    "sub_gene_name": 13,
    "pred": 22,
    "obj_id": 28,
    "obj_name": 29,
    "obj_type": 31,
    "obj_gene_id": 32,
    "obj_gene_name": 33,
}

relation_output_cols = {
    # sub
    "sub_id": 8,
    "sub_term": 9,
    "sub_type": 11,
    "sub_text": 14,
    "sub_neg": 17,
    "sub_confidence_score": 18,
    "sub_start_pos": 19,
    "sub_end_pos": 20,
    # pred
    "pred_type": 21,
    "pred": 22,
    "pred_neg": 23,
    "pred_start_pos": 24,
    "pred_end_pos": 25,
    # obj
    "obj_id": 28,
    "obj_term": 29,
    "obj_type": 31,
    "obj_text": 34,
    "obj_neg": 37,
    "obj_confidence_score": 38,
    "obj_start_pos": 39,
    "obj_end_pos": 40,
}
