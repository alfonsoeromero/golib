import abc
import numpy as np
import numpy.typing as npt

from golib.core.gene_ontology import GeneOntology
from golib.core.goterm import GOTerm
from rich.progress import track
from typing import Dict, Set

class SemanticSimilarityMixin(metaclass=abc.ABCMeta):
    """
    Abstract class for semantic similarity API
    """
    def __init__(self, ontology: GeneOntology) -> None:
        self.ontology = ontology

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, "gene_wise") and 
                callable(subclass.gene_wise) and 
                hasattr(subclass, "term_wise") and 
                callable(subclass.term_wise) or
                NotImplemented)

    @abc.abstractmethod
    def term_wise(self, ontology: GeneOntology, 
                  organism_name: str) -> Dict[str, npt.NDArray]:
        raise NotImplementedError

    @abc.abstractmethod
    def gene_wise(self, ontology: GeneOntology, 
                  organism_name: str) -> Dict[str, npt.NDArray]:
        raise NotImplementedError

    def lowest_common_ancestor(self, ancestors_a: Set[GOTerm], ancestors_b: Set[GOTerm],
                               organism_name: str, domain: str) -> float:
        domain_count = self.ontology._annotation_counts_cache[organism_name][domain]
        term_count = domain_count

        common_ancestors = ancestors_a & ancestors_b
        for t in common_ancestors:
            t_count = len(t.annotations[organism_name])
            if t_count < term_count:
                term_count = t_count
        return term_count / domain_count

class Resnik(SemanticSimilarityMixin):

    def __init__(self, ontology: GeneOntology) -> None:
        super().__init__(ontology)
        self._ancestor_cache: Dict = {}

    def _build_ancestor_cache(self, organism_name: str) -> None:
        if organism_name in self._ancestor_cache:
            return
        self._ancestor_cache[organism_name] = {}
        for go_id, term in track(self.ontology._terms.items(), description="Building ancetry cache"):
            if len(term.annotations[organism_name]) > 0:
                self._ancestor_cache[organism_name][term] = term.ancestors() 

    def term_wise(self, organism_name: str) -> Dict[str, npt.NDArray]:
        self._build_ancestor_cache(organism_name)
        ss = {}
        for domain in GeneOntology.DOMAINS:
            terms = [t for t in self._ancestor_cache[organism_name].keys() if t.domain == domain]
            N = len(terms)
            ss[domain] = {
                "terms":[t.go_id for t in terms],
                "similarity": np.zeros((N,N))
            }
            print(domain)
            for i in track(range(N), description=f"Calculating {domain} semantic similarity..."):
                for j in range(i, N):
                    r = -np.log(self.lowest_common_ancestor(
                        self._ancestor_cache[organism_name][terms[i]], 
                        self._ancestor_cache[organism_name][terms[j]],
                        organism_name=organism_name, 
                        domain=domain))
                    ss[domain]["similarity"][i,j] = r
                    ss[domain]["similarity"][j,i] = r
        return ss

    def gene_wise(self, ontology: GeneOntology, 
                  organism_name: str,
                  domain: str) -> Dict[str, npt.NDArray]:
        term_wise = self.term_wise(ontology, organism_name)
        
        return {"a": np.zeros((10,))}
