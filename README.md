# いい感じに複数生物種の遺伝子を検索できるサービス

## Elasticsearch

### index_template

```bash
curl -s -H "Content-Type: application/x-ndjson" -XPOST localhost:9200/_template/gene_basic --data-binary @index_template/gene_basic.json
```

### 2. _bulk

`scripts`配下にある`${organism}.py`を使用すると`data`配下に`${organism}_index.json`ができる

```bash
organism=marchantia
curl -s -H "Content-Type: application/x-ndjson" -XPOST localhost:9200/_bulk --data-binary @data/${organism}_index.json
```

### 3. search_template

```bash
# script作成
bash scripts/generate-search-template.sh search_template/gene_basic.mustache
# search_templateの登録
curl -s -H "Content-Type: application/x-ndjson" -XPOST localhost:9200/_scripts/gene_basic --data-binary @search_template/gene_basic.json
```

### GET

```bash
organism=marchantia
curl -XGET "http://localhost:9200/gene_${organism}/_search/template" -H 'Content-Type: application/json' -d '{"id": "gene_basic", "params": { "query_string": "porphyrin-containing", "size": 10 }}
```