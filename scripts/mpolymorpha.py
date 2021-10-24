import io
import os
import json
import argparse
import requests
import pandas as pd

from typing import List, Dict, Optional

HEADERS = {"Content-type": "application/json"}


def get_gene_corresponding_table() -> pd.DataFrame:
    url = (
        "https://marchantia.info/download/MpTak_v6.1/gene_correspondence_MpTak_v6.1.tsv"
    )
    r = requests.get(url)
    df: pd.DataFrame = pd.read_csv(io.BytesIO(r.content), sep="\t").dropna()

    return df


def get_all_gene_ids() -> List:
    df = get_gene_corresponding_table()
    df = df[(df["locus_type"] == "mRNA") & (df["MpTak_v6.1"] != "-")]

    return list(df["MpTak_v6.1"].drop_duplicates())


def get_annotations(
    url: str, all_gene_ids: List[str], genome_version: str = "MpTak_v6.1"
) -> Dict:

    query = json.dumps(
        {
            "genome": genome_version,
            "dbtypes": ["KOG", "KEGG", "Pfam", "GO"],
            "query": all_gene_ids,
        }
    )

    req = requests.post(url, query, headers=HEADERS)

    return req.json()


def get_nomenclature(url: str) -> List:
    req = requests.post(url, headers=HEADERS)
    return req.json()


def load_annotaions(
    path: Optional[str] = None, all_gene_ids: Optional[List[str]] = None
) -> Dict:
    if path is None:
        annotations_api = "https://marchantia.info/api/annotations/"
        print("annotation api:", annotations_api)
        annotations = get_annotations(annotations_api, all_gene_ids)
        with open("annotation.json", "w") as w:
            json.dump(annotations, w)

        return annotations
    else:
        with open(path) as f:
            annotations = json.load(f)

        return annotations


def load_nomenclatures(path: Optional[str] = None) -> List:
    if path is None:
        nomenclatures_api = "https://marchantia.info/api/nomenclatures/"
        print("nomenclatures api:", nomenclatures_api)
        nomenclatures = get_nomenclature(nomenclatures_api)
        with open("nomenclatures.json", "w") as w:
            json.dump(nomenclatures, w)

        return nomenclatures
    else:
        with open(path) as f:
            nomenclatures = json.load(f)
        return nomenclatures


def create_bulk_indexs(
    path: Optional[str],
    all_gene_ids: List[str],
    annotations: Dict[str, Dict],
    nomenclatures: List,
):
    indexs = []
    all_gene_id_set = set(all_gene_ids)
    d = {
        gene_id: {"organism": "Marchantia polymorpha", "gene_names": [], "go_term": []}
        for gene_id in all_gene_ids
    }
    # annotationからGO Term
    for gene_id, annos in annotations.items():
        if "GO" not in annos.keys():
            continue
        go_annos = annos["GO"]

        for anno in go_annos:
            go_anno = {"id": anno["id"], "description": anno["description"]}
            d[gene_id]["go_term"].append(go_anno)

    # nomenclatureからgene names
    for n in nomenclatures:
        gene_id = n[0]
        gene_name = n[2]
        if gene_id not in all_gene_id_set:
            continue

        d[gene_id]["gene_names"].append(gene_name)

    for k, v in d.items():
        index_header = {"index": {"_index": "gene_mpolymorpha"}}
        index_content = {"gene_id": k}
        index_content.update(v)
        indexs.append(json.dumps(index_header))
        indexs.append(json.dumps(index_content))
    indexs.append("")
    if path is None:
        path = "data/marchantia_index.json"

    with open(path, "w") as w:
        w.write("\n".join(indexs))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--use-api", action="store_true")
    parser.add_argument("--annotation", default="data/annotation.json", type=str)
    parser.add_argument("--nomenclature", default="data/nomenclatures.json", type=str)
    args = parser.parse_args()
    all_gene_ids = get_all_gene_ids()

    if args.use_api:
        annotations = load_annotaions(all_gene_ids=all_gene_ids)
        nomenclatures = load_nomenclatures()
    else:
        annotations = load_annotaions(args.annotation)
        nomenclatures = load_nomenclatures(args.nomenclature)

    create_bulk_indexs(
        path=None,
        all_gene_ids=all_gene_ids,
        annotations=annotations,
        nomenclatures=nomenclatures,
    )


if __name__ == "__main__":
    main()
