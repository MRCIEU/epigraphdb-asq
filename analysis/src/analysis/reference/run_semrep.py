# import datetime
# import multiprocessing
# import os

# import pandas as pd
# import requests
# from loguru import logger

# OUTDIR = "output"
# BIO_DATA = os.path.join(OUTDIR, "biorxiv_data.csv.gz")
# MED_DATA = os.path.join(OUTDIR, "medrxiv_data.csv.gz")
# GENERIC_CONCEPT_FILE = "semmedVER43_2021_R_GENERIC_CONCEPT.csv.gz"

# DATE = datetime.datetime.now().strftime("%Y-%m-%d")

# THREADS = 40

# if not os.path.exists(OUTDIR):
#     os.makedirs(os.path.join(OUTDIR, "semrep"))


# def read_arxiv_dump(data_dump):
#     d = data_dump
#     df = []
#     if os.path.exists(d):
#         df = pd.read_csv(d)
#     return df


# def get_all_arxiv_data(data_dump, arxiv_name):
#     # read existing
#     logger.info("Reading {}", data_dump)
#     start_num = 0
#     df = read_arxiv_dump(data_dump)
#     if isinstance(df, pd.DataFrame):
#         pub_data = list(df.T.to_dict().values())
#     else:
#         pub_data = []
#     start_num = len(pub_data)
#     logger.info("Aleady done {}", start_num)

#     # takes ~5 minutes for 10,000 records
#     logger.info("Getting total")
#     url = (
#         f"https://api.biorxiv.org/details/{arxiv_name}/2010-08-21/2021-08-28/"
#     )
#     logger.info(url)
#     # get the total number
#     r = requests.get(url + "0")
#     data = r.json()
#     total = data["messages"][0]["total"] + 1
#     # total=200
#     logger.info("Total: {}", total)

#     # loop through all records
#     # for i in range(start_num,total+1,100):
#     for i in range(start_num, total, 100):
#         logger.info("### {} ###", i)
#         url_start = f"{url}{i}"
#         logger.info(url_start)
#         res = requests.get(url_start)
#         data = res.json()
#         for d in data:
#             if d == "collection":
#                 for r in data[d]:
#                     # deal with newlines
#                     r2 = {x: r[x].replace("\n", " ") for x in r}
#                     pub_data.append(r2)
#         # not ideal, but to avoid issues with losing connection, dump to CSV repeatedly
#         if i % 10000 == 0:
#             df = pd.DataFrame(pub_data)
#             logger.info(df.shape)
#             df.to_csv(data_dump, index=False, compression="gzip")

#     df = pd.DataFrame(pub_data)
#     logger.info(df.shape)

#     df.drop_duplicates(inplace=True)
#     logger.info(df.shape)
#     # deal with new lines
#     df = df.replace(r"\\n", " ", regex=True)
#     df.to_csv(data_dump, index=False, compression="gzip")


# def run_semrep(text):
#     try:
#         if type(text) == str:
#             url = "http://ieu-db-interface.epi.bris.ac.uk:8067"
#             response = requests.post(
#                 url=url,
#                 data=text.encode("utf-8"),
#                 # data=text,
#                 headers={"Content-Type": "text/plain"},
#             )
#             # print(response.content)
#             return response.content.decode().split("\n")
#         else:
#             logger.info("Bad format {}", text)
#             return []
#     except:
#         print("Semrep API problem!")
#         return []


# def process_semrep(text, row_id, doi, section, arxiv_name):
#     doi_edit = doi.replace("/", "_")
#     outFile = os.path.join(
#         OUTDIR,
#         "semrep",
#         arxiv_name + "_" + str(doi_edit) + "_" + section + "_semrep.txt",
#     )
#     if not os.path.exists(outFile):
#         res = run_semrep(text)
#         negation_col = 23
#         keep_cols = {
#             "sub_id": 8,
#             "sub_name": 9,
#             "sub_type": 11,
#             "sub_gene_id": 12,
#             "sub_gene_name": 13,
#             "pred": 22,
#             "obj_id": 28,
#             "obj_name": 29,
#             "obj_type": 31,
#             "obj_gene_id": 32,
#             "obj_gene_name": 33,
#         }

