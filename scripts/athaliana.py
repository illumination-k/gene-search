import pandas as pd
import argparse
import json

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", "--input", type=str, default="base_data/ATH_GO_GOSLIM.txt"
    )
    args = parser.parse_args()

    df = pd.read_csv(args.input, sep="\t", header=None, comment="!")
    print(df.head()[[0, 4, 5]])

    all_gene_ids = set(df[0])
    d = {
        gene_id: {"organism": "athaliana", "gene_names": [], "go_term": []}
        for gene_id in all_gene_ids
    }
    for _, items in df.iterrows():
        gene_id = items[0].strip()
        go_id = items[5].strip()
        go_desc = items[4].strip()
        d[gene_id]["go_term"].append({"id": go_id, "description": go_desc})

    indexs = []
    for k, v in d.items():
        index_header = {"index": {"_index": "gene_mpolymorpha"}}
        index_content = {"gene_id": k}
        index_content.update(v)
        indexs.append(json.dumps(index_header))
        indexs.append(json.dumps(index_content))
    indexs.append("")

    with open("data/athaliana_index.json", "w") as w:
        w.write("\n".join(indexs))


if __name__ == "__main__":
    main()
