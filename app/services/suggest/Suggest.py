from distutils.sysconfig import PREFIX
import os
import re
from typing import List

from SPARQLWrapper import JSON, POST, SPARQLWrapper2

URI_REGEX = (
    "((http|https)://)(www.)?"
    + "[a-zA-Z0-9@:%._\\+~#?&//=]"
    + "{2,256}\\.[a-z]"
    + "{2,6}\\b([-a-zA-Z0-9@:%"
    + "._\\+~#?&//=]*)"
)

OND_NS = "https://data.hetarchief.be/term/onderwijs/"
EXT_NS = "https://w3id.org/onderwijs-vlaanderen/id/"

PREFIX = f"""
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX str: <{EXT_NS}structuur/>
PREFIX col: <{EXT_NS}collectie/>
PREFIX ocol: <{OND_NS}collectie/>

"""

GET_NIVEAUS = (
    PREFIX
    + """
SELECT ?id ?label ?definition ?collection (count(?child) as ?children) (SAMPLE(?parent) as ?parent)
WHERE {{
    {{ col:niveau skos:member ?id. 
       FILTER (?id != str:basisonderwijs)
    }} UNION {{ col:subniveau skos:member ?id. }} 

    ?id a skos:Concept; skos:prefLabel ?label.
    ?c skos:member ?id; skos:prefLabel ?collection.

    OPTIONAL {{ ?id skos:definition ?definition . }}
    OPTIONAL {{ ?id skos:narrower ?child. }}
    OPTIONAL {{ ?id skos:broader ?parent }}
}}
GROUP BY ?id ?label ?definition ?collection
"""
)

GET_COLLECTION_QUERY = (
    PREFIX
    + """
SELECT ?id ?label ?definition (count(?child) as ?child_count) (SAMPLE(?parent) as ?parent_id)
WHERE {{
    BIND(URI('{collection}') AS ?collection)
    ?collection a skos:Collection; skos:member ?id.

    ?id a skos:Concept; skos:prefLabel ?label.

    OPTIONAL {{ ?id skos:definition ?definition . }}
    OPTIONAL {{ ?id skos:narrower ?child. }}
    OPTIONAL {{ ?id skos:broader ?parent }}
}}
GROUP BY ?id ?label ?definition
"""
)

GET_SORTED_COLLECTION_QUERY = (
    PREFIX
    + """
SELECT ?id ?label ?definition ?child_count ?parent_id {{
    SELECT ?id ?label ?definition (count(?mid)-1 as ?position) (count(?child) as ?child_count) (SAMPLE(?parent) as ?parent_id)
    WHERE {{ 
WHERE {{ 
    WHERE {{ 
        BIND(URI('{collection}') AS ?collection)
        
        ?collection a skos:OrderedCollection .

        ?collection skos:memberList/rdf:rest* ?mid . 
  ?collection skos:memberList/rdf:rest* ?mid . 
        ?collection skos:memberList/rdf:rest* ?mid . 
        ?mid rdf:rest* ?node .
        ?node rdf:first ?id .

        ?id a skos:Concept;
            skos:prefLabel ?label.

        OPTIONAL {{ ?id skos:definition ?definition . }}
        OPTIONAL {{ ?id skos:narrower ?child. }}
        OPTIONAL {{ ?id skos:broader ?parent }}
    }}
    
    GROUP BY ?node ?id ?label ?definition
    ORDER BY ?position
}}
"""
)

GET_CHILDREN_QUERY = (
    PREFIX
    + """
SELECT DISTINCT ?id ?label ?definition ?parent
WHERE {{
    ?parent skos:narrower ?id.
    FILTER (?parent IN ({concept}))

    ?id a skos:Concept;
    skos:prefLabel ?label.

    OPTIONAL {{ ?id skos:definition ?definition .}}
}}
ORDER BY ASC(?label)
"""
)

SUGGEST_BY_IDS_QUERY = (
    PREFIX
    + """
SELECT DISTINCT ?id ?label ?definition
WHERE {{
    ocol:thema skos:member ?thema.
    col:graad skos:member ?graad.
    col:vak skos:member ?id.

    ?id a skos:Concept;
        skos:prefLabel ?label;
        skos:related ?thema, ?graad.

    OPTIONAL {{ ?id skos:definition ?definition . }}
    FILTER (?thema IN ({themas}) && ?graad IN ({graden}) )
}}
ORDER BY ASC(?label)
"""
)

GET_CONCEPT_BY_IDS_QUERY = (
    PREFIX
    + """
SELECT DISTINCT ?id ?label ?definition
WHERE {{
    ?id a skos:Concept;
    skos:prefLabel ?label.

    OPTIONAL {{ ?id skos:definition ?definition .}}
    FILTER (?id IN ({concept}))
}}
ORDER BY ASC(?label)
"""
)

