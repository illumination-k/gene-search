import argparse
import pandas as pd
import utils
import json


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", "--input", type=str, default="base_data/Ppatens_152_annotation_info.txt"
    )
    args = parser.parse_args()

    df = pd.read_csv(args.input, sep="\t", header=None)
    df = df[[1, 9]]

    indexs = []
    for _, items in df.iterrows():
        gene_id = items[1].strip()
        go_ids = [v for v in items[9].strip().split(",") if v != ""]

        go_terms = []
        for go_id in go_ids:
            desc = utils.get_godesc(utils.GODAG, go_id)
            go_terms.append({"id": go_id, "description": desc})

        index_header = {"index": {"_index": "gene_ppatents"}}
        index_content = {
            "gene_id": gene_id,
            "gene_names": [],
            "go_term": go_terms,
            "organism": "ppatents",
        }

        indexs.append(json.dumps(index_header))
        indexs.append(json.dumps(index_content))

    indexs.append("")
    with open("data/ppatents_index.json", "w") as w:
        w.write("\n".join(indexs))


if __name__ == "__main__":
    main()
