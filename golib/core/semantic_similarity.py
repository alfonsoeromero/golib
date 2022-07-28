import abc
import numpy as np
import numpy.typing as npt

from golib.core.gene_ontology import GeneOntology
from golib.core.goterm import lowest_common_ancestor
from typing import Dict

class SemanticSimilarityMixin(metaclass=abc.ABCMeta):
    """
    Abstract class for semantic similarity API
    """
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


class Resnik(SemanticSimilarityMixin):

    _ancestor_cache: Dict = {}

    def term_wise(self, ontology: GeneOntology, 
                  organism_name: str) -> Dict[str, npt.NDArray]:
        ss = {}
        for domain in GeneOntology.DOMAINS:
            terms = [t for t in ontology._terms if t.domain == domain]
            N = len(terms)
            ss[domain] = np.zeros((N,N))
            for i in range(N):
                for j in range(i, N):
                    r = -np.log(lowest_common_ancestor(terms[i], terms[j], 
                                                       organism_name=organism_name,
                                                       domain=domain))
                    ss[domain][i,j] = r
                    ss[domain][j,i] = r

        return ss

    def gene_wise(self, ontology: GeneOntology, 
                  organism_name: str,
                  domain: str) -> Dict[str, npt.NDArray]:
        term_wise = self.term_wise(ontology, organism_name)
        
        return {"a": np.zeros((10,))}
