import abc
import numpy as np
import numpy.typing as npt

from golib.core.gene_ontology import GeneOntology
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

    def term_wise(self, ontology: GeneOntology, 
                  organism_name: str) -> Dict[str, npt.NDArray]:

        return {"a": np.zeros((10,))}

    def gene_wise(self, ontology: GeneOntology, 
                  organism_name: str) -> Dict[str, npt.NDArray]:
        term_wise = self.term_wise()
        
        return {"a": np.zeros((10,))}
