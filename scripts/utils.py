from typing import Type
from goatools.base import get_godag
from goatools.obo_parser import GODag

GODAG = get_godag("data/go-basic.obo")


def get_godesc(godag: Type[GODag], go_id: str) -> str:
    go = godag.get(go_id)
    if go is None:
        return f"No Description in go-basic.obo, Maybe obsolated"
    return go.name