#         indices_to_access = list(keep_cols.values())
#         d = []
#         for i in res:
#             if len(i) > 0:
#                 l = i.split("|")
#                 if len(l) > 5 and l[5] == "relation":
#                     sem_series = pd.Series(l)
#                     accessed_series = sem_series[indices_to_access]
#                     accessed_list = list(accessed_series)
#                     dictionary = dict(zip(keep_cols.keys(), accessed_list))
#                     dictionary.update({"doi": doi, "section": section})
#                     # deal with negation
#                     if l[negation_col] != "":
#                         dictionary["pred"] = "NEG_" + dictionary["pred"]
#                         # logger.debug(dictionary['pred']+'\n'+str(l))
#                     d.append(dictionary)
#         semrep_arxiv_df = pd.DataFrame(d)
#         semrep_arxiv_df.to_csv(outFile, index=False, header=False)


# def parallel_semrep(arxiv_name, data_dump):
#     logger.info("Running SemRep with {} threads", THREADS)
#     df = read_arxiv_dump(data_dump)
#     # only want most recent version of each
#     # sort by data desc
#     df = df.sort_values(by="date", ascending=False)
#     # get top one for each doi
#     df = df.groupby("doi").head(1)
#     logger.info(df.shape)
#     logger.info(df.head())
#     pool = multiprocessing.Pool(THREADS)

#     title_list = ["title"] * df.shape[0]
#     abstract_list = ["abstract"] * df.shape[0]
#     arxiv_name_list = [arxiv_name] * df.shape[0]

#     logger.info("Titles...")
#     pool.starmap(
#         process_semrep,
#         zip(df["title"], df.index, df["doi"], title_list, arxiv_name_list),
#     )
#     logger.info("Abstracts...")
#     pool.starmap(
#         process_semrep,
#         zip(
#             df["abstract"], df.index, df["doi"], abstract_list, arxiv_name_list
#         ),
#     )


# def create_final(arxiv_name):
#     com = f"find {OUTDIR}/semrep/ -name '{arxiv_name}_*.txt' | xargs cat | sort | uniq | gzip > {OUTDIR}/{arxiv_name}_{DATE}_semrep.csv.gz"
#     logger.info(com)
#     os.system(com)


# def filter_final(arxiv_name):
#     # applying same filters as MELODI Presto
#     predIgnore = [
#         "PART_OF",
#         "ISA",
#         "LOCATION_OF",
#         "PROCESS_OF",
#         "ADMINISTERED_TO",
#         "METHOD_OF",
#         "USES",
#         "compared_with",
#     ]
#     # typeFilterList = ["aapp","dsyn","enzy","gngm","chem","clnd","horm","hops","inch","orch"]
#     typeFilterList = [
#         "aapp",
#         "clnd",
#         "clna",
#         "dsyn",
#         "enzy",
#         "gngm",
#         "chem",
#         "clnd",
#         "horm",
#         "hops",
#         "inch",
#         "orch",
#         "phsu",
#     ]

#     # load predicate data
#     logger.info("loading data...")
#     PRED_FILE = f"{OUTDIR}/{arxiv_name}_{DATE}_semrep.csv.gz"
#     df = pd.read_csv(PRED_FILE, sep=",")
#     col_names = [
#         "sub_id",
#         "sub_name",
#         "sub_type",
#         "sub_gene_id",
#         "sub_gene_name",
#         "pred",
#         "obj_id",
#         "obj_name",
#         "obj_type",
#         "obj_gene_id",
#         "obj_gene_name",
#         "doi",
#         "section",
#     ]

#     df.columns = col_names
#     logger.info(df.shape)
#     # filter on predicates
#     df = df[~df.pred.isin(predIgnore)]
#     logger.info(df.shape)

#     # filter on generic concepts
#     gc_df = pd.read_csv(
#         GENERIC_CONCEPT_FILE, names=["concept_id", "cui", "name"]
#     )
#     gc_ids = list(gc_df["cui"])
#     df = df[~(df["sub_id"].isin(gc_ids)) & ~(df["obj_id"].isin(gc_ids))]
#     logger.info(df.shape)

#     # filter on types
#     # df = df[df.sub_type.isin(typeFilterList)]
#     # df = df[df.obj_type.isin(typeFilterList)]
#     # logger.info(df.shape)

#     df.to_csv(
#         f"{OUTDIR}/{arxiv_name}_{DATE}_semrep_filter.csv.gz",
#         compression="gzip",
#         index=False,
#     )


# def run(arxiv_name, data_dump):
#     # get_all_arxiv_data(data_dump=data_dump,arxiv_name=arxiv_name)
#     # parallel_semrep(data_dump=data_dump,arxiv_name=arxiv_name)
#     # create_final(arxiv_name=arxiv_name)
#     filter_final(arxiv_name=arxiv_name)


# if __name__ == "__main__":
#     run("biorxiv", BIO_DATA)
#     run("medrxiv", MED_DATA)