GET_CANDIDATES_QUERY = (
    PREFIX
    + """
SELECT DISTINCT ?id ?label ?definition
WHERE {{
    ocol:thema skos:member ?thema.
    col:graad skos:member ?graad.
    col:vak skos:member ?id.

    ?id a skos:Concept;
        skos:prefLabel ?label;
        skos:related ?thema, ?graad.

    OPTIONAL {{ ?id skos:definition ?definition . }}
    FILTER (?thema IN ({themas}) || ?graad IN ({graden}) )
}}
ORDER BY ASC(?label)
"""
)

GET_RELATED_VAK_QUERY = (
    PREFIX
    + """
SELECT DISTINCT ?id ?label ?definition
WHERE {{
    col:vak skos:member ?id.

    ?id a skos:Concept;
    skos:prefLabel ?label;
    skos:related ?concept.

    OPTIONAL {{ ?id skos:definition ?definition . }}
    FILTER (?concept IN ({concepts}))
}}
ORDER BY ASC(?label)
"""
)


# Function to validate URL
# using regular expression
def isValidURI(str):

    # Compile the ReGex
    p = re.compile(URI_REGEX)

    # If the string is empty
    # return false
    if str is None:
        return False

    # Return if the string
    # matched the ReGex
    if re.search(p, str):
        return True

    return False


def join_ids(ids):
    for id in ids:
        if not isValidURI(id):
            raise ValueError("The id {} is not a valid URL.".format(id))

    return ", ".join("<" + str(id) + ">" for id in ids)


def read_query(file_path):
    # check if file is present
    if os.path.isfile(file_path):
        # open text file in read mode
        text_file = open(file_path, "r")

        # read whole file to a string
        data = text_file.read()

        # close file
        text_file.close()
        return data
    return None


class Suggest:
    """A simple api for vocbench data"""

    OND_NS = OND_NS
    EXT_NS = EXT_NS

    def __init__(self, endpoint: str, user: str, password: str):
        self.sparql = SPARQLWrapper2(endpoint)
        self.sparql.setMethod(POST)
        self.sparql.setCredentials(user, password)
        self.sparql.setReturnFormat(JSON)

    def __exec_query(self, query: str, **kwargs):
        formatted = query.format(**kwargs)
        self.sparql.setQuery(formatted)
        ret = self.sparql.queryAndConvert()

        for result in ret.bindings:
            yield {k: v.value for k, v in result.items()}

    def get_concept(self, concept: List[str]):
        """Get thesaurus concept by ids."""

        for res in self.__exec_query(
            GET_CONCEPT_BY_IDS_QUERY, concept=join_ids(concept)
        ):
            yield res

    def get_collection(self, collection: str, sorted: bool = False):
        """Get a collection members by collection id."""

        if not isValidURI(collection):
            raise ValueError("The id {} is not a valid URI.".format(collection))

        query = GET_COLLECTION_QUERY
        if sorted:
            query = GET_SORTED_COLLECTION_QUERY

        for res in self.__exec_query(query, collection=collection):
            yield res

    def get_children(self, concept: List[str]):
        """Get the children of a list of concept ids."""

        for res in self.__exec_query(GET_CHILDREN_QUERY, concept=join_ids(concept)):
            yield res

    def get_vakken(self):
        """Get list 'vakken'."""

        for res in self.get_collection(f"{self.EXT_NS}collectie/vak", True):
            yield res

    def get_themas(self):
        """Get list 'themas'."""

        for res in self.get_collection(f"{self.OND_NS}collectie/thema", True):
            yield res

    def get_graden(self):
        """Get list 'onderwijsgraden'."""

        for res in self.get_collection(f"{self.EXT_NS}collectie/graad"):
            yield res

    def get_niveaus(self):
        """Get list 'onderwijsniveaus'."""

        for res in self.__exec_query(GET_NIVEAUS):
            yield res

    def suggest(self, thema: List[str], graad: List[str]):
        """Suggest 'vakken' based on the identifiers of 'onderwijsgraad' and 'thema'."""

        for res in self.__exec_query(
            SUGGEST_BY_IDS_QUERY,
            themas=join_ids(thema),
            graden=join_ids(graad),
        ):
            yield res

    def get_candidates(self, thema: List[str], graad: List[str]):
        """Get all possible 'vakken' based on the identifiers of 'onderwijsgraad' and 'thema'."""

        for res in self.__exec_query(
            GET_CANDIDATES_QUERY,
            themas=join_ids(thema),
            graden=join_ids(graad),
        ):
            yield res

    def get_related_vak(self, concept: List[str]):
        """Get related vak by concept ids."""

        for res in self.__exec_query(GET_RELATED_VAK_QUERY, concepts=join_ids(concept)):
            yield res
