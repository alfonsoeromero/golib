from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


@dataclass(frozen=True)
class GOAnnotation:

    db: str
    db_object_id: str
    db_object_symbol: str
    qualifiers: List[str]
    go_id: str
    db_references: List[str]
    evidence_code: str
    with_or_from: Optional[List[str]]
    aspect: str
    db_object_name: Optional[str]
    db_object_synonyms: Optional[List[str]]
    db_object_type: str
    taxons: List[str]
    date: datetime
    assigned_by: str
    annotation_extension: Optional[List[str]] = None
    gene_product_form_id: Optional[str] = None

    @staticmethod
    def from_line(line) -> 'GOAnnotation':
        args = line.strip().split("\t")
        list_indices = [3, 5, 7, 9, 10, 12, 15, 16]
        for i in list_indices:
            if i < len(args):
                args[i] = args[i].split("|")

        return GOAnnotation(*args)

    def __repr__(self) -> str:
        """Returns a Python representation of this Object"""
        return f"{self.__class__.__name__} ({self.go_id})"
