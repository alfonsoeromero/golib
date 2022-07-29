from golib.io.obo_parser import OboParser
from golib.io.gaf_parser import GafParser
from golib.core.goterm import GOTerm
from typing import Dict, List
from rich.progress import track
import pandas as pd


class GeneOntology:

    """
    An abstraction to interact with the Gene Ontology

    It allows the user to load a obo structure, and annotate it 
    using GAF files.

    Parameters
    ----------
    obo : str
        The path to the ontology structure in OBO format
    verbose : bool, default True
        If True, progress bars and prints will be used
    """

    EXPERIMENTAL_EVIDENCE_CODES = ["EXP", "IDA", "IPI", "IMP",
                                   "IGI", "IEP", "TAS", "IC"]

    ALL_EVIDENCE_CODES = [
        # experimental
        'EXP', 'IDA', 'IPI', 'IMP', 'IGI', 'IEP',
        # High Throughput
        'HTP', 'HDA', 'HMP', 'HGI', 'HEP',
        # Computational Analysis
        'ISS', 'ISO', 'ISA', 'ISM', 'IGC', 'IBA', 'IBD', 'IKR', 'IRD', 'RCA'
        # Author statement
        'TAS', 'NAS',
        # Curator statement
        'IC', 'ND',
        # Electronic Annotation
        'IEA'
    ]
    DOMAINS = ['biological_process',
               'cellular_component',
               'molecular_function']

    def __init__(self, obo:str, verbose: bool=True):
        self._obo = obo
        self._terms: Dict = {}
        # a cache of the aliases to speed-up access
        self._alias_map: Dict = {}
        self._verbose = verbose
        # useful caches for calculations
        self._annotation_counts_cache: Dict = {}
        self._is_uppropagated: Dict = {}
         

    def find_term(self, go_id: str) -> GOTerm:
        """
        If the go_id is in the structure, return the term, 
        otherwise, find by alias

        Parameters
        ----------
        go_id : str
            The GO ID of the term to find

        Returns
        -------
        GOTerm
            The term instance
        """ 
        try:
            return self._terms[go_id]
        except KeyError:
            return self._terms[self._alias_map[go_id]]

    def build_ontology(self):
        """
        Loads the obo file into a DAG structure.
        """
        obo_parser = OboParser(self._obo)
        stanzas = []
        for stanza in obo_parser:
            if stanza.name != "Term":
                continue
            term = GOTerm(
                stanza.tags["id"][0].value,
                stanza.tags["name"][0].value,
                stanza.tags["namespace"][0].value,
                self)
            self._terms[term.go_id] = term

            # set the aliases
            if "alt_id" in stanza.tags:
                for alias in stanza.tags["alt_id"]:
                    self._alias_map[alias.value] = term.go_id
                    self._terms[term.go_id].aliases.append(alias.value)

            # set the `is_obsolete` variable
            if "is_obsolete" in stanza.tags:
                self._terms[term.go_id].is_obsolete = True

            stanzas.append(stanza)

        # add relations
        for stanza in track(stanzas, description="Building..."):
            go_id = stanza.tags["id"][0].value
            if "is_a" in stanza.tags:
                for related_go_id in stanza.tags["is_a"]:
                    self.find_term(go_id).add_relation(self.find_term(related_go_id.value), "is_a")

            if "relationship" in stanza.tags:
                for relationship in stanza.tags["relationship"]:
                    if relationship.modifiers is not None:
                        # TODO: warn
                        pass
                    split_relation = relationship.value.split()
                    if split_relation[0] == "part_of":
                        self.find_term(go_id).add_relation(self.find_term(split_relation[1]), "part_of")

    def load_gaf_file(self, gaf_file: str, organism_name: str,
                      evidence_codes: List[str]=EXPERIMENTAL_EVIDENCE_CODES,
                      domains: List[str]=DOMAINS,
                      annotate_obsolete: bool=False) -> Dict:
        """
        Loads annotations from a GAF file into the selected annotation set.

        Parameters
        ----------
        gaf_file : str
            Path to the file
        organism_name : str
            annotation set. If it does not exist, it will be created. 
            If it already exists, this function does nothing.

        Returns
        -------
        Dict 
            A dictionary of how many annotations were skipped.
            Keys indicate the reason of the skip, values are the counts.

        Note
        ----
        The loaded annotations are not up-propagated.
        """
        parser = GafParser(gaf_file)
        skip_counter = {k:0 for k in ["term_obsolete", "NOT qualifier", "not_in_domain", "term_not_found"]}
        for annotation in parser:
            if annotation.evidence_code in evidence_codes:
                try:
                    term = self.find_term(annotation.go_id)
                    if term.domain in domains:
                        if len(annotation.qualifiers) > 0:
                            if annotation.qualifiers[0] != "NOT":
                                if annotate_obsolete or not term.is_obsolete:
                                    term.annotations[organism_name][annotation.db_object_id] = 1
                                else:
                                    skip_counter["term_obsolete"] += 1
                            else:
                                skip_counter["NOT qualifier"] += 1
                        else:
                            if annotate_obsolete or not term.is_obsolete:
                                term.annotations[organism_name][annotation.db_object_id] = 1
                            else:
                                skip_counter["term_obsolete"] += 1
                    else:
                        skip_counter["not_in_domain"] += 1
                except KeyError:
                    skip_counter["term_not_found"] += 1
        self._is_uppropagated[organism_name] = False
        return skip_counter

    def up_propagate_annotations(self, organism_name: str,
                                 relations: List[str]=GOTerm.SUPPORTED_RELATIONS) -> None:
        """
        Up-propagate all annotations within an annotation set

        Parameters
        ----------
        organism_name : str
            annotation set
        relations : list of str
            the set of relations that will be considered.

        Notes
        -----
        All relations are assumed to be transitive.
        """
        annotated_terms = set()
        # get annotated terms
        for term in self._terms.values():
            if organism_name in term.annotations:
                annotated_terms.add(term)

        # up-propagate
        for term in track(annotated_terms, description="Up-propagating recursively..."):
            term.up_propagate_annotations(organism_name, relations=relations)

        # store the amounts in the annotation cache
        annotations = self.annotations(organism_name)
        self._annotation_counts_cache[organism_name] = {}
        self._annotation_counts_cache[organism_name]["global"] = annotations.shape[0]
        for domain in GeneOntology.DOMAINS:
            condition = annotations["Domain"] == domain
            count = annotations[condition].shape[0]
            self._annotation_counts_cache[organism_name][domain] = count

        self._is_uppropagated[organism_name] = True
                    
    def annotations(self, organism_name: str) -> pd.DataFrame:
        d = {k: [] for k in ["GO ID", "Protein", "Score", "Domain"]}
        for term in self._terms.values():
            if organism_name in term.annotations:
                for protein, score in term.annotations[organism_name].items():
                    d["GO ID"].append(term.go_id)
                    d["Protein"].append(protein)
                    d["Score"].append(score)
                    d["Domain"].append(term.domain)
        return pd.DataFrame(d)
        
