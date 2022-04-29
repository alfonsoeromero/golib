from golib.io.obo_parser import OboParser
from golib.io.gaf_parser import GafParser
from core.goterm import GOTerm
from typing import DefaultDict, Dict


class GeneOntology:

    """
    An abstraction to interact with the Gene Ontology

    It allows the user to load a obo structure, and annotate it 
    using GAF files.
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

    def __init__(self, obo:str):
        self._obo = obo
        self._terms: Dict = {}
        # a cache of the aliases to speed-up access
        self._alias_map: Dict = {}

    def build_structure(self):
        """
        Loads the obo file into a DAG structure.
        """
        obo_parser = OboParser(self._obo)
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
                    self._terms[term.go_id].aliases.add(alias.value)

            # set the `is_obsolete` variable
            if "is_obsolete" in stanza.tags:
                self._terms[term.go_id].is_obsolete = True

            stanzas.append(stanza)

        # add relations
        for stanza in stanzas:
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
                        self.find_term(go_id).add_relation(self.find_term(split_relation[1], "part_of")




