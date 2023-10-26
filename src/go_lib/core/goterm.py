from dataclasses import dataclass, field
from collections import defaultdict
from typing import Any, ClassVar, DefaultDict, List, Set
import numpy as np

@dataclass
class GOTerm:
    """
    A class representing a Gene Ontology Term
    """
    # Class variables
    SUPPORTED_RELATIONS: ClassVar[List[str]] = ["is_a", "part_of"]
    # Instance variables
    go_id: str
    name: str
    domain: str
    ontology: Any
    # KeyWord arguments
    relations: DefaultDict = field(default_factory=lambda: defaultdict(set))
    annotations: DefaultDict = field(default_factory=lambda: defaultdict(dict))
    aliases: List[str] = field(default_factory=list)
    ic: DefaultDict = field(default_factory=lambda: defaultdict(int))
    is_obsolete: bool = False

    def __hash__(self) -> int:
        return hash(self.go_id)

    def __repr__(self) -> str:
        return f"{self.go_id}"

    def add_relation(self, go_term: Any, relation: str):
        if relation in GOTerm.SUPPORTED_RELATIONS:
            self.relations[relation].add(go_term)
            go_term.relations[f"a_{relation}"].add(self)

    def parents(self, relations: List[str]=SUPPORTED_RELATIONS) -> Set:
        _parents = set()
        for relation in relations:
            _parents |= self.relations[relation]
        return _parents
        
    def ancestors(self, relations: List[str]=SUPPORTED_RELATIONS) -> Set:
        _ancestors = set()
        for relation in relations:
            _ancestors |= self.relations[relation]
            for term in self.relations[relation]:
                _ancestors |= term.ancestors(relations)
        return _ancestors

    def children(self, relations: List[str]=SUPPORTED_RELATIONS) -> Set:
        _children = set()
        for relation in relations:
            _children |= self.relations[f"a_{relation}"]
        return _children

    def descendants(self, relations: List[str]=SUPPORTED_RELATIONS) -> Set:
        _descendants = set()
        for relation in relations:
            _descendants |= self.relations[f"a_{relation}"]
            for term in self.relations[f"a_{relation}"]:
                _descendants |= term.descendants()
        return _descendants

    def up_propagate_annotations(self, organism_name:str,
                                 relations: List[str]=SUPPORTED_RELATIONS,
                                 same_domain: bool=True) -> None:
        """
        Recursively up-propagates the annotations until the root term

        Parameters
        ----------
        organism_name : str
            The annotation set to up-propagate
        relations : list, optional
            A list of relations that will be considered during up-propagation, 
            defaults to all supported relations.
            All relations are assumed to be transitive.
        same_domain : bool, defaults to True
            If true, the up-propagation is constrained to terms belonging to
            the same domain.
        """
        for relation in relations:
            for term in self.relations[relation]:
                if (same_domain and term.domain == self.domain) or not same_domain:
                    for prot, score in self.annotations[organism_name].items():
                        if prot in term.annotations[organism_name].keys():
                            term.annotations[organism_name][prot] = max(
                                term.annotations[organism_name][prot], score
                            )
                        else:
                            term.annotations[organism_name][prot] = score
                    term.up_propagate_annotations(organism_name,
                                                  relations=relations,
                                                  same_domain=same_domain)

    def information_content(self, organism_name: str) -> DefaultDict:
        """
        Calculates the information content of this term considering an annotation set.

        Parameters
        ----------
        organism_name : str
            The organism set to consider for the information content calculation

        Returns
        -------
        float
            The information content of this term within the selected annotation set.

        Notes
        -----
        The information content is stored after the first time is calculated, and therefore
        subsequent calls to this function are considerably faster than the initial call.
        """
        if organism_name not in self.ic:
            annotations_df = self.ontology.get_annotations(organism_name)
            len_annotations = len(self.annotations[organism_name])
            if len_annotations > 0:
                self.ic[organism_name] = -np.log(len_annotations/annotations_df.shape[0])/np.log(2)
            else:
                self.ic[organism_name] = 0
        return self.ic[organism_name]


